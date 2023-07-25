---
layout: post
title: A Python function for parsing CloudFront logs
summary: 
tags: python aws amazon-cloudfront
---

#!/usr/bin/env python3

import gzip
import sys

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
