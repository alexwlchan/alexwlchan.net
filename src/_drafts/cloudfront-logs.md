---
layout: post
title: Parsing CloudFront logs with Python
summary: A couple of functions I use to get access to CloudFront logs in a Pythonic way.
tags: python aws amazon-cloudfront
colors:
  css_light: "#673ABB"
  css_dark:  "#C9ABFF"
---

I've been doing work recently to analyse some [CloudFront access logs][logs].
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
        "time-taken": float,
        "time-to-first-byte": float,
    }
    
    url_encoded_fields = {
        "cs-uri-stem",
        "cs-uri-query",
    }

    nullable_fields = {
        "cs(Cookie)",
        "cs-uri-query",
        "fle-encrypted-fields",
        "fle-status",
        "sc-range-end",
        "sc-range-start",
        "ssl-cipher",
        "ssl-protocol",
        "x-forwarded-for",
    }

    for line in log_file:
        values = line.decode("utf8").strip().split("\t")

        log_data = dict(zip(field_names, values))

        # Convert a couple of numeric fields into proper numeric types,
        # rather than strings.
        for name, converter_function in numeric_fields.items():
            try:
                log_data[name] = converter_function(log_data[name])
            except ValueError:
                pass

        # Undo any URL-encoding in a couple of fields
        for name in url_encoded_fields:
            log_data[name] = urllib.parse.unquote(log_data[name])

        # Empty values in certain fields (e.g. ``sc-range-start``) are
        # represented by a dash; replace them with a proper empty type.
        for name, value in log_data.items():
            if name in nullable_fields and value == "-":
                log_data[name] = None

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

---

## Finding CloudFront logs on the local disk

If I'm going to be working offline or I know I'm going to be running lots of different bits of analysis on the same set of log files, sometimes I download the log fields directly to my local disk.
Then I use my [function for walking a file tree][snake-walker]

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

[snake-walker]: {% post_url 2023/2023-07-26-snake-walker %}

```python
{'c-ip': '1.2.3.4',
 'c-port': '9962',
 'cs(Cookie)': '-',
 'cs(Host)': 'dm4ob5gaol1gg.cloudfront.net',
 'cs(Referer)': '-',
 'cs(User-Agent)': 'python-requests/2.25.1',
 'cs-bytes': 233,
 'cs-method': 'GET',
 'cs-protocol': 'https',
 'cs-protocol-version': 'HTTP/1.1',
 'cs-uri-query': 'cacheBust=34da0c36-13b5-11ee-83e2-0242ac101002',
 'cs-uri-stem': '/storage/v1/context.json',
 'date': '2023-06-26',
 'fle-encrypted-fields': '-',
 'fle-status': '-',
 'sc-bytes': 618,
 'sc-content-len': 136,
 'sc-content-type': 'application/json',
 'sc-range-end': '-',
 'sc-range-start': '-',
 'sc-status': '403',
 'ssl-cipher': 'TLS_AES_128_GCM_SHA256',
 'ssl-protocol': 'TLSv1.3',
 'time': '00:05:49',
 'time-taken': 0.066,
 'time-to-first-byte': 0.066,
 'x-edge-detailed-result-type': 'Error',
 'x-edge-location': 'DUB2-C1',
 'x-edge-request-id': '7Yt7csr_PC5X_OVwA6LT3H2eVcxaMUvOInbSgCRlkk4NN8EpvBuLOg==',
 'x-edge-response-result-type': 'Error',
 'x-edge-result-type': 'Error',
 'x-forwarded-for': '-',
 'x-host-header': 'api-stage.wellcomecollection.org'}
```

```python
#!/usr/bin/env python3

import gzip
import sys
2
import boto3
import hyperlink


def get_cloudfront_logs(sess, *, bucket, key):
    s3 = sess.client('s3')

    with gzip.open(s3.get_object(Bucket=bucket, Key=key)['Body']) as logfile:

        # The first line is a version header, e.g.
        #
        #     b'#Version: 1.0\n'
        #
        next(logfile)

        # The second line tells us what the fields are, e.g.
        #
        #     b'#Fields: date time x-edge-location …\n'
        #
        fields = [f.strip() for f in next(logfile).replace(b'#Fields:', b'').split()]

        for line in logfile:

            try:
                line['sc-bytes'] = int(line['sc-bytes'])
            except ValueError:
                pass

            try:
                line['cs-bytes'] = int(line['cs-bytes'])
            except ValueError:
                pass

            try:
                line['time-taken'] = float(line['time-taken'])
            except ValueError:
                pass

            try:
                line['time-to-first-byte'] = float(line['time-to-first-byte'])
            except ValueError:
                pass

            yield dict(zip(fields, line.strip().split()))


if __name__ == '__main__':
    try:
        cf_logs_url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <CLOUDFRONT_LOGS_URL>")

    url = hyperlink.URL.from_text(cf_logs_url)
    bucket = url.host
    key = '/'.join(url.path)

    sess = boto3.Session()

    import collections

    tally = collections.Counter(
        hit[b'c-ip']
        for hit in get_cloudfront_logs(sess, bucket=bucket, key=key)
    )

    from pprint import pprint
    pprint(tally.most_common(10))
```