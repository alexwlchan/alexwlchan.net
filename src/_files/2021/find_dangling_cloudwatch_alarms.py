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
