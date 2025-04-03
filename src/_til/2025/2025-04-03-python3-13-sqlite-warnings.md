---
layout: til
title: Python 3.13 throws a `ResourceWarning` for SQLite databases that aren't explicitly closed
date: 2025-04-03 21:37:24 +0100
tags:
  - sqlite3
  - python
---
I was debugging some tests with a colleague today, and they were getting three test failures that I couldn't reproduce locally or in GitHub Actions:

```
pytest.PytestUnraisableExceptionWarning:
Exception ignored in: <sqlite3.Connection object>
…
ResourceWarning: unclosed database in <sqlite3.Connection object>
```

(We run our test suite with pytest and turn [warnings into errors](https://docs.pytest.org/en/7.1.x/how-to/capture-warnings.html), so this `ResourceWarning` was causing their test suite to fail.)

I got the sense that we had some leaky state from another test -- although this is a warning about a `sqlite3.Connection` object, the failing tests weren't doing anything with SQLite.
I guessed that we were opening a SQLite database in one test, then failing to close it, but the warning wasn't being raised until another test had started running.

But why was it failing on their machine, and not mine?

## sqlite3 got an extra warning in Python 3.13

We started comparing environments to work out what was different.

We quickly realised that we were running different versions of Python -- I had Python 3.12, but they had Python 3.13.
I started looking for SQLite changes in [What's new in Python 3.13](https://docs.python.org/3/whatsnew/3.13.html#sqlite3), and quickly found a relevant change:

> sqlite3: A ResourceWarning is now emitted if a Connection object is not closed explicitly. (Contributed by Erlend E. Aasland in gh-105539.)

This matches the error they were seeing.

Once I upgraded to Python 3.13, I could also reproduce the test failures locally.

We then identified the handful of places where we were leaving SQLite databases open, added an explicit close, and the tests started passing.
Hooray!

## Why does it matter?

An unclosed database isn't much of an issue in a test suite.

In our test suite, we use [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) to create temporary databases whenever we use a database in a test.
These databases only last as long as the test is running, and once the test is complete, they can be safely discarded.
The risk of data loss is minimal, because the tests should never be touching databases that contain real data.

An unclosed database can be a bigger issue in a running app.

A year or so ago, I wrote a bug in a Flask app where I would open SQLite database connections on new requests, but not close them afterwards.
Once I'd served a certain number of requests, new requests would fail with an error "too many open files", and the only way to resolve it was restarting the app.
I've now switched to the pattern described in [Using SQLite 3 with Flask](https://flask.palletsprojects.com/en/stable/patterns/sqlite3/) from the Flask docs, which closes the database at the end of each request, and this error has gone away.

Having my test suite check for unclosed files is a useful safety net.
If the test suite passes fine, that's not a guarantee that all is well -- but if I start getting warnings in the test suite, it's a clue that I'm leaving files open somewhere, and that might eventually affect my running app.

In this particular case, the mistake was in a test fixture rather than in app code.
I don't think this bug would have affected the running app, but it's fixed anyway -- and I'm pleased to know Python will catch similar mistakes I make in future.
