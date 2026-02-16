---
layout: note
title: Get a string representation of a Python traceback with `traceback.format_exc()`
date: 2025-06-13 09:05:29 +01:00
topic: Python
---
Here's a simple example:

```python {"names":{"1":"traceback"}}
import traceback

try:
    1/0
except Exception:
    print(repr(traceback.format_exc()))
```

And here's the output:

```console {"wrap":true}
$ python3 exception.py
'Traceback (most recent call last):\n  File "exception.py", line 4, in <module>\n    1/0\n    ~^~\nZeroDivisionError: division by zero\n'
```

It's all the text that would be printed to stderr, but now saved in a handy string I can keep for later.





## When do I use this?

I have a bunch of Python data pipelines that process items from a queue, and record success/failure in a database.

When an item fails, it's useful to know why it fails, and recording that information in the database makes it much easier to find than going to look through logs.
