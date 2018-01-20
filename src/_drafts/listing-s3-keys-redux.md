---
layout: post
summary: Python functions for getting a list of keys and objects in an S3 bucket.
tags: aws python
title: Listing keys in an S3 bucket with Python, redux
---

A few months ago, I wrote about some code for [listing keys in an S3 bucket](/2017/07/listing-s3-keys/).
I've been running variants of that code in production since then, and found a pair of mistakes in the original version.

Specifically:

*   It gives an unhelpful error if there aren't any matching keys, and
*   The generator is a bit too overzealous in discarding information.

Since that post has been fairly popular, I thought it was worth writing a short update.
In this post, I'll walk through the changes I've made in the newer versions of the code.

<!-- summary -->

As a quick reminder, this is the code we had at the end of the last post:

```python
import boto3


def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield key

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
```

First, let's see what happens if you use this code and there aren't any matching keys:

```pycon
>>> for key in get_matching_s3_keys(bucket='empty-bucket'):
...     print(key)
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "matching_s3_objects.py", line 27, in get_matching_s3_keys
    for obj in resp['Contents']:
KeyError: 'Contents'
```

If there aren't any matching keys, the ListObjects API doesn't include a "Contents" key in the response -- if that happens, we should return immediately.

We can fix this by checking that "Contents" is in the response before we try to iterate over it:

```python
try:
    contents = resp['Contents']
except KeyError:
    return

for obj in contents:
    ...
```

Now, if we don't have any matching keys in the bucket, we get back an empty generator, not an exception:

```pycon
>>> list(updated_get_matching_s3_keys(bucket='empty-bucket'))
[]
```

The second issue is that this generator only produces keys, but the ListObjects API call includes more information that just gets thrown away, including size, modified date, and ETag.
There have been times I want that information as well, and I have to edit the code so that it returns more than the key.

Rather than editing the code to get more info, it would be better to split this function into two generators: one that finds the matching objects, and one that spits out key names.
That way, if I want extra info, I can just use the output of the first generator.

To modify the generator to spit out objects, I can rename it to `get_matching_s3_objects`, and modify the yield as follows:

```python
for obj in resp['Contents']:
    key = obj['Key']
    if key.startswith(prefix) and key.endswith(suffix):
        yield obj
```

Then I can write a second generator that produces keys:

```python
def get_matching_s3_keys(bucket, prefix='', suffix=''):
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj['Key']
```

Putting all that together, here's my latest version of the code:

```python
import boto3


def get_matching_s3_objects(bucket, prefix='', suffix=''):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp['Contents']
        except KeyError:
            return

        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield obj

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj['Key']
```

If you've used the original code, I'd recommend switching to use this updated version.
You can find the code, along with a couple of tests, [on GitHub][github].

[github]: https://github.com/alexwlchan/alexwlchan.net/tree/master/code/matching_s3_objects
