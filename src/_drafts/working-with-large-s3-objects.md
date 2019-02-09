---
layout: post
title: Working with really large objects in S3
summary: Some code that allows you to process or selectively read large objects in S3 without downloading the entire object first.
tags: python aws
---

One of our current work projects involves working with large ZIP files stored in S3.
These are files in the [BagIt format][bagit], which contain files we want to put in long-term digital storage.
Part of this process involves unpacking the ZIP, and examining and verifying every file.
So far, so easy -- the AWS SDK allows us to read objects from S3, and there are plenty of libraries for dealing with ZIP files.

In Python, you can do something like:

```python
import zipfile

import boto3

s3 = boto3.client("s3")
s3.download_file(Bucket="bukkit", Key="bagit.zip", Filename="bagit.zip")

with zipfile.ZipFile("bagit.zip") as zf:
    print(zf.namelist())
```

This is what most code examples for working with S3 look like -- download the entire file first (whether to disk or in-memory), then work with the complete copy.

Where this breaks down is if you have an exceptionally large file, or you're working in a constrained environment.
Some of our BagIt files are tens of gigabytes, and the largest might be over half a terabyte (even if the individual files are small).
And if you've gone serverless and you're running in AWS Lambda, you only get [500 MB of disk space][lambda_faq].
What are we to do?

To process a ZIP file (like many formats), you don't need to load the entire file at once -- it has a well-defined internal structure, and you can read it a bit at a time.
In a ZIP, there's a table of contents that tells you what files it contains, and where they are in the overall ZIP.
If you want to extract a single file, you can read the table of contents, then jump straight to that file -- ignoring everything else.
This is easy if you're working with a file on disk, and S3 allows you to read a specific section of a object if you pass [an HTTP Range header][range_hdr] in your GetObject request.

So if we construct a wrapper for S3 objects that passes the correct Range headers, we can process a large object in S3 without downloading the whole thing.

I couldn't find any public examples of somebody doing this, so I decided to try it myself.
In this post, I'll walk you through how I was able to stream a large ZIP file from S3.
But fair warning: I wrote this as an experiment, not as production code.
You're welcome to use it, but you might want to test it first.

[bagit]: https://en.wikipedia.org/wiki/BagIt
[lambda_faq]: https://aws.amazon.com/lambda/faqs/
[range_hdr]: https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests-request-headers

## Getting a file-like object

In Python, there's a notion of a *"file-like object"* -- a wrapper around some I/O that behaves like a file, even if it isn't actually a file on disk.
It responds to calls like `read()` and `write()`, and you can use it in places where you'd ordinarily use a file.
The docs for the [io library][io_lib] explain the different methods that a file-like object can support, although not every file-like object supports every method -- for example, you can't `write()` to an HTTP response body.

Many libraries that work with local files can also work with file-like objects, including the [zipfile module][zipfile] in the Python standard library.
If we can get a file-like object from S3, we can pass that around and most libraries won't know the difference!

The boto3 SDK actually already gives us one file-like object, when you call GetObject.
Like so:

```python
import boto3

s3 = boto3.client("s3")
s3_object = s3.get_object(Bucket="bukkit", Key="bagit.zip")

print(s3_object["Body"])
# <botocore.response.StreamingBody object at 0x10c46f438>
```

That StreamingBody is a file-like object responds to `read()`, which allows you to download the entire file into memory.
So let's try passing that into ZipFile:

```python
import zipfile

import boto3

s3 = boto3.client("s3")
s3_object = s3.get_object(Bucket="bukkit", Key="bagit.zip")
streaming_body = s3_object["Body"]

with zipfile.ZipFile(streaming_body) as zf:
    print(zf.namelist())
```

Unfortunately, that throws an error:

```
Traceback (most recent call last):
  File "example.py", line 11, in <module>
    with zipfile.ZipFile(s3_object["Body"]) as zf:
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/zipfile.py", line 1108, in __init__
    self._RealGetContents()
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/zipfile.py", line 1171, in _RealGetContents
    endrec = _EndRecData(fp)
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/zipfile.py", line 241, in _EndRecData
    fpin.seek(0, 2)
AttributeError: 'StreamingBody' object has no attribute 'seek'
```

So although StreamingBody is file-like, it doesn't support the methods we need.
We'll have to create our own file-like object, and define those methods ourselves.

[io_lib]: https://docs.python.org/3/library/io.html
[zipfile]: https://docs.python.org/3/library/zipfile.html


## Creating our own file-like object

The io docs suggest a good base for a read-only file-like object that returns bytes (the S3 SDK deals entirely in bytestrings) is RawIOBase, so let's start with a skeleton class:

```python
import io


class S3File(io.RawIOBase):
    def __init__(self, s3_object):
        self.s3_object = s3_object
```

Note: the constructor expects an instance of [boto3.S3.Object][boto3_obj], which you might create directly or via a boto3 resource.
This means our class doesn't have to create an S3 client or deal with authentication -- it can stay simple, and just focus on I/O operations.


## Implementing the seek() method

When we tried to load a ZIP file the first time, we discovered that somewhere the zipfile module is using the seek() method.
Let's implement that as our first operation.
The io docs explain [how seek() works][io_seek]:

> <strong>seek</strong>(offset[, whence])
>
> Change the stream position to the given byte `offset`. `offset` is interpreted relative to the position indicated by `whence`. The default value for `whence` is `SEEK_SET`. Values for whence are:
>
> * `SEEK_SET` or 0 – start of the stream (the default); `offset` should be zero or positive
> * `SEEK_CUR` or 1 – current stream position; `offset` may be negative
> * `SEEK_END` or 2 – end of the stream; `offset` is usually negative
>
> Return the new absolute position.

This hints at the key part of doing selective reads: we need to know how far through we are.
What part of the object are we currently looking at?
When we open a file on disk, the OS handles that for us -- but in this case, we'll need to track it ourselves.

This is what a seek() method might look like:

```python
import io


class S3File(io.RawIOBase):
    def __init__(self, s3_object):
        self.s3_object = s3_object
        self.position = 0

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.position = offset
        elif whence == io.SEEK_CUR:
            self.position += offset
        elif whence == io.SEEK_END:
            self.position = self.s3_object.content_length + offset
        else:
            raise ValueError("invalid whence (%r, should be %d, %d, %d)" % (
                whence, io.SEEK_SET, io.SEEK_CUR, io.SEEK_END
            ))

        return self.position

    def seekable(self):
        return True
```

We've added the `position` attribute to track where we are in the stream, and that's what we update when we call `seek()`.

The `content_length` attribute on the S3 object tells us its length in bytes, which corresponds to the end of the stream.

For the ValueError, I copied the error you get if you pass an unexpected whence to a regular open() call:

```pycon
>>> open("example.py").seek(5, 5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid whence (5, should be 0, 1 or 2)
```

Now let's try using this updated version:

```python
s3 = boto3.resource("s3")
s3_object = s3.Object(bucket_name="bukkit", key="bag.zip")

s3_file = S3File(s3_object)

with zipfile.ZipFile(s3_file) as zf:
    print(zf.namelist())
```

This gets further, but now it throws a different error:

```
Traceback (most recent call last):
  File "example.py", line 38, in <module>
    with zipfile.ZipFile(s3_file) as zf:
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/zipfile.py", line 1108, in __init__
    self._RealGetContents()
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/zipfile.py", line 1171, in _RealGetContents
    endrec = _EndRecData(fp)
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/zipfile.py", line 251, in _EndRecData
    data = fpin.read()
NotImplementedError
```

So we know what to implement next!

[boto3_obj]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html?highlight=s3#S3.Object
[io_seek]: https://docs.python.org/3/library/io.html?highlight=io#io.IOBase.seek


## Implementing the read() method

The io docs explain [how read() works][io_read]:

> **read**(size=-1)
>
> Read up to `size` bytes from the object and return them. As a convenience, if `size` is unspecified or -1, all bytes until EOF are returned. Otherwise, only one system call is ever made. Fewer than `size` bytes may be returned if the operating system call returns fewer than `size` bytes.
>
> If 0 bytes are returned, and `size` was not 0, this indicates end of file. If the object is in non-blocking mode and no bytes are available, None is returned.

To implement this method, we have to remember that we read from the position set by `seek()` -- not necessarily the start of object.
And when we've read some bytes, we need to advance the position.

To read a specific section of an S3 object, we pass an HTTP Range header into the get() call, which defines what part of the object we want to read.

So let's add a read() method:

```python
class S3File(io.RawIOBase):
    ...

    @property
    def size(self):
        return self.s3_object.content_length

    def read(self, size=-1):
        if size == -1:
            # Read to the end of the file
            range_header = "bytes=%d-" % self.position
            self.seek(offset=0, whence=io.SEEK_END)
        else:
            new_position = self.position + size

            # If we're going to read beyond the end of the object, return
            # the entire object.
            if new_position >= self.size:
                return self.read()

            range_header = "bytes=%d-%d" % (self.position, new_position - 1)
            self.seek(offset=size, whence=io.SEEK_CUR)

        return self.s3_object.get(Range=range_header)["Body"].read()

    def readable(self):
        return True
```

This is a little more complicated than seek().

I've added a `size` property that exposes the length of the stream, and wraps the `content_length` attribute.
This is for convenience.

If the user doesn't specify a size for `read()`, we create an open-ended Range header and seek to the end of the file.
Note that I'm calling `seek()` rather than updating the position manually -- it saves me writing a second copy of the logic for tracking the position.

If the caller passes a size to `read()`, we need to work out if this size goes beyond the end of the object -- in which case we should truncate it!
If it is too big, we fall back to reading the entire object, by making a second call to `read()` -- we don't need to duplicate that logic.
If it's not, we create a Range header (and note that byte ranges include the upper value, hence the -1), and seek to the appropriate position.

Then we call the get() method on the object, pass the Range header, and read all the bytes that come back.

If you use this version of the code, we can load the list of files in the ZIP correctly:

```python
s3 = boto3.resource("s3")
s3_object = s3.Object(bucket_name="bukkit", key="bag.zip")

s3_file = S3File(s3_object)

with zipfile.ZipFile(s3_file) as zf:
    print(zf.namelist())
```

And that's all you need to do selective reads from S3.

[io_read]: https://docs.python.org/3/library/io.html?highlight=io#io.RawIOBase.read


## Is it worth it?

There's a small cost to making GetObject calls in S3 -- both in money and performance.

This wrapper class uses more GetObject calls than downloading the object once.
In my brief experiments, it took 3 calls to load the table of contents, and another 3 calls to load an individual file.
If you can, it's cheaper and faster to download the entire object to disk, and do all the processing locally -- but only if you have the resources to do so!
This wrapper is useful when you can't do that.

In practice, I'd probably use a hybrid approach: download the entire object if it's small enough, or use this wrapper if not.
I'd trade some extra performance and lower costs for a bit more code complexity.

At work, we write everything in Scala, so I don't think we'll ever use this code directly.
(At best, we'll use the ideas it contains.)
But this post proves the general idea: you can process a large object in S3 without having to download the whole thing first.



## Putting it all together: the final code

Adding a couple of extra convenience methods (a repr() for pretty-printing, and tell() is a useful convenience), this is the final code, along with the example:

```python
import io


class S3File(io.RawIOBase):
    def __init__(self, s3_object):
        self.s3_object = s3_object
        self.position = 0

    def __repr__(self):
        return "<%s s3_object=%r>" % (type(self).__name__, self.s3_object)

    @property
    def size(self):
        return self.s3_object.content_length

    def tell(self):
        return self.position

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.position = offset
        elif whence == io.SEEK_CUR:
            self.position += offset
        elif whence == io.SEEK_END:
            self.position = self.size + offset
        else:
            raise ValueError("invalid whence (%r, should be %d, %d, %d)" % (
                whence, io.SEEK_SET, io.SEEK_CUR, io.SEEK_END
            ))

        return self.position

    def seekable(self):
        return True

    def read(self, size=-1):
        if size == -1:
            # Read to the end of the file
            range_header = "bytes=%d-" % self.position
            self.seek(offset=0, whence=io.SEEK_END)
        else:
            new_position = self.position + size

            # If we're going to read beyond the end of the object, return
            # the entire object.
            if new_position >= self.size:
                return self.read()

            range_header = "bytes=%d-%d" % (self.position, new_position - 1)
            self.seek(offset=size, whence=io.SEEK_CUR)

        return self.s3_object.get(Range=range_header)["Body"].read()

    def readable(self):
        return True


if __name__ == "__main__":
    import zipfile

    import boto3

    s3 = boto3.resource("s3")
    s3_object = s3.Object(bucket_name="bukkit", key="bagit.zip")

    s3_file = S3File(s3_object)

    with zipfile.ZipFile(s3_file) as zf:
        print(zf.namelist())
```

As I said at the top, I wrote this as an experiment, not as production code.
Feel free to use it ([MIT licence][mit]), but you probably want to do some more testing first!

[mit]: https://opensource.org/licenses/MIT
