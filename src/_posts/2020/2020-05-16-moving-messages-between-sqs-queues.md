---
layout: post
date: 2020-05-16 09:43:00 +00:00
title: Moving messages between SQS queues
summary: You can send messages to a DLQ if they fail processing. What if you fix the bug, and you want to resend the failed messages?
tags:
  - aws
  - aws:amazon sqs
---

At work, we make heavy use of [Amazon SQS](https://en.wikipedia.org/wiki/Amazon_Simple_Queue_Service) for message queues.
We write tasks to an SQS queue, and then a worker application reads the tasks from the queue and does some processing.
When the worker is done, it sends the message to another queue, where another worker can pick it up.
This is a classic microservices pattern.

<figure style="width: 600px;">
  {%
    inline_svg
    filename="sqs_queue_worker.svg"
    alt="Three boxes joined by arrows, pointing from left to right. Boxes, L–R: a pink box (labelled “input queue”); a black dashed box (labelled “worker”); another pink box (labelled “output queue”)."
  %}
</figure>

Sometimes a task can't be processed successfully -- for example, if there's a bug in the worker code.
You can [configure SQS][sqs_dlq] to send such problematic messages to a [dead-letter queue (DLQ)][dlq], where you can inspect them in isolation and work out what went wrong.

[sqs_dlq]: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
[dlq]: https://en.wikipedia.org/wiki/Dead_letter_queue

Once we've found the problem in the worker, fixed the bug and deployed a new version, we want to send all the messages from the DLQ back to the original input queue, so they can be processed by the updated worker.
There's no way to do this in SQS directly, so we've written a script to do it for us.
Although we primarily use this to redrive problematic messages that went to a DLQ, **this script allows you to move messages between an arbitrary pair of SQS queues**.

It uses code I shared two years ago [to dump the contents of an SQS queue][dump_q].

[dump_q]: /2018/downloading-sqs-queues/
[send_message_batch]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.send_message_batch
[fixed_chunks]: /2018/iterating-in-fixed-size-chunks/

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

```python
#!/usr/bin/env python
"""
Move all the messages from one SQS queue to another.

Usage: redrive_sqs_queue.py --src-url=<SRC_QUEUE_URL> --dst-url=<DST_QUEUE_URL>
       redrive_sqs_queue.py -h | --help

See https://alexwlchan.net/2020/05/moving-messages-between-sqs-queues/

"""
import argparse
import sys

import boto3


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Move all the messages from one SQS queue to another."
    )

    parser.add_argument(
        "--src-url",
        required=True,
        help="Queue to read messages from (e.g. a dead-letter queue)",
    )
    parser.add_argument("--dst-url", required=True, help="Queue to move messages to")

    return parser.parse_args()


def get_messages_from_queue(sqs_client, queue_url):
    """Generates messages from an SQS queue.

    Note: this continues to generate messages until the queue is empty.
    Every message on the queue will be deleted.

    :param queue_url: URL of the SQS queue to read.

    See https://alexwlchan.net/2018/01/downloading-sqs-queues/

    """
    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url, AttributeNames=["All"], MaxNumberOfMessages=10
        )

        try:
            yield from resp["Messages"]
        except KeyError:
            return

        entries = [
            {"Id": msg["MessageId"], "ReceiptHandle": msg["ReceiptHandle"]}
            for msg in resp["Messages"]
        ]

        resp = sqs_client.delete_message_batch(QueueUrl=queue_url, Entries=entries)

        if len(resp["Successful"]) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )


if __name__ == "__main__":
    args = parse_args()

    src_queue_url = args.src_url
    dst_queue_url = args.dst_url

    if src_queue_url == dst_queue_url:
        sys.exit("Source and destination queues cannot be the same.")

    sqs_client = boto3.client("sqs")

    for message in get_messages_from_queue(sqs_client, queue_url=src_queue_url):
        sqs_client.send_message(QueueUrl=dst_queue_url, MessageBody=message["Body"])
```
