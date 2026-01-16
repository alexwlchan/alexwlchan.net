---
layout: til
title: Write to the middle of a file with Python
date: 2024-08-09 00:42:31 +01:00
summary: Open the file with mode `r+` to be able to seek around the file and write to it.
tags:
  - python
---
When you open a file in Python, you can use mode `+` to open the file for updating -- you can move around the file and write to parts of it selectively, without having to rewrite the entire file.
This allows you to make changes in the middle of a file.

Here's an example program:

```python
with open("greeting.txt", "w") as out_file:
    out_file.write("hello world")

with open("greeting.txt") as in_file:
    print(repr(in_file.read()))

with open("greeting.txt", "r+") as out_file:
    out_file.write("howdy")

with open("greeting.txt") as in_file:
    print(repr(in_file.read()))

with open("greeting.txt", "r+") as out_file:
    out_file.seek(6)
    out_file.write("sarah")

with open("greeting.txt") as in_file:
    print(repr(in_file.read()))
```

And the output:

```console
$ python3 example.py
'hello world'
'howdy world'
'howdy sarah'
```

This also works with `rb+` if you want to write binary data.

Compare to the other two modes for writing to files:

*   `w` will truncate the file, forcing you to write the whole thing from scratch
*   `a` will only append to the file, even if you seek through it
