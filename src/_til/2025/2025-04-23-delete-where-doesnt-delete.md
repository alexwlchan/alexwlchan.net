---
layout: til
title: Why isn't `delete_where()` deleting rows in sqlite-utils?
summary: |
  The `delete_where()` function doesn't auto-commit, so you need to wrap it `with db.conn` or something else to trigger the commit.
date: 2025-04-23 09:45:02 +0100
tags:
  - python
  - sqlite
  - python:sqlite-utils
---
I was writing some code using `sqlite-utils`, and I was confused about why rows weren't being deleted when I called `delete_where()`.
Here's an example:

```python
from sqlite_utils import Database

db = Database("shapes.db")

db["squares"].insert({"colour": "red"})
db["squares"].insert({"colour": "green"})
db["squares"].insert({"colour": "blue"})

db["squares"].delete_where("colour = 'blue'")
```

If I inspect the database after running this Python script, the `blue` row is still present:

```console
$ sqlite3 shapes.db 'select * from squares'
red
green
blue
```

I found [a four-year old GitHub issue](https://github.com/simonw/sqlite-utils/issues/159) discussing the same behaviour, which explains that `delete_where()` doesn't auto-commmit (unlike other functions like `insert()` or `upsert()`).

You need to wrap it in a context manager that commits the transaction, so it actually performs the deletion.
For example:

```python
with db.conn:
    db["squares"].delete_where("colour = 'blue'")
```

This is how it works in the ["Deleting multiple records" example in the docs](https://sqlite-utils.datasette.io/en/stable/python-api.html#deleting-multiple-records), but it doesn't mention the importance of the `with db.conn` line.
It's also not mentioned in [the API reference](https://sqlite-utils.datasette.io/en/stable/reference.html#sqlite_utils.db.Table.delete_where).

As I was fixing this bug, I had a vague memory of a similar issue with sqlite-utils in the past, but I can't find any notes about it now.
I'm writing this TIL so I can remember if I see this again.
