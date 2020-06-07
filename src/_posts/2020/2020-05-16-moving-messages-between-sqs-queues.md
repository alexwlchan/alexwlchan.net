---
layout: post
date: 2020-05-16 09:43:00 +0000
title: Moving messages between SQS queues
summary: You can send messages to a DLQ if they fail processing. What if you fix the bug, and you want to resend the failed messages?
category: Amazon Web Services
tags: aws amazon-sqs
---

At work, we make heavy use of [Amazon SQS](https://en.wikipedia.org/wiki/Amazon_Simple_Queue_Service) for message queues.
We write tasks to an SQS queue, and then a worker application reads the tasks from the queue and does some processing.
When the worker is done, it sends the message to another queue, where another worker can pick it up.
This is a classic microservices pattern.

<figure style="width: 600px;">
  {% inline_svg "_images/2020/sqs_queue_worker.svg" %}
</figure>

Sometimes a task can't be processed successfully -- for example, if there's a bug in the worker code.
You can [configure SQS][sqs_dlq] to send such problematic messages to a [dead-letter queue (DLQ)][dlq], where you can inspect them in isolation and work out what went wrong.

[sqs_dlq]: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
[dlq]: https://en.wikipedia.org/wiki/Dead_letter_queue

Once we've found the problem in the worker, fixed the bug and deployed a new version, we want to send all the messages from the DLQ back to the original input queue, so they can be processed by the updated worker.
There's no way to do this in SQS directly, so we've written a script to do it for us.
Although we primarily use this to redrive problematic messages that went to a DLQ, **this script allows you to move messages between an arbitrary pair of SQS queues**.

It uses code I shared two years ago [to dump the contents of an SQS queue][dump_q], the [send_message_batch() API][send_message_batch] in the boto3 SDK, and my snippet for [iterating in fixed-sized chunks][fixed_chunks].
Putting these three things together, you can move messages from one queue to another.

[dump_q]: /2018/01/downloading-sqs-queues/
[send_message_batch]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.send_message_batch
[fixed_chunks]: /2018/12/iterating-in-fixed-size-chunks/

Be careful running this code -- if the worker is running, and it picks up the messages immediately, they might go back to the DLQ if there's another problem with the worker.
The script would then resend them to the input queue, and the worker would send them back to the DLQ.
The messages would bounce back-and-forth forever.

Our queue-backed workers scale down to zero when the queue is empty, and they take a few minutes to start up when the queue starts filling.
Usually that's enough time for the script to finish running, so it's not an issue for us, but it is something to be aware of.

As with most of my scripts, this is written in Python.
You can [download the file](/files/2020/redrive_sqs_queue.py), or copy/paste the source code below.
Run it by passing the URL of the source and destination queue as arguments:

```
python3 redrive_sqs_queue.py \
    --src-url=https://sqs.amazonaws.com/123456789/my-queue-dlq \
    --dst-url=https://sqs.amazonaws.com/123456789/my-queue
```

Here's the code:

{% inline_code python _files/2020/redrive_sqs_queue.py %}
