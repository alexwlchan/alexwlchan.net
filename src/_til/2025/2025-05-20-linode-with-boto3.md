---
layout: til
title: Using Linode object storage and boto3
summary: If you're doing `get_object` or `put_object` calls, you need a couple of extra config flags.
date: 2025-05-20 12:49:59 +0100
tags:
  - linode
  - python
---
```python
access_key = 'JJO…'
secret_key = 'eji…'

import boto3  # pip install boto3==1.38.19
from botocore.config import Config

s3_client = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
    config=Config(request_checksum_calculation="when_required"),
)

s3_client.upload_file(
    Filename="README.md",
    Bucket="flickr-foundation-data-lifeboat-zips",
    Key="README.md"
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
    config=Config(response_checksum_validation="when_required"),
)

s3_client.download_file(
    Filename="README.md",
    Bucket="flickr-foundation-data-lifeboat-zips",
    Key="README.md"
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
    config=Config(),
)

s3_client.generate_presigned_url(
    "get_object",
    Params={
        "Bucket": "flickr-foundation-data-lifeboat-zips",
        "Key": "README.md",
    },
    ExpiresIn=3600,
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url="https://gb-lon-1.linodeobjects.com",
    config=Config(),
)

s3_client.delete_object(
    Bucket="flickr-foundation-data-lifeboat-zips",
    Key="README.md"
)

s3_client.list_objects_v2(
    Bucket="flickr-foundation-data-lifeboat-zips"
)
```