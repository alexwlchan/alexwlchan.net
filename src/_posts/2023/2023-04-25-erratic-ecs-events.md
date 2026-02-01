---
layout: post
date: 2023-04-25 13:40:02 +00:00
title: Getting alerts about flaky ECS tasks in Slack
summary: |
  When ECS is "unable to consistently start tasks successfully", we get a Slack alert that tells us to investigate.
tags:
  - aws:amazon ecs
  - aws
  - slack
colors:
  index_light: "#b24c0e"
  index_dark:  "#e7862a"
card_attribution: https://pixabay.com/photos/light-bulb-incandescent-smoke-crack-503881/
---

At work, we use [Amazon ECS] to run some of our Docker-based services.
ECS is a container orchestrator, similar to Kubernetes: we tell it what Docker images we want to run in what configuration, and it stops or starts containers to match.
If a container stops unexpectedly, ECS starts new containers automatically to replace it.

Occasionally, we see "unable to consistently start tasks successfully" messages in the "Deployments and events" tab of the ECS console:

{%
  picture
  filename="ecs_events_not_starting.png"
  alt="A table of events in the ECS service console. Three of the five events shown have the message 'service image_inferrer is unable to consistently start tasks successfully. For more information, see the Troubleshooting section of the Amazon ECS Developer Guide.'"
  width="697"
  class="screenshot"
%}

This has always been a mistake that we've made -- maybe we've introduced a bug that crashes the container, we're trying to launch a non-existent container, or we've messed up the ever-fiddly IAM permissions.
Whatever it is, we need to investigate.

So we know when to investigate, we've set up an alerting system that tells us in Slack whenever ECS is struggling to start tasks:

{%
  picture
  filename="ecs_slack_alert.png"
  alt="An alert in Slack with the message 'image_inferrer is unable to consistently start tasks successfully' with a clickable link 'View in console'. The alert has a red border and a siren emoji."
  width="667"
  class="screenshot"
%}

The alert tells us the name of the affected ECS cluster and service, and includes a link to the relevant part of the AWS console.
We include clickable links in a lot of our Slack alerts, to make it as easy as possible to start debugging.

This is what it looks like under the hood:

<figure>
{%
  inline_svg
  filename="ecs_slack_alert_pipeline.svg"
  alt="An architecture diagram representing the flow of data. On the left is the ECS service, with an arrow labelled 'all events' pointing to CloudWatch rule. From the rule is another arrow '“can’t start tasks” events only' pointing to the Lambda function, which in turn points to the Slack channel."
  class="wide_img dark_aware"
%}
</figure>

ECS publishes a [stream of events][events] to CloudWatch Events, and within CloudWatch we're filtering for the *"unable to consistently start tasks successfully"* events.
In particular, we've got an [event pattern] that looks for the `SERVICE_TASK_START_IMPAIRED` event name.

Any matching events trigger a Lambda function, which extracts the key information from the event, gets a [Slack webhook URL] from Secrets Manager, then posts a message to Slack.
This is a standard pattern for alerting Lambdas that we've used multiple times.

If you're interested, all the code for this setup is publicly available under an MIT licence.
Both the [Terraform definitions] and [Lambda source code] are in our platform-infrastructure repo.

And now if you'll excuse me, there's an ECS task that needs my attention…

[Amazon ECS]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
[events]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwe_events.html#ecs_service_events_warn_type
[event pattern]: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
[Slack webhook URL]: https://api.slack.com/messaging/webhooks
[Terraform definitions]: https://github.com/wellcomecollection/platform-infrastructure/tree/main/monitoring/terraform/modules/slack_alert_on_ecs_tasks_not_starting
[Lambda source code]: https://github.com/wellcomecollection/platform-infrastructure/blob/main/monitoring/slack_alerts/ecs_tasks_cant_start_alert/src/ecs_tasks_cant_start_alert.py
