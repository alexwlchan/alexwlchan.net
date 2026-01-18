---
layout: post
date: 2021-08-22 07:40:23 +00:00
title: Finding misconfigured or dangling CloudWatch Alarms
summary: A Python script that finds CloudWatch Alarms which are based on a now non-existent source.
tags:
  - aws
  - aws:amazon cloudwatch
  - python
colors:
  index_light: "#B0084D"
  index_dark:  "#f97bb0"
---

At work, we use a lot of [CloudWatch Alarms][alarms].
This allows you to monitor metrics from a variety of places, and take action when a metric hits some particular threshold.
For example:

-   Many of our apps are SQS-backed workers.
    We have alarms that monitor the SQS queue that feeds each app, and adds or removes instances based on the size of the queue.
-   We use [DynamoDB tables with autoscaling][dynamodb].
    That creates CloudWatch alarms that monitor the utilisation of the table, and match the provisioned capacity to current usage.
-   We have an alarm for [5XX errors from API Gateway][gateway].
    When we see too many errors within a minute, the alarm triggers [notifications in Slack][slack_alarms] so we know to investigate.

Earlier this week, I was looking through the CloudWatch console, and I found a bunch of alarms that were pulling metrics from non-existent sources.
It looks like we created a resource, created some CloudWatch alarms based on it, but when we deleted the resource the alarms stuck around.
Those alarms will never do anything, because the metrics they're based on will never change.

I wrote a Python script to find these dangling alarms, which you can copy/paste or [download below](/files/2021/find_dangling_cloudwatch_alarms.py).

After I ran my script, I was able to delete several hundred old alarms, three-quarters of the alarms in our account.
I was doing it to make it easier to review the alarms we are using, rather than to save money – but a small dent in the bill never goes amiss.

```python
#!/usr/bin/env python3
"""
Finds CloudWatch metric alarms that are pulling from a non-existent source,
e.g. an alarm that's based on the size of a now-deleted queue.

This script doesn't delete the alarm, it just warns you that the alarm
is never going to change in its current configuration.  You might want
to delete the alarm, or point it at a different source.

I've implemented checks for the Alarm sources that I use most often,
but CloudWatch Alarms can pull from other sources.  The script should be
extensible to other sources/namespaces if that's useful to you.

From https://alexwlchan.net/2021/08/finding-misconfigured-or-dangling-cloudwatch-alarms/

"""

import functools

import boto3
from botocore.exceptions import ClientError


def get_metric_alarm_descriptions(sess):
    resource = sess.resource("cloudwatch")
    client = sess.client("cloudwatch")

    for alarm in resource.alarms.all():
        resp = client.describe_alarms(AlarmNames=[alarm.name])
        yield from resp["MetricAlarms"]


# Note: often you'll have more than one alarm that reads from
# a given source (e.g. one alarm for table usage high and another
# for table usage low).
#
# There's no point doing repeated, successive checks for the existence
# of a table/queue/function/whatever, so cache the results here.


@functools.cache
def dynamodb_table_exists(sess, *, table_name):
    """
    Returns True if this DynamoDB table exists, False otherwise.
    """
    client = sess.client("dynamodb")

    try:
        client.describe_table(TableName=table_name)
        return True
    except ClientError as err:  # pragma: no cover
        if err.response["Error"]["Code"] == "ResourceNotFoundException":
            return False
        else:
            raise


@functools.cache
def sqs_queue_exists(sess, *, queue_name):
    """
    Returns True if this SQS queue exists, False otherwise.
    """
    client = sess.client("sqs")

    try:
        client.get_queue_url(QueueName=queue_name)
        return True
    except ClientError as err:  # pragma: no cover
        if err.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
            return False
        else:
            raise


@functools.cache
def lambda_function_exists(sess, *, function_name):
    """
    Returns True if this Lambda function exists, False otherwise.
    """
    client = sess.client("lambda")

    try:
        client.get_function(FunctionName=function_name)
        return True
    except ClientError as err:  # pragma: no cover
        if err.response["Error"]["Code"] == "ResourceNotFoundException":
            return False
        else:
            raise


if __name__ == "__main__":
    sess = boto3.Session()

    for alarm in get_metric_alarm_descriptions(sess):
        dimensions = {dim["Name"]: dim["Value"] for dim in alarm["Dimensions"]}

        # Is this alarm based on a non-existent table?
        if alarm.get("Namespace") == "AWS/DynamoDB":
            table_name = dimensions["TableName"]
            if not dynamodb_table_exists(sess, table_name=table_name):
                print(
                    f"!!! Alarm {alarm['AlarmArn']} is based on non-existent table {table_name}"
                )
            continue

        # Is this alarm based on a non-existent queue?
        if alarm.get("Namespace") == "AWS/SQS":
            queue_name = dimensions["QueueName"]
            if not sqs_queue_exists(sess, queue_name=queue_name):
                print(
                    f"!!! Alarm {alarm['AlarmArn']} is based on non-existent SQS queue {queue_name}"
                )
            continue

        # Is this alarm based on a non-existent Lambda function?
        if alarm.get("Namespace") == "AWS/Lambda":
            function_name = dimensions["FunctionName"]
            if not lambda_function_exists(sess, function_name=function_name):
                print(
                    f"!!! Alarm {alarm['AlarmArn']} is based on non-existent Lambda function {function_name}"
                )
            continue
```

[alarms]: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html
[dynamodb]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html
[gateway]: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html
[slack_alarms]: /2018/cloudwatch-alarms-in-slack/
