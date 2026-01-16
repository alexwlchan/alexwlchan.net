---
layout: til
title: How to stream lines from stdout with `subprocess`
summary: Use `subprocess.Popen()` with `bufsize=1` and `text=True`, then you can interate over the lines with `proc.stdout`.
date: 2025-05-17 14:50:11 +01:00
tags:
  - python
---
I was writing a Python script that shells out to external tool which prints output line-by-line to stdout.
I wanted my script to read those lines, and then do some follow-up work for each line.

I know several ways to run an external process and capture the stdout with the [`subprocess` module][subprocess], but they're all blocking -- I have to wait for the entire process to complete.
This is annoying and inefficient if the external tool is slow.
Ideally I'd like to stream lines from the external tool; to start my follow-up work as soon as there's a line available.

Today I discovered that if you start a process with [`subprocess.Popen()`][popen], and you pass `bufsize=1` and `text=True`, then the stdout will be line-buffered.
This allows you to iterate over lines as they're written, rather than waiting for all of them.

Here's an example:

```python
import subprocess

args = ["yt-dlp", "--get-id", "https://www.youtube.com/watch?list=PLCbA9r6ecYWU6SVyvb32a0YHIzpr9jxnW"]

proc = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1, text=True)

for line in proc.stdout:
    print(line)

proc.poll()
print(proc.returncode)
```

[subprocess]: https://docs.python.org/3/library/subprocess.html#module-subprocess
[popen]: https://docs.python.org/3/library/subprocess.html#subprocess.Popen
