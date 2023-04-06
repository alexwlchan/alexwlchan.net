---
layout: post
title: Getting alerts about flaky ECS tasks in Slack
summary:
tags:
---

At work, we use [Amazon ECS] to run some of our Docker-based services.
ECS is a container orchestrator, similar to Kubernetes: we tell it what Docker images we want to run in what configuration, and it stops or starts containers to match.
If a container stops unexpectedly, ECS starts new containers automatically to replace it.

Occasionally, we see "unable to consistently start tasks successfully" messages in the "Deployments and events" tab of the ECS console:

<img src="Screenshot 2023-04-05 at 10.07.33.png">

This has always been our mistake -- maybe we've introduced a bug that crashes the container, we're trying to launch a non-existent container, or we've messed up the ever-fiddly IAM permissions.
Whatever it is, we need to investigate.

So we know when to investigate, we've set up an alerting system that tells us in Slack whenever ECS is struggling to start tasks:

[example alert]

In this post, I'll explain how I've set up these alerts.

---

This is the basic architecture:

[architecture]

We send all our ECS events to a CloudWatch Rule, which filters for "task stopped events".
Those events go to a custom Lambda via an SNS topic, and the Lambda creates the message which is posted in Slack.
Let's step through the pieces in turn.

## step 1: set up an eventbridge rule / ecs to sns

eventbridge rule
why sns?
because we already have lots of sns-triggered lambdas
can probably trigger lambda directly

## step 2: get interesting info from lambda payload

example

## step 3: post to slack

get slack webhook from secrets manager
post to slack
includes link to console for easy debugging


---

Occasionally, we change something and ECS struggles to start new containers.
Maybe we've written a crashing bug in the code that runs on first run,

maybe there's a crashing bug in our startup code, or the container is trying to pull resources

