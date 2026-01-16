---
layout: post
date: 2023-07-28 05:13:02 +00:00
title: Parsing CloudFront logs with Python
summary: A couple of functions I use to get access to CloudFront logs as easy-to-use iterators.
tags:
  - python
  - aws
  - aws:amazon cloudfront
colors:
  css_light: "#673ABB"
  css_dark:  "#C9ABFF"
---

I've been doing work recently to analyse some [CloudFront access logs][logs].
There are lots of ways to do this, and I normally reach for Python inside a [Jupyter Notebook] because those are tools I'm very familiar with.
I've done this a few times now, so I thought it'd be worth pulling out some of the common functions I write every time.

The first is a parsing function, which gets the individual log entries from a single log file.
This takes a file-like object in binary mode, so works the same whether I'm reading the file from a local disk or directly from S3.
This is what it looks like:

```python
import datetime
import urllib.parse


def parse_cloudfront_logs(log_file):
    """
    Parse the individual log entries in a CloudFront access log file.

    Here ``logfile`` should be a file-like object opened in binary mode.

    The format of these log files is described in the CloudFront docs:
    https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html#LogFileFormat

    """
    # The first line is a version header, e.g.
    #
    #     b'#Version: 1.0\n'
    #
    next(log_file)

    # The second line tells us what the fields are, e.g.
    #
    #     b'#Fields: date time x-edge-location …\n'
    #
    header = next(log_file)

    field_names = [
        name.decode("utf8")
        for name in header.replace(b"#Fields:", b"").split()
    ]

    # For each of the remaining lines in the file, the values will be
    # space-separated, e.g.
    #
    #     b'2023-06-26  00:05:49  DUB2-C1  618  1.2.3.4  GET  …'
    #
    # Split the line into individual values, then combine with the field
    # names to generate a series of dict objects, one per log entry.
    #
    # For an explanation of individual fields, see the CloudFront docs:
    # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html#LogFileFormat
    numeric_fields = {
        "cs-bytes": int,
        "sc-bytes": int,
        "sc-content-len": int,
        "sc-status": int,
        "time-taken": float,
        "time-to-first-byte": float,
    }

    url_encoded_fields = {
        "cs-uri-stem",
        "cs-uri-query",
    }

    nullable_fields = {
        "cs(Cookie)",
        "cs(Referer)",
        "cs-uri-query",
        "fle-encrypted-fields",
        "fle-status",
        "sc-range-end",
        "sc-range-start",
        "sc-status",
        "ssl-cipher",
        "ssl-protocol",
        "x-forwarded-for",
    }

    for line in log_file:
        values = line.decode("utf8").strip().split("\t")

        log_data = dict(zip(field_names, values))

        # Undo any URL-encoding in a couple of fields
        for name in url_encoded_fields:
            log_data[name] = urllib.parse.unquote(log_data[name])

        # Empty values in certain fields (e.g. ``sc-range-start``) are
        # represented by a dash; replace them with a proper empty type.
        for name, value in log_data.items():
            if name in nullable_fields and value == "-":
                log_data[name] = None

        # Convert a couple of numeric fields into proper numeric types,
        # rather than strings.
        for name, converter_function in numeric_fields.items():
            try:
                log_data[name] = converter_function(log_data[name])
            except ValueError:
                pass

        # Convert the date/time from strings to a proper datetime value.
        log_data["date"] = datetime.datetime.strptime(
            log_data.pop("date") + log_data.pop("time"),
            "%Y-%m-%d%H:%M:%S"
        )

        yield log_data
```

It generates a dictionary, one per log line.
The named values make it easy for me to inspect and use the log entries in my analysis code.
A couple of the values are converted to more meaningful types than strings -- for example, the `cs-bytes` field is counting the bytes, so it makes sense for it to be an `int` rather than a `str`.

This is how it gets used:

```python
for log_entry in parse_cloudfront_logs(log_file):
    print(log_entry)
    # {'c-ip': '1.2.3.4', 'c-port': '9962', 'cs-cookie': None, ...}
```

And then I can use my regular Python tools for analysing iterable data.
For example, if I wanted to count the most commonly-requested URIs in a log file:

```python
import collections

tally = collections.Counter(
    log_entry["cs-uri-stem"]
    for log_entry in parse_cloudfront_logs(log_file)
)

from pprint import pprint
pprint(tally.most_common(10))
```

CloudFront writes new log files a couple of times an hour.
Sometimes I want to look at a single log file if I'm debugging an event which occurred at a particular time, but other times I want to look at multiple files.
For that, I have a couple of additional functions which handle combining log entries from different files.

[logs]: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html
[Jupyter Notebook]: https://jupyter.org/

---

## Finding CloudFront logs on the local disk

If I'm going to be working offline or I know I'm going to be running lots of different bits of analysis on the same set of log files, sometimes I download the log fields directly to my local disk.
Then I use my [function for walking a file tree][snake-walker] to get a single iterator for all the entries in a folder full of log files:

```python
import gzip


def get_cloudfront_logs_from_dir(root):
    """
    Given a folder that contains CloudFront access logs, generate all
    the CloudFront log entries from all the log files.
    """
    for path in get_file_paths_under(root, suffix='.gz'):
        with gzip.open(path) as log_file:
            yield from parse_cloudfront_logs(log_file)


for log_entry in get_cloudfront_logs_from_dir("cf"):
    print(log_entry)
```

[snake-walker]: /2023/snake-walker/

---

## Finding CloudFront logs in S3

CloudFront logs are stored in S3, so if I'm running inside AWS, it can be faster and easier to read log files directly out of S3.
For this I have a function that lists all the S3 keys within a given prefix, then opens the individual objects and parses their log entries.
This gives me a single iterator for all the log entries in a given S3 prefix:

```python
import boto3
import gzip


def list_s3_objects(sess, **kwargs):
    """
    Given an S3 prefix, generate all the objects it contains.
    """
    s3 = sess.client("s3")

    for page in s3.get_paginator("list_objects_v2").paginate(**kwargs):
        yield from page.get("Contents", [])


def get_cloudfront_logs_from_s3(sess, *, Bucket, **kwargs):
    """
    Given an S3 prefix that contains CloudFront access logs, generate
    all the CloudFront log entries from all the log files.
    """
    s3 = sess.client("s3")
    
    for s3_obj in list_s3_objects(sess, Bucket=Bucket, **kwargs):
        Key = s3_obj["Key"]

        body = s3.get_object(Bucket=Bucket, Key=Key)["Body"]

        with gzip.open(body) as log_file:
            yield from parse_cloudfront_logs(log_file)


sess = boto3.Session()

for log_entry in get_cloudfront_logs_from_s3(
    sess,
    Bucket="wellcomecollection-api-cloudfront-logs",
    Prefix="api.wellcomecollection.org/",
):
    print(log_entry)
```

---

## Getting loop-y with my logs

A couple of years ago I watched Ned Batchelder's talk [Loop Like A Native], which is an amazing talk that I'd recommend to Python programmers of any skill level.
One of the key ideas I took from that is the idea of creating abstractions around iteration: rather than creating heavily nested `for` loops, use functions to work at higher levels of abstraction.

That's what I'm trying to do with these functions (and the one in my [previous post]) -- to abstract away the exact mechanics of finding and parsing the log files, and just get a stream of log events I can use like any other Python iterator.

I think the benefits of this abstraction will become apparent in another post I'm hoping to write soon, where I'll go through some of the analysis I'm actually doing with these logs.
The post will jump straight into a `for` loop of CloudFront log events, and it won't have to worry about exactly where those events come from.

[Loop Like A Native]: https://nedbatchelder.com/text/iter.html
[previous post]: /2023/snake-walker/
