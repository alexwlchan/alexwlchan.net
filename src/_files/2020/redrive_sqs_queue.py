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
