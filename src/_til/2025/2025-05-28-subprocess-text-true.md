---
layout: til
title: Use `text=true` with `subprocess` functions to get stdout/stderr as str, not bytes
date: 2025-05-28 20:12:29 +0100
tags:
  - python
---
I often use the [`subprocess` module][subprocess] to capture the output of external processes in Python, for example:

{% code lang="pycon" names="0:subprocess" %}
>>> import subprocess
>>> subprocess.check_output(["echo", "hello world"])
b'hello world\n'
{% endcode %}

This returns the output as `bytes`, and so I usually have to decode the output to get a `str`.
(And I can never remember whether I need to encode/decode when converting `bytes` to `str`, so I get it wrong half the time.)

I recently discovered I can pass `text=true` to `subprocess` functions, and it does the work of decoding the output for me.
For example:

{% code lang="pycon" %}
>>> subprocess.check_output(["echo", "hello world"], text=True)
'hello world\n'
{% endcode %}

It's a small thing, but it'll make all my scripts that use `subprocess` a bit easier to follow.

(I discovered this option when I learnt that you can iterate over `subprocess` output [line-by-line](/til/2025/subprocess-line-by-line/).)

[subprocess]: https://docs.python.org/3/library/subprocess.html#module-subprocess