---
layout: post
date: 2019-07-03 19:33:55 +0000
title: Listing even more keys in an S3 bucket with Python
summary: Python functions for getting a list of keys and objects in an S3 bucket.
category: Working with AWS
---

Two years ago, I wrote a Python function for [listing keys in an S3 bucket](/2017/07/listing-s3-keys/).
At the time I was still very new to AWS and the boto3 library, and I thought this might be a useful snippet -- turns out it's by far the most popular post on the site!

I added [a couple of bugfixes](/2018/01/listing-s3-keys-redux/) a few months later, but otherwise I haven't touched it since.

Part of that code is handling pagination in the S3 API -- it makes a series of calls to the ListObjectsV2 API, fetching up to 1000 objects at a time.
Every response includes a "continuation token", and you pass that token into your next API call to get the next page of results.

It turns out the boto3 SDK can handle this for you, with [paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html).
Rather than doing the pagination manually, you call a paginator and it handles that for you.

Here's an example:

```python
import boto3

client = boto3.client("s3")

paginator = client.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket="my-bucket-name"):
    print(page["Contents"])
```

Each `page` is the equivalent of a `resp` in the original code -- but it's a bit simpler.

There are quite a few paginators in the boto3 SDK, and they save you having to work out how any given API implements pagination (because they're not consistent).
So if you want to list keys in an S3 bucket with Python, this is the paginator-flavoured code that I use these days:

```python
import boto3


def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix, )
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]
```

Along with the paginator support, I've made one other change:

The `prefix` argument can take a string or a tuple, to match the behaviour of Python's `str.startswith(…)` method.
Previously, if you passed multiple prefixes, the function would list the entire bucket and filter the results post-API call.
Now, it makes individual ListObjects calls for each prefix, which should be faster and cheaper.

For example, if you wanted to look at `a/` and `z/`, the old code would fetch everything from `b/` to `y/` as well.
Now it fetches all of `a/`, then all of `z/`, then finishes.

You can drop this code straight in place of the old code, and it should work exactly the same.
Fully backwards compatible!

As with all my other code, this is released under the [MIT license](https://github.com/alexwlchan/alexwlchan.net/blob/9a80d17de47b130772bb5433592e8fffd1d18118/LICENSE).
If you use it, please include a copyright statement and a link back to the original blog post.
And if you're feeling generous, perhaps send me a thank you note or [a couple of coins](https://ko-fi.com/alexwlchan)?
