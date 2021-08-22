---
layout: post
date: 2021-08-22 07:40:23 +0000
title: Finding misconfigured or dangling CloudWatch Alarms
summary: A Python script that finds CloudWatch Alarms which are based on a now non-existent source.
tags: amazon-cloudwatch python
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

{% inline_code python _files/2021/find_dangling_cloudwatch_alarms.py %}

[alarms]: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html
[dynamodb]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html
[gateway]: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html
[slack_alarms]: https://stacks.wellcomecollection.org/getting-helpful-cloudwatch-alarms-in-slack-ba98fcbe6d31
