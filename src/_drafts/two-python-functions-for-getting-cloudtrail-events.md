---
layout: post
title: Two Python functions for getting CloudTrail events
tags: aws aws-cloudtrail
---

Last week I was trying to debug an anomaly in the AWS account at work -- it looked like we were making tens of millions of GetObject API calls, when we expected our code to make a fraction of that number.
According to Cost Explorer, the majority of our bill for several days last month was GetObject-related -- why?

To help debug the problem, I enabled logging of account activity with [CloudTrail](https://aws.amazon.com/cloudtrail/).
This is a service designed for audit and governance: it can log every AWS API call that happens in an account, so you can see exactly who did what, and when.
By analysing the CloudTrail logs, I was hoping to see where all these GetObject calls were coming from.
Which application was at fault?

Each API call is a single CloudTrail event, which includes lots of information:

{% details %}
<summary>Example CloudTrail event for a HeadObject call</summary>

```json
{
  "additionalEventData": {
    "AuthenticationMethod": "AuthHeader",
    "CipherSuite": "ECDHE-RSA-AES128-GCM-SHA256",
    "SignatureVersion": "SigV4",
    "bytesTransferredIn": 0.0,
    "bytesTransferredOut": 0.0,
    "x-amz-id-2": "uPZKeSBqZ+u8Ob2LNwWXu5qZLj4hPOyrb8MuZRIP01KnRlh4qR9KRuyBzF2qSKTvm4FjepBw5s8="
  },
  "awsRegion": "eu-west-1",
  "eventCategory": "Data",
  "eventID": "bb96b75f-0047-4907-ae51-4e86f81bf71e",
  "eventName": "HeadObject",
  "eventSource": "s3.amazonaws.com",
  "eventTime": "2020-08-29T23:53:21Z",
  "eventType": "AwsApiCall",
  "eventVersion": "1.07",
  "managementEvent": false,
  "readOnly": true,
  "recipientAccountId": "975596993436",
  "requestID": "0970D894699EDB33",
  "requestParameters": {
    "Host": "wellcomecollection-storage.s3.eu-west-1.amazonaws.com",
    "bucketName": "wellcomecollection-storage",
    "key": "digitised/b29325493/v1/data/objects/b29325493_0003_0315.jp2"
  },
  "resources": [
    {
      "ARN": "arn:aws:s3:::wellcomecollection-storage/digitised/b29325493/v1/data/objects/b29325493_0003_0315.jp2",
      "type": "AWS::S3::Object"
    },
    {
      "ARN": "arn:aws:s3:::wellcomecollection-storage",
      "accountId": "975596993436",
      "type": "AWS::S3::Bucket"
    }
  ],
  "responseElements": null,
  "sourceIPAddress": "172.30.209.10",
  "userAgent": "[aws-sdk-java/1.11.504 Linux/4.14.186-146.268.amzn2.x86_64 OpenJDK_64-Bit_Server_VM/11.0.2+9-Debian-3bpo91 java/11.0.2 scala/2.12.10 exec-env/AWS_ECS_FARGATE]",
  "userIdentity": {
    "accessKeyId": "ASIA6GJQ4XOOE447BROR",
    "accountId": "975596993436",
    "arn": "arn:aws:sts::975596993436:assumed-role/storage-prod-bag-replicator_azure_task_role/99c28596f91341839c1d07da27b65fe2",
    "principalId": "AROA6GJQ4XOOHQZQZM5FX:99c28596f91341839c1d07da27b65fe2",
    "sessionContext": {
      "attributes": {
        "creationDate": "2020-08-29T21:56:45Z",
        "mfaAuthenticated": "false"
      },
      "sessionIssuer": {
        "accountId": "975596993436",
        "arn": "arn:aws:iam::975596993436:role/storage-prod-bag-replicator_azure_task_role",
        "principalId": "AROA6GJQ4XOOHQZQZM5FX",
        "type": "Role",
        "userName": "storage-prod-bag-replicator_azure_task_role"
      }
    },
    "type": "AssumedRole"
  },
  "vpcEndpointId": "vpce-0d4aa186edac65a21"
}
```
{% enddetails %}

CloudTrail events can be written to objects in an S3 bucket, and they typically appear within 15 minutes of the API call.
The logs are written as gzip-compressed JSON files, with all the events for the 15 minute period in one file.

There are lots of tools for parsing CloudTrail logs, including big data tools like Amazon Athena.
If I was doing full-time CloudTrail analysis, it'd be worth taking the time to learn proper tools, but for a one-off investigation I decided to use the tools I already know: Python and Jupyter Notebook.

I wrote a couple of Python functions to parse these files, and emit individual events.
First, a function for getting logs directly from S3:

```python
import gzip
import json

import boto3


def get_cloudtrail_events_from_s3(s3_client=None, *, bucket, prefix):
    """
    Generate CloudTrail events from log files stored in S3.
    """
    if s3_client is None:
        s3_client = boto3.client("s3")

    paginator = s3_client.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for list_result in page["Contents"]:
            s3_key = list_result["Key"]

            if not s3_key.endswith(".json.gz"):
                continue

            s3_obj = s3_client.get_object(Bucket=bucket, Key=s3_key)

            with gzip.open(s3_obj["Body"]) as infile:
                records = json.load(infile)
                yield from records["Records"]
```

This is good for doing quick experiments.

To analyse the entire set, I downloaded the logs bucket to a local folder with `aws s3 sync`, and I wrote a second function that gets the events from the logs in the folder.
This saved me having to redownload the complete log set from S3 every time.

```python
import gzip
import json
import os


def get_cloudtrail_events_from_fs(root):
    """
    Generate CloudTrail events from log files stored locally.
    """
    for dirpath, _, filenames in os.walk(root):
        for f in sorted(filenames):
            if not f.endswith(".json.gz"):
                continue

            path = os.path.join(dirpath, f)

            with gzip.open(path) as infile:
                records = json.load(infile)
                yield from records["Records"]
```

Both of these functions generate individual events, so calling code doesn't have to worry about the exact format of the log files, or the underlying 15 minute periods.
They both worked well, and allowed me to do some analysis to find out how many GetObject calls we were actually making.

For example, I was able to use the [collections module](https://docs.python.org/3/library/collections.html) to find the most common API calls on a particular day:

```python
import collections
import pprint

event_names = collections.Counter()

for event in get_cloudtrail_events_from_fs(root="cloudtrail_logs/08/30"):
    event_names[(event["eventSource"], event["eventName"])] += 1

pprint(event_names.most_common(5))
```

```
[(('s3.amazonaws.com', 'HeadObject'), 8757667),
 (('s3.amazonaws.com', 'GetObject'), 3077835),
 (('s3.amazonaws.com', 'GetObjectTagging'), 101949),
 (('s3.amazonaws.com', 'ListObjects'), 22941),
 (('s3.amazonaws.com', 'PutObject'), 7738)]
```

Notice that while there are millions of GetObject API calls, there aren't tens of millions.

This was a useful clue -- it turns out that although Cost Explorer was attributing hundreds of dollars to GetObject-related spending, it wasn't just the cost of GetObject API calls.
Looking at the bill more closely, I realised that GetObject cost was the API call *and the external data transfer costs*.
I was expecting to see that as a separate entry in Cost Explorer, but apparently not.

I don't know if/when I'll be using CloudTrail again -- this particular problem now resolved, I've turned off the S3 logging -- but I have written these functions several times now, so I'm keeping them for future reference.
