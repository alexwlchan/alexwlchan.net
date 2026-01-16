---
layout: til
date: 2024-03-24 11:34:05 +00:00
title: Getting a boto3 Session for an IAM role using Python
summary: Why I use Sessions in boto3, and the Python function I use to create them.
tags:
  - python
  - aws
---
When I worked at Wellcome, I was doing a lot of work with AWS, and I was a frequent user of boto3, the Python SDK for AWS.
There were a lot of IAM roles, spread across multiple accounts, and I was writing Python scripts that would work with specific roles.

I was persuaded to use boto3 Sessions in [an article by Ben Kehoe](https://ben11kehoe.medium.com/boto3-sessions-and-why-you-should-use-them-9b094eb5ca8e).
Although most of my Python code was one-off scripts where there's not much difference, I thought it was a good habit to get into so I switched everywhere.
On the rare occasions I wrote Python in prod, I had the habit ingrained.

The following snippet became a common element in my scripts:

```python
import boto3


def get_aws_session(*, role_arn: str) -> boto3.Session:
    """
    Create a boto3 Session authenticated with the given IAM role ARN.
    """
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object["Credentials"]

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
```

Ben reviews this code in his article, and points out a couple of shortcomings: it's not so readable, and it doesn't handle credential expiry.
He has a library `aws-assume-role-lib` that he suggests using as an alternative.

I only used this snippet in one-off scripts.
For me, wrapping it in a function fixed the readability issue, and I wasn't concerned about expiring credentials.
At Wellcome, credentials would expire after 4 hours.
It was unusual for me to have scripts that ran longer than that, and when I did it wasn't too arduous to restart the script every so often.

In prod code, I'd just create the session directly:

```python
sess = boto3.Session()
```

and let the AWS environment work out how to retrieve credentials (e.g. if I was running in a Lambda function, I'd let it use the execution role).

I'm not currently using AWS for anything, so this code may get out of date.
