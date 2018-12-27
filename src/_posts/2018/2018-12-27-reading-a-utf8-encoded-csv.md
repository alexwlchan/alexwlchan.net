---
layout: post
date: 2018-12-27 17:38:55 +0000
title: Notes on reading a UTF-8 encoded CSV in Python
summary: Some notes on trying to do this in a way that supports both Python 2 and 3, and the frustration of doing so.
tags: python
theme:
  minipost: true
---

Here's a problem I solved today: I have a CSV file to parse which contained UTF-8 strings, and I want to parse it using Python.
I want to do it in a way that works in both Python 2.7 and Python 3.

This proved to be non-trivial, so this blog post is a quick brain dump of what I did, in the hope it's useful to somebody else and/or my future self.

## Problem statement

Consider the following minimal example of a CSV file:

```csv
1,alïce
2,bøb
3,cárol
```

We want to parse this into a list of lists:

```python
[
    ["1", "alïce"],
    ["2", "bøb"],
    ["3", "cárol"],
]
```

## Experiments

The following code can read the file in Python 2.7; here we treat the file as a bag of bytes and only decode after the CSV parsing is done:

```python
import csv

with open("example.csv", "rb") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    for row in csvreader:
        row = [entry.decode("utf8") for entry in row]
        print(": ".join(row))
```

But if you run that code in Python 3, you get the following error:

```
Traceback (most recent call last):
  File "reader2.py", line 6, in <module>
    for row in csvreader:
_csv.Error: iterator should return strings, not bytes (did you open the file in text mode?)
```

The following code can read the file in Python 3:

```python
import csv

with open("example.csv", encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    for row in csvreader:
        print(": ".join(row))
```

But the `encoding` argument to `open()` is only in Python 3 or later, so you can't use this in Python 2.

In theory this is backported as [`codecs.open()`](https://docs.python.org/3/library/codecs.html#codecs.open), but I get a different error if I use `codecs.open()` in this file with Python 2.7:

```
Traceback (most recent call last):
  File "reader3.py", line 7, in <module>
    for row in csvreader:
UnicodeEncodeError: 'ascii' codec can't encode character u'\xef' in position 4: ordinal not in range(128)
```

This feels like it should be possible using only the standard library, but it was becoming sufficiently complicated that I didn't want to bother.

I considered defining these as two separate functions, and running:

```python
import sys

if sys.version_info[0] == 2:
    read_csv_python2()
else:
    read_csv_python3()
```

but that felt a little icky, and would have been annoying for code coverage.
Having two separate functions also introduces a source of bugs -- I might remember to update one function, but not the other.

I found [csv23](https://pypi.org/project/csv23/) on PyPI, whose description sounded similar to what I wanted.
The following snippet does what I want:

```python
import csv23

with csv23.open_reader("example.csv") as csvreader:
    for row in csvreader:
        print(": ".join(row))
```

This reads the CSV file as UTF-8 in both Python 2 and 3.
Having a third-party library is mildly annoying, but it's easier than trying to write, test and maintain this functionality myself.

## tl;dr

Python 2 only:

```python
import csv

with open("example.csv", "rb") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    for row in csvreader:
        row = [entry.decode("utf8") for entry in row]
        print(": ".join(row))
```

Python 3 only:

```python
import csv

with open("example.csv", encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    for row in csvreader:
        print(": ".join(row))
```

Both Python 2 and 3:

```python
import csv23

with csv23.open_reader("example.csv") as csvreader:
    for row in csvreader:
        print(": ".join(row))
```
