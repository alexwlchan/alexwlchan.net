---
layout: til
title: How to gracefully restart a gunicorn app
date: 2024-01-16 14:11:51 +0000
tags:
  - python
  - python:gunicorn
---
Suppose I have a Flask app:

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    color = 'yellow'
    return '<style>body { background: %s }</style>\n\n%s' % (color, color)
```

and I run the app using gunicorn:

```console
$ gunicorn app:app --workers 4 --bind 127.0.0.1:8008 --daemon
```

In this example, I've started four workers, which means five proceeses: one master and four workers.
Here's an example list of processes, slightly tidied for readability:

```console
$ ps -ef | grep gunicorn
16190     1   gunicorn app:app --workers 4 --bind 127.0.0.1:8008 --daemon
16244 16190   gunicorn app:app --workers 4 --bind 127.0.0.1:8008 --daemon
16254 16190   gunicorn app:app --workers 4 --bind 127.0.0.1:8008 --daemon
16264 16190   gunicorn app:app --workers 4 --bind 127.0.0.1:8008 --daemon
16341 16190   gunicorn app:app --workers 4 --bind 127.0.0.1:8008 --daemon
```

Here PID 16190 is the master process, and PIDs 16244, 16254, 16264 and 16341 are the workers.

To reload the app (e.g. if you've changed the source code), you can send a SIGUP to one of the processes, for example:

```console
$ kill -HUP 12345
```

(This master/worker nomenclature is how they're described [gunicorn itself](https://docs.gunicorn.org/en/stable/design.html).)

## What if the new code is faulty?

If there's a bug in the updated code (say, a syntax error), then reloading the app will tear down the entire site.

This seems to happen whether I restart the master or just one of the workers.

## Restart the master or the worker?

Either works.

If you restart the master process, it restarts all the workers -- your change rolls out immediately.

If you restart a single worker, the other workers are untouched -- so you'll get different responses depending which worker you hit.

## What about environment variables?

A common pattern in my apps is to inject some environment variables at startup.
If I `kill -HUP` a gunicorn app, it remembers the original environment variables that were passed in – you don't need to re-set them.
