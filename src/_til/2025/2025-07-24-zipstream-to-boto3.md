---
layout: til
title: Using zipstream to stream new zip files to object storage with boto3
summary: You can construct a `zipstream.ZipFile`, add files, then wrap it in a file-like object to upload it with `S3.upload_fileobj`.
date: 2025-07-24 11:42:15 +01:00
tags:
  - python
  - python:boto3
---
I'm writing some code to build large ZIP files and store them in [S3-compatible object storage](/til/2025/linode-with-boto3/).

I could build the ZIP as a local file, and then upload it to the cloud -- but that means I need to have enough local disk space to store the entire file before I begin uploading.
Alternatively, I could store the zip in an in-memory buffer -- but now I need lots of memory instead of lots of disk.
What if I could generate the ZIP file piece-by-piece, so I don't need to hold the whole thing at once?

I found Allan Lei's [zipstream module](https://github.com/allanlei/python-zipstream), which does exactly what I want:

> Like Python's ZipFile module, except it works as a generator that provides the file in many small chunks.

It took a bit of work to integrate it with boto3.

(I was using [Linode object storage](/til/2025/linode-with-boto3/) for all of these examples, but I think it should be the same for any S3-compatible storage that works with boto3.)

I'm using boto3 1.38.19 and zipstream 1.1.4.

## You need to pass a file-like object

Here's my first attempt, based on the code in the python-zipstream README.
I construct the `ZipFile`, add files, then pass it directly to `upload_fileobj`.

```python
import boto3
import zipstream

s3_client = boto3.client("s3")

zf = zipstream.ZipFile(mode="w")

zf.writestr(arcname="greeting.txt", data=b"Hello world!")
zf.writestr(arcname="numbers.json", data=b"[1, 2, 3, 4, 5]")

# ❌ Does not work ❌
s3_client.upload_fileobj(
    Fileobj=zf,
    Bucket="my-example-bucket",
    Key="example.zip"
)
```

This fails with an exception:

```
KeyError: 'There is no item named 8388608 in the archive'
```

This is because `upload_fileobj` expects to receive a file-like object, whereas `zipstream.ZipFile` is giving it an iterable of `bytes`.
We can write a wrapper class that transforms the `ZipFile` to get our first working upload.

```python
class FileLikeObject:
    """
    Wrap an iterable of ``bytes`` and turn it into a file-like object
    that can be passed to ``S3Client.upload_fileobj``.
    """

    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.buffer = b""

    def read(self, size=-1) -> bytes:
        """
        Read up to ``size`` bytes from the object and return them.

        If ``size`` is unspecified or -1, all bytes until EOF are returned.
        Fewer than ``size`` bytes may be returned if there are less than
        ``size`` bytes left in the iterator.
        """
        size: int = size or -1

        # Fill the buffer with enough bytes to fulfil the request.
        while size < 0 or len(self.buffer) < size:
            try:
                chunk = next(self.iterator)
                self.buffer += chunk
            except StopIteration:
                break

        if size < 0:
            result, self.buffer = self.buffer, b""
        else:
            result, self.buffer = self.buffer[:size], self.buffer[size:]

        return result


s3_client.upload_fileobj(
    Fileobj=FileLikeObject(zf),
    Bucket="example-bucket",
    Key="example.zip",
)
```

This wrapper class also gives an opportunity to capture other data as the stream is being uploaded -- for example, if you wanted to get the size or checksum of the ZIP file as it's being created.

## Set `allowZip64=True` if you want big ZIP files

By default, ZIP files have a limit of 4 GB and 65,535 files.
If you want bigger zip files, you need to use the ZIP64 extension.
In zipstream, this is disabled by default.

If you try to upload a ZIP file that exceeds these limits:

```python
zf = zipstream.ZipFile(mode="w")

for i in range(100000):
    s = str(i).zfill(6)

    zf.writestr(arcname=f'numbers/{s[1]}/{s[2]}/{s}.txt', data=s.encode("utf8"))

s3_client.upload_fileobj(
    Fileobj=FileLikeObject(zf),
    Bucket="example-bucket",
    Key="numbers.zip",
)
```

then the upload fails with an error:

```
zipfile.LargeZipFile: Files count would require ZIP64 extensions
```

You need to set `allowZip64=True`:

```python
zf = zipstream.ZipFile(mode="w", allowZip64=True)
```

and then the upload succeeds.
