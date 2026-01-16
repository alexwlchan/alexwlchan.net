---
layout: til
title: Use shlex.split() to parse log files quickly
date: 2024-01-05 12:09:22 +00:00
tags:
  - python
  - nginx
---
I wanted to parse some nginx log files, and I know I've done something like this in the past (possibly with Apache logs) – but I remember that involved quite a complicated regex for extracting all the components.

I stumbled upon [an article by ksndeveloper][ksndeveloper] with a much simpler trick: [use `shlex.split()`][shlex.split].

Today I wanted to get a list of URLs from a set of log messages, which went as so:

```pycon
>>> import shlex
>>> line = '127.0.0.1 - - [01/Dec/2023:12:08:23 +0000] "GET /page/with/error HTTP/1.0" 500 0 "-" "-"'

>>> shlex.split(line)
['127.0.0.1', '-', '-', '[01/Dec/2023:12:08:23', '+0000]', 'GET /page/with/error HTTP/1.0', '500', '0', '-', '-']

>>> shlex.split(line)[5]
'GET /page/with/error HTTP/1.0'

>>> shlex.split(line)[5].split()
['GET', '/page/with/error', 'HTTP/1.0']

>>> shlex.split(line)[5].split()[1]
'/page/with/error'
```

I haven't tested this extensively, so I don't know if it's robust against larger, more complex log files, but it worked well enough for some quick analysis.

[ksndeveloper]: https://dev.to/ksndeveloper/parsing-nginx-logs-using-python-1m6k
[shlex.split]: https://docs.python.org/3/library/shlex.html#shlex.split
