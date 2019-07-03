---
layout: post
date: 2017-07-18 08:30:00 +0000
summary: A short Python function for getting a list of keys in an S3 bucket.
tags: aws python
title: Listing keys in an S3 bucket with Python
category: Working with AWS
---

{% update 2019-07-03 %}
  In the two years since I wrote this post, I've fixed a couple of bugs, made the code more efficient, and started using [paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) to make it simpler.
  If you want to use it, I'd recommend using the [updated version](/2019/07/listing-s3-keys/).
{% endupdate %}

A lot of my recent work has involved batch processing on files stored in Amazon S3.
It's been very useful to have a list of files (or rather, keys) in the S3 bucket – for example, to get an idea of how many files there are to process, or whether they follow a particular naming scheme.

The AWS APIs (via [boto3][boto3]) do provide a way to get this information, but API calls are paginated and don't expose key names directly.
It's a bit fiddly, and I don't generally care about the details of the AWS APIs when using this list -- so I wrote a wrapper function to do it for me.
All the messiness of dealing with the S3 API is hidden in general use.

Since this function has been useful in lots of places, I thought it would be worth writing it up properly.

<!-- summary -->

The first place to look is the [`list_objects_v2` method][list_objects] in the boto3 library.
We call it like so:

```python
import boto3

s3 = boto3.client('s3')
s3.list_objects_v2(Bucket='example-bukkit')
```

The response is a dictionary with a number of fields.
The `Contents` key contains metadata (as a dict) about each object that's returned, which in turn has a `Key` field with the object's key.
This is easier to explain with a code example:

```python
def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""
    keys = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys
```

This is great -- if we only have a few objects in our bucket.
But an S3 bucket can contain many keys, more than could practically be returned in a single API response, so the API is paginated.
This call only returns the first 1000&nbsp;keys.

API responses have a `ContinuationToken` field, which can be passed to the ListObjects API to get the next page of results.
By looking for this token, and using it to make another request, we can steadily fetch every key in the bucket:

```python
def get_all_s3_keys(bucket):
    """Get a list of all keys in an S3 bucket."""
    keys = []

    kwargs = {'Bucket': bucket}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            keys.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

    return keys
```

Let's unpack what's going on here.
The `kwargs` dictionary contains the parameters that we're passing to the `list_objects_v2` method.
This allows us to update the parameters we're using as we get new information (specifically, when we get the first continuation token).
Passing them in as `**kwargs` causes them to be unpacked and used as named parameters, as if we'd run:

```python
s3.list_objects_v2(Bucket=bucket, ContinuationToken=resp['NextContinuationToken'])
```

Using a dict is more flexible than if we used `if … else`, because we can modify the keys however we like.
You might have seen the reverse of this, when functions collect arbitrary keyword arguments [as follows][kwargs]:

```python
def foo(arg1, arg2, **kwargs):
    ...
```

(In fact, this is how large chunks of the boto3 package are implemented.)

Once we've got a response, we extract the continuation token and add it to `kwargs`, which means we'll pass it on the next ListObjects call.
When we're on the final page of results, the `ContinuationToken` field is omitted (because there's nowhere to continue to) – at which point the KeyError tells us that we should stop looking, and return the list to the user.

(If you read the boto3 documentation about the response, you'll see we could also look at the `isTruncated` field to decide if there are more keys to fetch.)

So now we have a list of all the keys in our bucket.
But this function will fetch every key upfront -- that's slow, because it might make many API requests, and memory-expensive, because it puts every key in a list.
Python has support for lazy generators with the `yield` keyword -- rather than computing every result upfront, we compute results as they're required.
This is essential for infinite iterators, or in this case, iterators that are very large.

Here's what the function looks like if we rewrite it as a generator:

```python
def get_s3_keys_as_generator(bucket):
    """Generate all the keys in an S3 bucket."""
    kwargs = {'Bucket': bucket}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            yield obj['Key']

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
```

Not only is this more efficient, it also makes the function a bit shorter and neater.

The version I use has one more step -- filtering on prefix and suffix.
This is useful if I'm looking at keys in a particular directory, or of a particular file type.

The prefix is an argument that can be passed directly to the AWS APIs -- S3 stores objects in alphabetical order, so filtering by prefix is cheap (this is a bit of a handwave, but I think it's roughly correct).
We have to filter the suffix after we have the API results, because that involves inspecting every key manually.

This is what the function looks like when we add prefix and suffix arguments:

```python
def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    kwargs = {'Bucket': bucket, 'Prefix': prefix}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.endswith(suffix):
                yield key

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
```

And here's one more neat trick -- in Python, the `startswith` and `endswith` method on strings can take a string, or a tuple of strings, and in the latter case, return True if any of them match.
For example:

```python
>>> 'xyz'.startswith('x')
True
>>> 'xyz'.startswith(('x', 'X'))
True
>>> 'abc'.endswith(('c', 'd', 'e'))
True
>>> 'def'.endswith(('0', '1'))
False
```

We already have the suffix behaviour, and it's only a little more work to get it working for prefixes.
This is the function I have in my codebase:

```python
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

Because it's a generator, you use this function by looping over it directly.
For example:

```python
for key in get_matching_s3_keys(bucket='bukkit', prefix='images/', suffix='.jpg'):
    print(key)
```

And we can also pass a tuple of prefixes or suffixes -- if, for example, the file extension isn't always the same case:

```python
for key in get_matching_s3_keys(bucket='bukkit', suffix=('.jpg', '.JPG')):
    print(key)
```

This function absorbs all the messiness of dealing with the S3 API, and I can focus on actually using the keys.
Although S3 isn't actually a traditional filesystem, it behaves in very similar ways -- and this function helps close the gap.

{% update 2019-07-03 %}
  In the two years since I wrote this post, I've fixed a couple of bugs, made the code more efficient, and started using [paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) to make it simpler.
  If you want to use it, I'd recommend using the [updated version](/2019/07/listing-s3-keys/).
{% endupdate %}

[boto3]: https://github.com/boto/boto3
[list_objects]: https://boto3.readthedocs.io/en/stable/reference/services/s3.html#S3.Client.list_objects_v2
[kwargs]: https://stackoverflow.com/q/36901/1558022
