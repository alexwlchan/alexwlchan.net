---
layout: post
date: 2017-11-22 11:50:19 +0000
title: Downloading logs from Amazon CloudWatch
tags: aws python
summary: A detailed breakdown of how I wrote a Python script to download logs from CloudWatch.
category: Working with AWS
---

At work, we use [Amazon CloudWatch][cloudwatch] for logging in our applications.
All our logs are sent to CloudWatch, and you can browse them in the AWS Console.
The web console is fine for one-off use, but if I want to do in-depth analysis of the log, nothing beats a massive log file.
I'm very used to tools like grep, awk and tr, and I'm more productive using those than trying to wrangle a web interface.

So I set out to write a Python script to download all of my CloudWatch logs into a single file.
The AWS SDKs give you access to CloudWatch logs, so this seems like it should be possible.
There are other tools for doing this (for example, I found [awslogs][awslogs] after I was done) --- but sometimes it can be instructive to reinvent something from scratch.

In this post, I'll explain how I wrote this script, starting from nothing and showing how I build it up.
It's also a nice chance to illustrate several libraries I use a lot (boto3, docopt and maya).
If you just want the code, skip to the end of the post.

[cloudwatch]: https://en.wikipedia.org/wiki/Amazon_Elastic_Compute_Cloud#Amazon_CloudWatch
[awslogs]: https://github.com/jorgebastida/awslogs

<!-- summary -->

## Getting all the logs

Let's start by grabbing a bundle of logs from CloudWatch.
In CloudWatch, each application has its own _log group_.
Within the group, each running instance has its own _log stream_, which in turn contains a series of _log events_.
You can filter log events by group or by stream.

Our applications often run multiple instances at once (for extra capacity and redundancy), so I want to grab all the logs from the group, which may cover multiple streams.
In this post, I won't show you how to filter to a single stream --- but you might want to try adding that feature if it would be useful for you.

There are two methods in the [boto3 SDK][boto3] that sound helpful -- `filter_log_events()`, and `get_log_events()`.
The latter only lets us read from a single stream at a time, but we want to read from multiple streams, so we'll use `filter` in this script.
Let's grab the first batch of events:

[boto3]: http://boto3.readthedocs.io/en/latest/reference/services/logs.html

```python
import boto3


def get_log_events(log_group):
    """List the first 10000 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    client = boto3.client('logs')
    resp = client.filter_log_events(logGroupName=log_group, limit=10000)
    return resp['events']


if __name__ == '__main__':
    for event in get_log_events('platform/loris'):
        print(event)
```

We're only passing two arguments to `get_log_events`: the name of the log group, and the maximum number of events to return.
I've set this to 10,000, the maximum, to reduce the number of API calls we need.
Then the whole set is returned as a list of 10k items.

But what if we have more than 10k logs?
How do we get the rest?

The docs tell us that each API response includes a `nextToken` parameter, which we can pass into the next call to get the next set of logs.
So let's tweak the function to do that:

```python
def get_log_events(log_group):
    """Generate all the log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    client = boto3.client('logs')
    kwargs = {
        'logGroupName': log_group,
        'limit': 10000,
    }
    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break
```

This will poll continuously, passing `nextToken` into the next call, until we get a response that doesn't include it --- which is the final set of log events.

Notice that the previous function returned a list of events; here, I've switched to using a generator with `yield from` (requires Python 3).
We could accumulate a list inside the function, then return that list --- but that's potentially very memory-expensive (if there are lots of events), and a generator means the caller can abort early, thus saving API calls and time.

So now we have a way to get ALL THE LOGS.

## Wrapping that in a script

We've got a generator that gives us all the events.
Let's send them somewhere useful --- for me, that's a log file that has all the messages, one per line.
I wrote a script like this:

```python
def get_log_events(log_group):
    ...


if __name__ == '__main__':
    for event in get_log_events('platform/loris'):
        print(event['message'].rstrip())
```

Note that I'm calling `rstrip()` on each message --- this is to get rid of trailing newlines, so my log file doesn't have lots of extra empty lines.

Now I can run the following command at the console:

```console
$ python3 print_log_events.py > loris.log
```

and I get my log file!

## Passing command-line parameters

So we have a script, but we have to hard-code the name of the log group.
Every time I want a different set of logs, I have to edit the script.
That's a bit yucky; wouldn't it be nice if we could pass the script parameters instead?

Enter [docopt][docopt], a library for parsing command-line arguments.
I've written about docopt [before][before]; in short, it lets you write the help string for a script, and then uses that to build an argument parser.

Most of the work is writing the help string --- parsing the arguments only requires a single line of code.
Something like:

```python
"""Print log event messages from a CloudWatch log group.

Usage: print_log_events.py <LOG_GROUP_NAME>
       print_log_events.py -h --help

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  -h --help       Show this screen.

"""

import docopt


def get_log_events(log_group):
    ...


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    log_group = args['<LOG_GROUP_NAME>']
    for event in get_log_events(log_group=log_group):
        print(event['message'].rstrip())
```

So now I can pass different log groups on the command line, and get different logs:

```console
$ python3 print_log_events.py platform/loris > loris.log
$ python3 print_log_events.py platform/catalogue_api > catalogue_api.log
```

This gives us a script that can download all the logs, and get them from any log group we have access to.

[docopt]: http://docopt.org/
[before]: /2017/09/ode-to-docopt/

## Filtering by date

The current script will download _all_ the logs in a group.
That could be quite a lot!
Some of our applications have been running for months, and will have millions of log events.
What if we want less?
For example, if I'm investigating outages from the last few days, I only want a few days of logs.
I don't need the complete log history of the application.

The boto3 docs for [client.get\_log\_events()][get_log_events] show us two parameters we can use for this purpose:

> **startTime** (_integer_) -- The start of the time range, expressed as the number of milliseconds after Jan 1, 1970 00:00:00 UTC. Events with a time stamp earlier than this time are not included.
>
> **endTime** (_integer_) -- The end of the time range, expressed as the number of milliseconds after Jan 1, 1970 00:00:00 UTC. Events with a time stamp later than this time are not included.

For now, let's just add some new parameters to our function, and pass them straight through:

```python
def get_log_events(log_group, start_time=None, end_time=None):
    """Generate all the log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.
    :param start_time: Only fetch events with a timestamp after this time.
        Expressed as the number of milliseconds after midnight Jan 1 1970.
    :param end_time: Only fetch events with a timestamp before this time.
        Expressed as the number of milliseconds after midnight Jan 1 1970.

    """
    client = boto3.client('logs')
    kwargs = {
        'logGroupName': log_group,
        'limit': 10000,
    }

    if start_time is not None:
        kwargs['startTime'] = start_time
    if end_time is not None:
        kwargs['endTime'] = end_time

    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break
```

We can also add some options for users to pass the start time and end time to the script:

```python
"""Print log event messages from a CloudWatch log group.

Usage: print_log_events.py <LOG_GROUP_NAME> [--start=<START>] [--end=<END>]
       print_log_events.py -h --help

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  --start=<START>     Only print events with a timestamp after this time
                      (expressed as milliseconds after midnight Jan 1, 1970).
  --end=<END>         Only print events with a timestamp before this time
                      (expressed as milliseconds after midnight Jan 1, 1970).
  -h --help           Show this screen.

"""

def get_log_events(log_group, start_time, end_time):
    ...


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    log_group = args['<LOG_GROUP_NAME>']
    if args['--start']:
        start_time = int(args['--start'])
    else:
        start_time = None
    if args['--end']:
        end_time = int(args['--end'])
    else:
        end_time = None

    logs = get_log_events(
        log_group=log_group,
        start_time=start_time,
        end_time=end_time
    )
    for event in logs:
        print(event['message'].rstrip())
```

So if I want to fetch logs from the last 24 hours, I can run:

```console
$ python3 print_log_events.py platform/loris --start=1511213601140 --end=1511299967564
```

[get_log_events]: http://boto3.readthedocs.io/en/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_events

## Graceful handling of times

Expressing time as milliseconds since midnight on 1 Jan 1970 UTC is… awkward.

It's a (fairly) unambiguous format for computers to deal with, but it's unwieldy for people.
Before you can use those parameters, you need to handle timezones, seconds, and so on.
Datetime logic is very fiddly --- so let's not do it ourselves.

Luckily, Python has a wealth of libraries for dealing with datetimes.
A recent favourite of mine is [Maya][maya], which wraps a number of other datetime libraries for a nice, clean API.
In particular, there's a way to turn human descriptions of times into datetime objects:

```pycon
>>> import maya
>>> maya.when('two days ago')
<MayaDT epoch=1511169236.51311>
>>> maya.when('yesterday at 3pm')
<MayaDT epoch=1511276400.0>
```

Maya records times as seconds since the epoch (with negative integers used to record times before the epoch).
We can use this to get milliseconds as well:

```python
import maya


def milliseconds_since_epoch(time_string):
    dt = maya.when(time_string)
    seconds = dt.epoch
    return seconds * 1000
```

Now we can take the `--start` and `--end` arguments to our script, and pass them through the function before we call `get_log_events()`.
This gives our script a much more human-friendly interface:

```python
"""Print log event messages from a CloudWatch log group.

Usage: print_log_events.py <LOG_GROUP_NAME> [--start=<START>] [--end=<END>]
       print_log_events.py -h --help

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  --start=<START>     Only print events with a timestamp after this time.
  --end=<END>         Only print events with a timestamp before this time.
  -h --help           Show this screen.

"""

def get_log_events(log_group, start_time, end_time):
    ...


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    log_group = args['<LOG_GROUP_NAME>']

    if args['--start']:
        try:
            start_time = milliseconds_since_epoch(args['--start'])
        except ValueError:
            exit(f'Invalid datetime input as --start: {args["--start"]}')
    else:
        start_time = None

    if args['--end']:
        try:
            end_time = milliseconds_since_epoch(args['--end'])
        except ValueError:
            exit(f'Invalid datetime input as --end: {args["--end"]}')
    else:
        end_time = None

    ...
```

Notice that I'm wrapping the call in a `try … except ValueError` block --- this is to catch any errors raised by Maya, if the user passes a datetime string it fails to parse.
Wrapping and re-raising the error means we can give more user-friendly context, noting the value which caused the error, and the name of the associated flag.

The `get_log_events()` function retains the millisecond-based interface --- I've deliberately kept the date-parsing logic out of that function.
That function stays small and focused, which makes it easier to reuse, maintain and test.

[maya]: https://github.com/kennethreitz/maya

## Putting it all together

In this post, we've written a script that:

* Gets a series of log events from CloudWatch
* Prints the associated log messages
* Filters the logs based on start time and end time
* Reads command-line input to get the log group name, start time, and end time --- and does so in a human-friendly way

This is the final version of the script:

```python
#!/usr/bin/env python
# -*- encoding: utf-8
"""Print log event messages from a CloudWatch log group.

Usage: print_log_events.py <LOG_GROUP_NAME> [--start=<START>] [--end=<END>]
       print_log_events.py -h --help

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  --start=<START>     Only print events with a timestamp after this time.
  --end=<END>         Only print events with a timestamp before this time.
  -h --help           Show this screen.

"""

import boto3
import docopt
import maya


def get_log_events(log_group, start_time=None, end_time=None):
    """Generate all the log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.
    :param start_time: Only fetch events with a timestamp after this time.
        Expressed as the number of milliseconds after midnight Jan 1 1970.
    :param end_time: Only fetch events with a timestamp before this time.
        Expressed as the number of milliseconds after midnight Jan 1 1970.

    """
    client = boto3.client('logs')
    kwargs = {
        'logGroupName': log_group,
        'limit': 10000,
    }

    if start_time is not None:
        kwargs['startTime'] = start_time
    if end_time is not None:
        kwargs['endTime'] = end_time

    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break


def milliseconds_since_epoch(time_string):
    dt = maya.when(time_string)
    seconds = dt.epoch
    return seconds * 1000


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    log_group = args['<LOG_GROUP_NAME>']

    if args['--start']:
        try:
            start_time = milliseconds_since_epoch(args['--start'])
        except ValueError:
            exit(f'Invalid datetime input as --start: {args["--start"]}')
    else:
        start_time = None

    if args['--end']:
        try:
            end_time = milliseconds_since_epoch(args['--end'])
        except ValueError:
            exit(f'Invalid datetime input as --end: {args["--end"]}')
    else:
        end_time = None

    logs = get_log_events(
        log_group=log_group,
        start_time=start_time,
        end_time=end_time
    )
    for event in logs:
        print(event['message'].rstrip())
```

I don't use this script every time I want to check my CloudWatch logs --- for simple tasks, the web interface is good enough, and lots of API calls can be really slow --- but for detailed log analysis, it's invaluable.

It takes longer to write these detailed breakdowns of scripts, but it's a useful exercise (for me if nobody else!).
It forces me to really think about what I'm writing, and I always get better code as a result.
This is far too low for most code, but I recommend trying it every once in a while.
