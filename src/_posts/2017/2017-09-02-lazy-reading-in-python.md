---
layout: post
date: 2017-09-02 17:34:00 +0000
link: https://github.com/alexwlchan/lazyreader
summary: I wrote a small Python module for lazy file reading, ideal for efficient
  batch processing.
tags: python
title: A Python module for lazy reading of file objects
category: Programming and code
---

At work, we often pass data around via large files kept in Amazon S3 -- XML exports from legacy applications, large log files, JSON dumps of Elasticsearch indexes -- that sort of thing.
The services that deal with these files run in Docker containers on AWS, and they have limited memory and local storage.

Downloading large files into memory is slow, expensive, and often unnecessary.
Many of these files contain a list of records, which we want to process one-at-a-time.
We only need to hold a single record in memory at a time, not the whole file.

Python can do efficient line-by-line processing of local files.
The following code only reads a line at a time:

```python
with open('very-long-file.txt') as f:
    for line in f:
        do_stuff_with(line)
```

This is more efficient, and usually results in faster code -- but you can only do this for local files, and the only delimiter is a newline.
You need a different wrapper if you want to do this for files in S3, or use a different delimiter -- and that's what this module does.
It goes like this:

```python
import boto3
from lazyreader import lazyread

s3 = boto3.client('s3')
s3_object = client.get_object(Bucket='example-bucket', Key='records.txt')
body = s3_object['Body']

for doc in lazyread(body, delimiter=b';'):
    print(doc)
```

The code isn't especially complicated, just a little fiddly, but I think it's a useful standalone component.

I was mildly surprised that something like this doesn't already exist, or if it does, I couldn't find the right search terms!
If you know an existing module that does this, please let me know.

You can install lazyreader from PyPI (`pip install lazyreader`), or see the README for more details.
