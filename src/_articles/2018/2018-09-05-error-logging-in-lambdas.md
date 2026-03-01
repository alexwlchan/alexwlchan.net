---
layout: article
date: 2018-09-05 20:11:59 +00:00
title: A basic error logger for Python Lambdas
summary: A snippet to make it a bit easier to debug errors in AWS Lambda functions
  written in Python.
topics:
  - AWS
  - Python
---

At work, we use [AWS Lambda][lambda] functions for a bunch of "glue" pieces between different services.
Sometimes, a quick Python script in a Lambda function is the most convenient way to run something.

This post has a snippet that I wrote to make it easier to debug errors.

As a quick reminder, this is the basic structure of a Lambda:

```python {"names":{"1":"json","2":"lambda_handler","3":"event","4":"context"}}
import json


def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
```

The body of your code goes in [the handler function][handler], which is passed an event and a context.
The event is the trigger for the function (for example, if you have a Lambda triggered by an SNS message, it would contain the SNS body).
The [context object][context] contains some runtime information about the Lambda.

When I was first writing Lambdas, I'd log the event so I could see what the trigger was:

```python {"names":{"1":"lambda_handler","2":"event","3":"context"}}
def lambda_handler(event, context):
    print('event = %r' % event)
    ...
```

This is fine when experimenting, but when the Lambda was run at scale, it got expensive -- some of our events are quite large, and logging the entire event racks up quite a CloudWatch bill.
And in 99% of cases, the log is unnecessary -- I only ever looked at the log when I was developing something new, or if there'd been an error.
If the Lambda completed successfully, I'd never read the log.

So I took it out, and the bill went back down -- but now I can't see what the trigger was if the Lambda has an error.
This is annoying when I'm trying to debug an error.

So I wrote this snippet, which logs the event if and only if the Lambda throws an exception:

```python {"names":{"1":"functools","2":"sys","3":"log_event_on_error","4":"handler","8":"wrapper","9":"event","10":"context"}}
import functools
import sys


def log_event_on_error(handler):
    @functools.wraps(handler)
    def wrapper(event, context):
        try:
            return handler(event, context)
        except Exception:
            print('event = %r' % event)
            raise

    return wrapper
```

This is a decorator that runs the original handler, and if the handler throws an exception, it prints the trigger event and re-raises the exception.
You could also log the context here; I don't because I've yet to find anything useful in the context I'd want when debugging.

To use the decorator, I add `@log_event_on_error` to the handler function.
Like so:

```python {"names":{"1":"json","3":"lambda_handler","4":"event","5":"context"}}
import json


@log_event_on_error
def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
```

This gives me the best of both worlds: no logging if the handler completes successfully (and no logging costs!), and it logs the event if something unexpected goes wrong.

This snippet has been running in prod for several months, and it's been a useful addition to my collection.

[lambda]: https://en.wikipedia.org/wiki/AWS_Lambda
[handler]: https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
[context]: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html