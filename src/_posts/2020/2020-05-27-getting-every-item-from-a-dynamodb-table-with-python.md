---
layout: post
date: 2020-05-27 09:26:13 +0000
title: Getting every item from a DynamoDB table with Python
summary: A Python function that generates every item in a DynamoDB table.
category: Amazon Web Services
tags: aws amazon-dynamodb python
---

At work, we use [DynamoDB] as our primary database.
DynamoDB is a NoSQL database service hosted by Amazon, which we use as a persistent key-value store.
Our apps make requests like *"Store this document under identifier X"* ([PutItem]) or *"Give me the document stored under identifier Y"* ([GetItem]).
This sort of single document lookup is very fast in DynamoDB.

DynamoDB is less useful if you want to do anything that involves processing documents in bulk, such as aggregating values across multiple documents, or doing a bulk update to everything in a table.
There's no built-in way to do this -- you have to use the [Scan operation] to read everything in the table, and then write your own code to do the processing.

I've written a function to get every item from a DynamoDB table many times, so I'm going to put a tidied-up version here that I can copy into future scripts and projects.
If this is something you'd find useful, copy and paste it into your own code.

[DynamoDB]: https://en.wikipedia.org/wiki/Amazon_DynamoDB
[PutItem]: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html
[GetItem]: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html
[Scan operation]: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html



## Scanning in serial: simple, but slow

The Python SDK for AWS is [boto3].
It includes [a client for DynamoDB], and [a paginator] for the Scan operation that fetches results across multiple pages.

I wrap that in a function that generates the items from the table, one at a time, as shown below.
By yielding the items immediately, it avoids holding too much of the table in memory, and the calling code can start processing items immediately.

If I want to use an extra parameter like FilterExpression, I can pass that into the function and it gets passed to the Scan.

```python
import boto3


def scan_table(dynamo_client, *, TableName, **kwargs):
    """
    Generates all the items in a DynamoDB table.

    :param dynamo_client: A boto3 client for DynamoDB.
    :param TableName: The name of the table to scan.

    Other keyword arguments will be passed directly to the Scan operation.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    """
    paginator = dynamodb_client.get_paginator("scan")

    for page in paginator.paginate(TableName=TableName, **kwargs):
        yield from page["Items"]


if __name__ == "__main__":
    dynamodb_client = boto3.client("dynamodb")

    for item in scan_table(dynamodb_client, TableName="my-table-name"):
        print(item)
```

[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[a client for DynamoDB]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
[a paginator]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#paginators



## Scanning in parallel: faster, more complex

The function above works fine, but it can be slow for a large table -- it only reads the rows one at a time.
If you want to go faster, DynamoDB has a feature called [Parallel Scan].
It splits the table into distinct segments, and if you run multiple workers in parallel, each reading a different segment, you can read the table much faster.

(Long-time readers might remember I've previously written [about using Parallel Scan in Scala].)

This is a bit more complicated, because we have to handle the pagination logic ourselves.
We also need to spin up the multiple workers, and then combine their results back together.

The code is based on one of [my recipes for concurrent.futures].
It creates a future with a Scan operation for each segment of the table.
When the future completes, it looks to see if there are more items to fetch in that segment -- if so, it schedules another future; if not, that segment is done.
It keeps doing this until it's read the entire table.

Depending on how much parallelism I have available, this can be many times faster than scanning in serial.

```python
import concurrent.futures
import itertools

import boto3


def parallel_scan_table(dynamo_client, *, TableName, **kwargs):
    """
    Generates all the items in a DynamoDB table.

    :param dynamo_client: A boto3 client for DynamoDB.
    :param TableName: The name of the table to scan.

    Other keyword arguments will be passed directly to the Scan operation.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    This does a Parallel Scan operation over the table.

    """
    # How many segments to divide the table into?  As long as this is >= to the
    # number of threads used by the ThreadPoolExecutor, the exact number doesn't
    # seem to matter.
    total_segments = 25

    # How many scans to run in parallel?  If you set this really high you could
    # overwhelm the table read capacity, but otherwise I don't change this much.
    max_scans_in_parallel = 5

    # Schedule an initial scan for each segment of the table.  We read each
    # segment in a separate thread, then look to see if there are more rows to
    # read -- and if so, we schedule another scan.
    tasks_to_do = [
        {
            **kwargs,
            "TableName": TableName,
            "Segment": segment,
            "TotalSegments": total_segments,
        }
        for segment in range(total_segments)
    ]

    # Make the list an iterator, so the same tasks don't get run repeatedly.
    scans_to_run = iter(tasks_to_do)

    with concurrent.futures.ThreadPoolExecutor() as executor:

        # Schedule the initial batch of futures.  Here we assume that
        # max_scans_in_parallel < total_segments, so there's no risk that
        # the queue will throw an Empty exception.
        futures = {
            executor.submit(dynamo_client.scan, **scan_params): scan_params
            for scan_params in itertools.islice(scans_to_run, max_scans_in_parallel)
        }

        while futures:
            # Wait for the first future to complete.
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                yield from fut.result()["Items"]

                scan_params = futures.pop(fut)

                # A Scan reads up to N items, and tells you where it got to in
                # the LastEvaluatedKey.  You pass this key to the next Scan operation,
                # and it continues where it left off.
                try:
                    scan_params["ExclusiveStartKey"] = fut.result()["LastEvaluatedKey"]
                except KeyError:
                    break
                tasks_to_do.append(scan_params)

            # Schedule the next batch of futures.  At some point we might run out
            # of entries in the queue if we've finished scanning the table, so
            # we need to spot that and not throw.
            for scan_params in itertools.islice(scans_to_run, len(done)):
                futures[executor.submit(dynamo_client.scan, **scan_params)] = scan_params


if __name__ == "__main__":
    dynamo_client = boto3.resource("dynamodb").meta.client

    for item in parallel_scan_table(dynamo_client, TableName="my-table-name"):
        print(item)
```

[Parallel Scan]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan
[about using Parallel Scan in Scala]: /2018/08/parallel-scan-scanamo/
[my recipes for concurrent.futures]: /2019/10/adventures-with-concurrent-futures/
