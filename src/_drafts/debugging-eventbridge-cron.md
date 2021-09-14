---
layout: post
title: When is my EventBridge cron expression going to run next?
summary: The AWS console will tell you when your EventBridge rule is going to run… if you know where to look.
tags: aws amazon-eventbridge
---

Within AWS, you can use [EventBridge rules] to run something on a schedule.
For example, if you wanted to create daily reports, you could use an EventBridge rule to run a Lambda function that creates the report once a day.

There are two ways to specify an EventBridge rule: a [cron expression] or a rate expression.
You use cron expressions when you want fine-grained control over the schedule, but I find them tricky to reason about.
I'm not always sure if I've got a cron expression right, or when it's next going to run.

Today I stumbled upon a useful feature in the EventBridge console -- it'll tell you the next time your cron expression is going to run!

Suppose you're looking at a rule in the console:

<img src="/images/2021/eventbridge_rule_2x.png" srcset="/images/2021/eventbridge_rule_1x.png 1x, /images/2021/eventbridge_rule_2x.png 2x" style="width: 574px;" alt="A rule in the EventBridge console. It's titled 'run_costs_report', has a section titled 'Rule details', then a second section titled 'Event schedule' with the expression 'cron(0 8 ? * 3#2 *)'.">

If you click "Edit", and scroll down to the section titled "Define pattern", it'll show you the next 10 trigger dates when your cron expression will run:

<img src="/images/2021/eventbridge_trigger_dates_2x.png" srcset="/images/2021/eventbridge_trigger_dates_1x.png 1x, /images/2021/eventbridge_trigger_dates_2x.png 2x" style="width: 574px;" alt="A section in the AWS console titled 'Define pattern', with a text field for editing a cron expression and a list of the next 10 trigger dates at the bottom. There's a selection picker which is currently 'GMT'.">

As you edit your cron expression, the list updates to reflect your changes.
You can also choose whether the list shows times in GMT (UTC+0) or your local timezone.

I'd configured my rule in Terraform, so I hadn't looked at the console at all -- it was pure chance that I found this page.
It helped me debug an issue I was having, and much faster than if I'd used trial-and-error.
(I had an off-by-one bug, because I'd forgotten the UK isn't in GMT right now.)

I don't write many EventBridge rules so I don't know when I'll need this again, but it seems like something I'll want to remember.

[EventBridge rules]: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html
[cron expression]: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html#eb-cron-expressions
