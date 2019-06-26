---
layout: post
date: 2018-01-25 21:56:15 +0000
title: Getting every message in an SQS queue
tags: aws python
summary: Code for saving every message from an SQS queue, and then saving the messages to a file, or resending them to another queue.
category: Working with AWS

index:
  best_of: true
---

At work, we make heavy use of [Amazon SQS][sqs] message queues.
We have a series of small applications which communicate via SQS.
Each application reads a message from a queue, does a bit of processing, then pushes it to the next queue.
This is a classic microservices pattern.

![Three applications, communicating via two message queues.](/images/2018/sqs_queues.png)

Sometimes an application fails to process a message correctly, in which case SQS can send the message to a separate [dead-letter queue (DLQ)][dlq].
(Our [Terraform module for SQS queues][tf] automatically creates and configures a DLQ for all our queues.)
Sending faulty messages to a DLQ allows you to see them all in one go, rather than trying to spot the failures in your logs.

Unfortunately, the AWS Console doesn't make it very easy to go through the contents of a queue.
You can see one message at a time, but this makes it hard to spot patterns or debug a large number of failures.
It would be easier to have the entire queue in a local file, so we can analyse it or process every message at once.
I've written a Python function to do just that, and in this post, I'll walk through how it works.

<!-- summary -->

<figure>
  <img src="/images/2018/sqs_console.png" alt="A list of rows in the SQS Console, showing a fragment of the body, the size and the sent date.">
  <figcaption>
    Viewing queue messages in the AWS Console.
    Our messages are large JSON objects, so most of the detail isn't even visible!
    You can click "More Details" to see the entire message, but you can only view one at a time.
  </figcaption>
</figure>

We start with the [`receive_message()` method][rmessages] in the boto3 SDK.
This allows us to download our first batch of messages:

```python
import boto3

sqs_client = boto3.client('sqs')
resp = sqs_client.receive_message(
    QueueUrl='https://sqs.eu-west-1.amazonaws.com/1234567890/example_dlq',
    AttributeNames=['All'],
    MaxNumberOfMessages=10
)
```

We pass the URL of our DLQ as a parameter.
The "AttributeNames = All" means we get as much information as possible about queue messages, because it might be useful later.
We ask for 10&nbsp;messages because that's the most we can fetch in a single API call.

The docs tell us the response is a dict with a single key, "Messages", which contains the messages.
If the queue is empty, so is the response.
So we can extract the individual messages like this:

```python
try:
    messages = resp['Messages']
except KeyError:
    print('No messages on the queue!')
    messages = []
```

So once we have the first ten messages, we want to get the next ten messages.
How do we do that?

We could call `receive_message()` again, and we'd probably get new messages, but we need to be careful.
Just receiving a message isn't enough to remove it from an SQS queue.
Suppose it were: if a consumer received a message from a queue, then crashed before it could finish processing the message, the original message would be lost.

To prevent losing messages, consumers have to explicitly tell SQS that they're finished with the message -- and only then does it delete the message from the queue.
If SQS doesn't hear back within a certain time (the *visibility timeout*, default 30&nbsp;seconds), it assumes the message needs to be re-sent.
Only when SQS has re-sent a message several times, and never heard back from a consumer, does it assume the message is faulty, and then the message is sent to the DLQ.

So we need to mark our messages as "done", or we might get duplicate messages from `receive_message()`.
Each message includes a `ReceiptHandle` that we send back to SQS via the [`delete_message_batch()` API][delete].
We need to pass it a list of dicts, each containing an ID (that we generate) and a receipt handle.

```python
entries = [
    {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
    for msg in resp['Messages']
]

resp = sqs_client.delete_message_batch(QueueUrl=queue_url, Entries=entries)
```

The response tells us whether it successfully deleted all the messages, and if not, which failed to delete.
That's what the IDs are for -- we can work out which deletes failed, if any.
We could use the IDs to retry any failed deletes, but in practice, I've never had an issue with message deletions, so I'll just raise an error if that ever occurs:

```python
if len(resp['Successful']) != len(entries):
    raise RuntimeError(
        f"Failed to delete messages: entries={entries!r} resp={resp!r}"
    )
```

(Note use of [f-strings][pep498], which have me a total convert to Python 3.)

Putting this together, we have enough code to fetch ten messages from a queue.
Then we can run this repeatedly until the queue runs out of messages.
Rather than printing when we get the KeyError, we break out of the loop.
And then let's wrap the code in a function:

```python
import boto3


def get_messages_from_queue(queue_url):
    sqs_client = boto3.client('sqs')

    messages = []

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )

        try:
            messages.extend(resp['Messages'])
        except KeyError:
            break

        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in resp['Messages']
        ]

        resp = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )

        if len(resp['Successful']) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )

    return messages
```

This isn't ideal, because we're accumulating all the messages in a list -- if our queue is large, this spends a lot of memory.
We might run out of memory entirely, and lose all the messages!
Better would be to rewrite this as a generator, yielding the messages as we receive them.
If we do that, the code becomes cleaner and more efficient.

Add a docstring, and we have the final version of the function:

```python
import boto3


def get_messages_from_queue(queue_url):
    """Generates messages from an SQS queue.

    Note: this continues to generate messages until the queue is empty.
    Every message on the queue will be deleted.

    :param queue_url: URL of the SQS queue to drain.

    """
    sqs_client = boto3.client('sqs')

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )

        try:
            yield from resp['Messages']
        except KeyError:
            return

        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in resp['Messages']
        ]

        resp = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )

        if len(resp['Successful']) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )
```

If you want to use this code, just copy-and-paste it into your project, ideally with a link back to this post.

## Saving the messages to a file

One use for this code is saving the entire queue to a local file, one message per line.
This means I can start to unpick it with tools like [jq][jq] and [grep][grep], and look for common patterns or failure reasons in my messages.

Having a generator of messages means I can print them one-by-one, redirect to a file, and I don't need to keep them in memory.
Throw in docopt for some argument parsing, and I've got a complete script:

```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: get_sqs_messages.py <QUEUE_URL>
       get_sqs_messages.py -h | --help
"""

import json

import boto3
import docopt


def get_messages_from_queue(queue_url):
    ...


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    queue_url = args['<QUEUE_URL>']

    for message in get_messages_from_queue(queue_url):
        print(json.dumps(message))
```

I run the script as follows:

```console
$ python get_sqs_messages.py 'https://sqs.amazonaws.com/1234567890/example_q' > q.txt
```

(I could modify the script to take a `--file` argument, and have the script write directly to the file, but shell redirection is fine.
There's no need to reinvent the wheel.)

## Re-sending messages to another queue

Here's another common pattern: some messages fail and land on a DLQ.
We identify the problem, fix the bug, and deploy a new version.
Now we'd like to re-send all those messages to the original queue, so they can be processed by the fixed application.

As well as `receive_message()`, boto3 also has a [`send_message()` API][sendmsg].
We need to pass it the queue URL, and the message body -- and we have the latter from the original message.
So once again adding some docopt for dressing:

```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: sqs_redrive.py --src=<QUEUE_URL> --dst=<QUEUE_URL>
       sqs_redrive.py -h | --help
"""

import boto3
import docopt


def get_messages_from_queue(queue_url):
    ...


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    src_queue_url = args['--src']
    dst_queue_url = args['--dst']

    sqs_client = boto3.client('sqs')

    for message in get_messages_from_queue(src_queue_url):
        sqs_client.send_message(
            QueueUrl=dst_queue_url,
            Body=message['Body']
        )
```

and you run this script as follows:

```console
$ python sqs_redrive.py \
        --src='https://sqs.amazonaws.com/1234567890/example_dlq' \
        --dst='https://sqs.amazonaws.com/1234567890/example_q'
```

## Other uses

Most of the time, our applications run smoothly, and our DLQs sit idle.
But when something does go wrong, these are both useful scripts to have lying around.
I'm sure there are other uses for this code.
If you find it useful, or think of another way to use it, please [let me know][contact]!

[sqs]: https://en.wikipedia.org/wiki/Amazon_Simple_Queue_Service
[dlq]: https://en.wikipedia.org/wiki/Dead_letter_queue
[tf]: https://github.com/wellcometrust/terraform-modules/tree/master/sqs
[rmessages]: http://boto3.readthedocs.io/en/stable/reference/services/sqs.html#SQS.Client.receive_message
[delete]: http://boto3.readthedocs.io/en/stable/reference/services/sqs.html#SQS.Client.delete_message_batch
[pep498]: https://www.python.org/dev/peps/pep-0498/
[jq]: https://stedolan.github.io/jq/
[grep]: https://en.wikipedia.org/wiki/Grep
[sendmsg]: http://boto3.readthedocs.io/en/stable/reference/services/sqs.html#SQS.Client.send_message
[contact]: /#contact
