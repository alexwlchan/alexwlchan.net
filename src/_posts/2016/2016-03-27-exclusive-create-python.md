---
date: 2016-03-27 10:33:00 +0000
layout: post
slug: exclusive-create-python
summary: If you want to create a file, but only if it doesn't already exist, Python
  3 has a helpful new file mode `x`.
tags: python
title: Exclusively create a file in Python 3
---

I've been tidying up a lot of old Python code recently, and I keep running into this pattern:

```python
if not os.path.exists('newfile.txt'):
    with open('newfile.txt', 'w') as f:
        f.write('hello world')
```

The program wants to write some text to this file, but only if nobody's written to it before – they don't want to overwrite the existing contents.
This approach is very sensible: if we check that the file exists before writing, we can avoid scribbling over a pre-existing file.

But this code is subject to a race condition: if the file pops into existence between the `if` and the `open()`, we scribble all over it anyway.

To catch this race condition, Python 3.3 [added a new file mode](https://docs.python.org/3/whatsnew/3.3.html#io): `x` for exclusive creation.
If you open a file in mode `x`, the file is created and opened for writing – but *only* if it doesn't already exist.
Otherwise you get a FileExistsError.

Here's how I'd rewrite the snippet above:

```python
try:
    with open('newfile.txt', 'x') as f:
        f.write('hello world')
except FileExistsError:
    print('File already exists.  Clean up!')
```

Using the `x` mode means you can be sure that you won't override an existing file.
It's safer than the existence check.

I probably won't use this a lot, but when I do, I'll appreciate it.
This has been my general experience with Python 3: there's no killer feature that I can't live without, just a growing pile of small niceties that I miss when I go back to Python 2.