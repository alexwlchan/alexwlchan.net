---
layout: post
date: 2023-07-03 13:43:19 +00:00
title: Turning off ECS tasks overnight using an EventBridge Schedule
summary: Calling the UpdateService API on a fixed schedule allows us to turn services off in the evening, and back on again the next morning.
tags:
  - aws:amazon ecs
  - aws:amazon-eventbridge
colors:
  css_light: "#9a255e"
  css_dark:  "#ff3d9c"
card_attribution: https://www.pexels.com/photo/analog-clock-sketch-in-black-surface-745365/
---

At work, we have a bunch of ECS services that run 24/7, even though they don't need to.
For example, we have a staging version of our website, where we test new changes before they're deployed to the live site.
We're only making changes during UK office hours, so running the staging site in evenings or on weekends is pointless.

I'd often thought about turning them off overnight, to save a bit of money, but I never quite got around to it.
I always imagined it would involve a bunch of moving pieces, possibly some Lambda functions we'd have to deploy and manage, and it all felt a bit too much effort.
Our bill isn't in a precarious place, and premature cost optimisation takes away from [better ways] to use our time.

Then I read [an article by Victor Ronin][ronin] about using Terraform to create schedules in EventBridge, which is much simpler than what I was expecting.
I tried rolling that pattern out to our ECS services, and it worked very well.

[better ways]: https://en.wikipedia.org/wiki/Opportunity_cost
[ronin]: https://aembit.io/blog/using-terraform-to-configure-aws-to-periodically-start-an-ec2-instance

---

The core logic sits in a pair of EventBridge Schedules, created with the `aws_scheduler_schedule` resource.
One schedule turns a service off in the evening; another turns it back on the next morning.

```hcl
resource "aws_scheduler_schedule" "turn_off_in_the_evening" {
  name       = "${var.service_name}-turn_off_in_the_evening"

  # This cron expression will run at 7pm UTC on weekdays.
  schedule_expression = "cron(0 19 ? * MON,TUE,WED,THUR,FRI *)"

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:ecs:updateService"
    role_arn = aws_iam_role.scheduler.arn

    input = jsonencode({
      Cluster      = var.cluster
      Service      = var.service_name
      DesiredCount = 0
    })
  }

  flexible_time_window {
    mode = "OFF"
  }
}

resource "aws_scheduler_schedule" "turn_on_in_the_morning" {
  name       = "${var.service_name}-turn_on_in_the_morning"

  # This cron expression will run at 7am UTC on weekdays.
  schedule_expression = "cron(0 7 ? * MON,TUE,WED,THUR,FRI *)"

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:ecs:updateService"
    role_arn = aws_iam_role.scheduler.arn

    input = jsonencode({
      Cluster      = var.cluster
      Service      = var.service_name
      DesiredCount = var.desired_task_count
    })
  }

  flexible_time_window {
    mode = "OFF"
  }
}

variable "cluster"            { type = string }
variable "service_name"       { type = string }
variable "desired_task_count" { type = number }
```

They're triggered on a schedule, according to the cron expression.
UK office hours are roughly 9 to 5, and the schedules are picked to include these hours plus a bit of "slop".
This is to account for people who work slightly earlier, slightly later, or when the UK timezone doesn't match UTC.

I do a lot of this sort of "slop" in scheduling code.
I'll accept a bit of inefficiency or redundancy if it means I can get simpler code.
I could tighten these schedules so they follow UK office hours more closely, but it would add a lot of complexity for marginal gains.
It's not worth it.

The most interesting bit to me is how the schedule updates the ECS service -- it calls the UpdateService API with a payload that I provide.
In this case I'm just changing the DesiredCount value, but it seems like this could be used to call other AWS APIs.
That feels like it has a lot of potential elsewhere.

We've already got a variant of these schedules that turns an EC2 instance off/on outside our working hours, and I imagine this won't be the last time I play with EventBridge Schedules.

---

Alongside the two schedules, you need an IAM role that allows EventBridge to modify your ECS services when it runs.
This is how our IAM role is defined:

```hcl
resource "aws_iam_role" "scheduler" {
  name               = "${var.service_name}-office-hours-scaling"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "allow_update_service" {
  statement {
    actions = ["ecs:UpdateService"]

    resources = [var.service_arn]
  }
}

resource "aws_iam_role_policy" "allow_update_service" {
  role   = aws_iam_role.scheduler.name
  policy = data.aws_iam_policy_document.allow_update_service.json
}

variable "service_arn"  { type = string }
variable "service_name" { type = string }
```

This is pretty standard IAM – create the role, and allow the EventBridge Scheduler service to assume it.
Then we create an IAM policy document that allows calling the UpdateService API for the service we're turning off/on, and we attach that policy document to the role.

---

This isn't a lot of Terraform, but it would be annoying to copy/paste this for every service we have.
To save ourselves the hassle, it's included it in our standard ECS service module, and services can opt-in to this behaviour with a single flag:

```hcl
module "service" {
   source = "git::github.com/wellcomecollection/terraform-aws-ecs-service.git//modules/service?ref=v3.15.3"
   name   = "staging-site"
   …
   turn_off_outside_office_hours = true
 }
```

Partly this is for readability, but mostly it's to make this behaviour quick and easy to enable -- which means we're more likely to actually do it.

We've already rolled this out to a dozen existing services, and there's a nice dent in last month's EC2 bill.
As we build out new services, I expect this behaviour to spread ever further.
