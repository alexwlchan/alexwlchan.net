---
layout: til
title: Using Linode object storage and boto3
summary: If you're calling `put_object`, you need the config option `request_checksum_calculation = "when_required"`.
date: 2025-07-23 15:46:49 +01:00
tags:
  - linode
  - python
  - python:boto3
---
I'm using [Linode object storage](https://www.linode.com/products/object-storage/), which has an S3-compatible API, so it should work with any existing AWS libraries.
In particular, I'm [using boto3](https://techdocs.akamai.com/cloud-computing/docs/using-the-aws-sdk-for-python-boto3-with-object-storage).

I did have to add a couple of settings to get everything working -- here are some code examples.

## Uploading a file

You need to add `request_checksum_calculation` is you're uploading files:

```python
import boto3  # pip install boto3==1.38.19
from botocore.config import Config

ACCESS_KEY = 'JJO…'
SECRET_KEY = 'eji…'

s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
    config=Config(request_checksum_calculation="when_required"),
)

s3_client.put_object(
    Bucket="example-bucket",
    Key="greeting.txt",
    Body=b"Hello world!",
)

s3_client.upload_file(
    Filename="greeting.txt",
    Bucket="example-bucket",
    Key="greeting.txt"
)
```

If you don't add the setting, you get an error when trying to do the PutObject operation:

> botocore.exceptions.ClientError: An error occurred (XAmzContentSHA256Mismatch) when calling the PutObject operation: None

## Downloading files

There is an equivalent setting `response_checksum_validation`, but I don't seem to need it for downloading files:

```python
s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
)

s3_client.get_object(
    Bucket="example-bucket",
    Key="greeting.txt"
)

s3_client.download_file(
    Bucket="example-bucket",
    Key="greeting.txt",
    Filename="greeting.txt",
)

s3_client.generate_presigned_url(
    "get_object",
    Params={"Bucket": "example-bucket", "Key": "greeting.txt"}
)
```

## Other operations

Other operations likewise work fine with the standard settings:

```python
s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
)

s3_client.delete_object(
    Bucket="flickr-foundation-data-lifeboat-zips",
    Key="README.md"
)

s3_client.list_objects_v2(
    Bucket="flickr-foundation-data-lifeboat-zips"
)
```
