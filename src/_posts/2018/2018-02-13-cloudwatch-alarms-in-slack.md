---
layout: post
date: 2018-02-13T11:36:50.494Z
title: Getting helpful CloudWatch alarms in Slack
summary: How we use AWS Lambda to send messages about our CloudWatch alarms to Slack, and some ways we add context and information to make those messages as helpful as possible.
canonical_url: https://stacks.wellcomecollection.org/getting-helpful-cloudwatch-alarms-in-slack-ba98fcbe6d31
tags:
  - wellcome collection
  - slack
---
*I wrote this article while I was working at Wellcome Collection. It was originally published [on their Stacks blog](https://stacks.wellcomecollection.org/getting-helpful-cloudwatch-alarms-in-slack-ba98fcbe6d31) under a CC BY 4.0 license, and is reposted here in accordance with that license.*

<p>In the <a href="https://wellcomecollection.org/sites/default/files/Wellcome%20Collection%20Who%20we%20are%20and%20what%20we%20do.pdf">digital platform team</a>, we make heavy use of Slack for our monitoring. As soon as something goes wrong, we get a message telling us about the problem. Here’s an example:</p>

{%
  picture
  filename="1*eyLFQ0VhA2Z-9tFoI5W39Q.png"
  width="648"
  alt=""
%}

<p>Real-time messages in Slack let us react quickly to errors. In this post, I’ll explain how these alarms work, and some work we’ve done to make them as helpful as possible.</p>

<h2>Architecture</h2>

{%
  picture
  filename="1*_ulsaWF4LAmK0C30ziJWwA.png"
  width="750"
  alt=""
%}

<p>All our logging and monitoring is handled by CloudWatch. We have <a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Metric">CloudWatch metrics</a> that measure the state of our deployment — for example, the number of messages on each queue, or the 500 errors returned from our applications.</p><p>For important metrics, we create <a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#CloudWatchAlarms">CloudWatch alarms</a> that trigger whenever a metric crosses a defined threshold — for example, when a dead-letter queue has a non-zero number of messages. When an alarm triggers, we have CloudWatch send a notification to an SNS topic.</p><p>All our alarms send notifications to the same topic, which in turn triggers a Post to Slack Lambda. This is a Python function that reads the notification, and calls the Slack API to post a message to an internal Slack channel.</p>

<h2>Creating richer alarms</h2>

<p>The SNS notification includes the alarm name and the state reason (why was the threshold crossed). We can expose those for a basic alarm, but it’s not always obvious what the alarm means:</p>

{%
  picture
  filename="1*mrV13JqHGocG0E6QvAIEBA.png"
  width="648"
  alt=""
%}

<p>We’ve made a number of changes to our Post to Slack Lambda to improve on the basic alarm, so we get more context and more helpful messages in Slack.</p>

<h3>Threshold Crossed: 1 sentence was less than clear</h3>

<p>The state reason explains why the alarm was triggered, for example:</p><blockquote><p><strong>id_minter-alb-unhealthy-hosts<br></strong>Threshold Crossed: 1 datapoint [3.0 (05/02/18 14:34:00)] was greater than or equal to the threshold (1.0).</p></blockquote><p>This message is describing the internals of CloudWatch — but what does it actually mean? It only makes sense if you know what the underlying CloudWatch metric is measuring.</p><p>Because the state reason follows a standard pattern, we can parse it to get the useful information, and then try to replace it with something more human-friendly. Some examples:</p><blockquote><p>There are 2 unhealthy targets in the transformer ALB target group.</p><p>There was an error in the notify_old_deploys Lambda.</p><p>There are 2 items on the sierra_items_windows DLQ.</p><p>There were multiple 500 errors (4) from the grafana ALB target group.</p></blockquote><p>These messages are shorter, so they’re more likely to be read, and they give more context than the default message.</p><p>The logic that picks these sentences relies on our alarm names following a consistent naming scheme — for example, every DLQ metric is named <em>queue_name_dlq_not_empty</em>. We manage our entire deployment using Terraform, and this consistency is a nice side benefit.</p>

<h3>Not all alarms are equally severe</h3>

<p>Some alarms need a faster response than others. The public-facing API is down? Let’s fix that immediately. An assertion in an internal service? We’ll fix that too, but it doesn’t have to be right now.</p><p>To make our urgent alarms stand out, we have two levels of message: “error” and “warning”. Our Lambda decides a level for each alarm, and formats it accordingly. These are examples of the two formats:</p>

{%
  picture
  filename="1*paMF34mV4WYuiwYclvvevw.png"
  width="648"
  alt=""
%}

<p>
{%
  picture
  filename="1*mrV13JqHGocG0E6QvAIEBA.png"
  width="648"
  alt=""
%}
</p>

<p>So if we’re having a bad day, we can easily pick out the most important alarms.</p><p>Additionally, we have two channels: our main team channel gets any critical errors for public-facing services, and a side channel gets warnings for everything else. We have to be disciplined about checking the side channel, but we’ve found this is a good way to reduce noise in our main channel, and it makes important errors stand out even more.</p>

<h3>Links to CloudWatch logs</h3>

<p>These alarms are good, but they’re a bit passive. There’s no call to action. Once an alarm fires, what should we do next? A common starting point is to check the logs — and we can help there too.</p><p>When an application has an error, there are key phrases that we know to look for. In a Python Lambda, errors are usually accompanied by <em>“Traceback” </em>or <em>“Task timed out”. </em>In our Scala services, <em>“HTTP 500” </em>is a good phrase to search for.</p><p>We can work out the CloudWatch log group name from the alarm name (because they both follow consistent naming conventions, thanks to Terraform). We know roughly when the error occured from the alarm message, and together with the search terms we can build a link to the CloudWatch web console.</p><p>For example, here’s a link that searches for <em>“HTTP 500” </em>in the <em>“platform/api_romulus_v1” </em>log group at around noon:</p><p><a href="https://eu-west-1.console.aws.amazon.com/cloudwatch/home?region=eu-west-1#logEventViewer:group=platform/api_romulus_v1;filter=%22HTTP%20500%22;start=2018-02-02T11:55:00Z;end=2018-02-02T12:05:00Z"><em>https://eu-west-1.console.aws.amazon.com/cloudwatch/home?region=eu-west-1#logEventViewer:group=platform/api_romulus_v1;filter=%22HTTP%20500%22;start=2018-02-02T11:55:00Z;end=2018-02-02T12:05:00Z</em></a></p><p>So if we know some search terms to try, our Lambda includes a link to some hopefully useful logs:</p>

{%
  picture
  filename="1*A6E-cT-NO8fjzh0EHbQOBQ.png"
  width="648"
  alt=""
%}

<p>To reduce visual noise, we use bit.ly to shorten the links.</p><p>So now our alarm has a call to action: an error occurred, now click here to read the logs.</p>

<h3>Inline CloudWatch logs</h3>

<p>When you look at the CloudWatch web console, it’s using the FilterCloudWatchEvents API under the hood to find matching log events. Why not do that in our Lambda?</p><p>So as well as posting the URL, our Lambda does a quick search of the logs, and includes anything that looks interesting in the Slack alarm. This isn’t perfect — if there’s a lot of logging, it may give up before it finds the relevant line — but when it works, it can be really helpful. Here’s another example:</p>

{%
  picture
  filename="1*D8c0qeNLWoHsam8OjKfQuQ.png"
  width="648"
  alt=""
%}

<p>So now we get an alarm, we see which application went wrong, and we can see the cause of the bug without even leaving Slack. (This Lambda makes several network calls, and we’ve just been unlucky and hit the default timeout. The fix is to <a href="https://github.com/wellcometrust/platform/commit/0d862c17f4f88676621cb3b7ed0547ca6e1d4908">raise the timeout</a>, which I did as soon as I left Slack.)</p>

<h2>Try it yourself!</h2><p>These alarms aren’t a fixed target — we’re often tweaking them to make them more useful. There’s no “right” way to format these alarms, but there are ways to make them more helpful.</p><p>All the code that builds these alarms is on GitHub, and MIT-licensed. The main Lambda code is in <a href="https://github.com/wellcometrust/platform/blob/master/monitoring/post_to_slack/src/post_to_slack.py">post_to_slack.py</a>, and some Platform logic lives in separate files.</p><p>Some of this is specific to our deployment, but the ideas could apply to any setup. If you use Slack for monitoring, I’d encourage you to think about humanising your alarms. We’ve found it makes them significantly more helpful, and that means errors get fixed that much quicker!</p>
