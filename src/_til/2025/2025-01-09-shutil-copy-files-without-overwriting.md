---
layout: til
title: Use `shutil.copyfileobj` and `xb` to avoid overwriting files when copying in Python
date: 2025-01-09 16:30:03 +0000
tags:
  - python
---
If you want to copy a file but be sure you're never going to overwrite an existing file at the destination, use [`shutil.copyfileobj(src, dst)`](https://docs.python.org/3/library/shutil.html#shutil.copyfileobj).
This function requires you to pass file-like objects, so you can open the destination file with exclusive creation mode&nbsp;`x`.
This will throw a `FileExistsError` error if the destination file already exists.

Here's a minimal example:

```console?prompt=$
$ cat copy_file.py
import shutil

with open("src.txt", "rb") as src, open("dst.txt", "xb") as dst:
    shutil.copyfileobj(src, dst)

$ echo 'hello world' > src.txt

$ python3 copy_file.py

$ cat dst.txt
hello world

$ python3 copy_file.py
Traceback (most recent call last):
  File "copy_file.py", line 6, in <module>
    open("dst.txt", "xb") as dst
    ~~~~^^^^^^^^^^^^^^^^^
FileExistsError: [Errno 17] File exists: 'dst.txt'
```

{% comment %}
```python
import shutil

with (
    open("src.txt", "rb") as src,
    open("dst.txt", "xb") as dst
):
    shutil.copyfileobj(src, dst)
```

And here's what happens if you run it:

```console
$ echo 'hello world' > src.txt

$ python3 copy_file.py

$ cat dst.txt
hello world

$ python3 copy_file.py
Traceback (most recent call last):
  File "copy_file.py", line 6, in <module>
    open("dst.txt", "xb") as dst
    ~~~~^^^^^^^^^^^^^^^^^
FileExistsError: [Errno 17] File exists: 'dst.txt'
```
{% endcomment %}

## Why not use `os.path.exists()`?

A common pattern for this sort of check is to call `os.path.exists()` before doing the file copy.
For example, here's some code that was suggested by Claude when I asked about this problem:

```python
import os
import shutil

if not os.path.exists(dst):
    shutil.copy(src, dst)
```

But this introduces a race condition.
What if a file appears at `dst` after you call `os.path.exists`, but before you call `shutil.copy`?
Then it would be overwritten.

This is a class of bug known as [time-of-check to time-of-use](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use).
