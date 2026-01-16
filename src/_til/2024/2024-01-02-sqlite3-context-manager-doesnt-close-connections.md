---
layout: til
title: Python's sqlite3 context manager doesn’t close connections
date: 2024-01-02 07:18:04 +00:00
summary: |
  The `sqlite3.connect(…)` context manager will hold connections open, so you need to remember to close it manually or write your own context manager.
tags:
  - python
  - sqlite
---
I was working on an app that started failing in prod with an error “too many open files”, and I think it was because I wasn't closing SQLite database connections properly.

In my case I was literally just creating the connection and never closing it:

```python
import sqlite3

con = sqlite3.connect("example.db")
cur = con.cursor()
…
```

I think the `con` variable would eventually get garbage-collected, but obviously not fast enough!

I also found [a blog post by Robin Wilson][robin] describing a similar issue, where the built-in context manager in `sqlite3` doesn't actually close the connection.
It will commit any pending transactions, but holds the database open:

```python
import sqlite3

with sqlite3.connect('test.db') as connection:
    # do some stuff in the database

# out of the context manager, database is still open
```

You have to explicitly close the connection yourself, e.g. writing your own context manager or using [contextlib.closing].
There are suggestions in the comments on Robin's blog, and I know I've written a few before.

[robin]: https://blog.rtwilson.com/a-python-sqlite3-context-manager-gotcha/
[contextlib.closing]: https://docs.python.org/3/library/contextlib.html#contextlib.closing
