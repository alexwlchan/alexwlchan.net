#!/usr/bin/env python3
"""
This is a script for publishing lots of messages to SNS.

Suppose I have a large collection of messages I want to send to SNS,
stored as lines in a text file, e.g. some Wellcome catalogue IDs.

    xfcrpna3
    qf8sxvxm
    ed3w4fv9
    d4aahw7u
    hwfrryuz

I could loop through the file line-by-line and send them to SNS one-by-one,
but that's slow and inefficient.  It would be more efficient to use the
SNS PublishBatch API to send them ten at a time.

This script provides a convenient wrapper for doing so.

See https://alexwlchan.net/2023/my-sns-firehose/

"""

import argparse
import concurrent.futures
import functools
import itertools
import os
import uuid

import boto3
import tqdm


def concurrently(handler, inputs, *, max_concurrency=5):
    """
    Calls the function ``handler`` on the values ``inputs``.

    ``handler`` should be a function that takes a single input, which is the
    individual values in the iterable ``inputs``.

    Generates (input, output) tuples as the calls to ``handler`` complete.

    See https://alexwlchan.net/2019/10/adventures-with-concurrent-futures/ for an explanation
    of how this function works.

    """
    # Make sure we get a consistent iterator throughout, rather than
    # getting the first element repeatedly.
    handler_inputs = iter(inputs)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(handler, input): input
            for input in itertools.islice(handler_inputs, max_concurrency)
        }

        while futures:
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                original_input = futures.pop(fut)
                yield original_input, fut.result()

            for input in itertools.islice(handler_inputs, len(done)):
                fut = executor.submit(handler, input)
                futures[fut] = input


def chunked_iterable(iterable, size):
    """
    Break an iterable into pieces of the given size.

    See https://alexwlchan.net/2018/iterating-in-fixed-size-chunks/
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def get_batch_entries(path):
    """
    Given a file which contains one notification per line, generate a series
    of values that can be passed as the `PublishBatchRequestEntries` argument
    to the `Sns.publish_batch` method.
    """
    for batch in chunked_iterable(open(path), size=10):
        yield [{"Id": str(uuid.uuid4()), "Message": line.strip()} for line in batch]


def parse_args():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Publish lots of notifications to Amazon SNS.",
    )

    parser.add_argument(
        "INPUT_FILE", help="A path containing notifications to send, one per line"
    )
    parser.add_argument(
        "--topic-arn", help="The ARN of the SNS topic to publish to", required=True
    )

    return parser.parse_args()


def publish_batch(sns_client, topic_arn, batch_entries):
    resp = sns_client.publish_batch(
        TopicArn=topic_arn, PublishBatchRequestEntries=batch_entries
    )

    # This is to account for any failures in sending messages to SNS.
    # I've never actually had this happen in practice so I've not written
    # any code to handle it (I'd probably just retry the whole script)
    # but I include it just in case.
    assert len(resp['Failed']) == 0, resp


def publish_messages(*, input_file, topic_arn):
    sess = boto3.Session()

    # Note: creating boto3 clients isn't thread-safe, so it's important
    # to create it once rather than creating it multiple times in the
    # concurrently() handler.
    #
    # See https://github.com/boto/boto3/issues/801
    sns_client = sess.client("sns")

    total_entries = sum(len(entries) for entries in get_batch_entries(input_file))

    with tqdm.tqdm(total=total_entries) as pbar:
        for (batch, _) in concurrently(
            handler=functools.partial(publish_batch, sns_client, topic_arn),
            inputs=get_batch_entries(input_file),
        ):
            pbar.update(len(batch))


if __name__ == "__main__":
    args = parse_args()
    publish_messages(input_file=args.INPUT_FILE, topic_arn=args.topic_arn)
