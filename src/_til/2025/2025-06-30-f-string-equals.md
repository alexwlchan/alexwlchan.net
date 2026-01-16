---
layout: til
title: Python's f-strings support `=` for self-documenting expressions
date: 2025-06-30 15:52:12 +01:00
summary: The f-string `f"{x=}"` expands to `f"x={x}"`.
tags:
  - python
---
I was reading [PEP 736](https://peps.python.org/pep-0736/#prior-art), a rejected proposal for a shorthand syntax for keyword arguments, and it mentioned a new-to-me bit of prior art:

> Python already possesses a very similar feature in f-string interpolation where `f'{x=}'` is effectively expanded to `f'x={x}'` (see [related GitHub issue](https://github.com/python/cpython/issues/80998)).

It supports both single variables and more complex expressions.
Here's a few examples:

```pycon
>>> x = 42
>>> f"{x=}"
'x=42'
>>> f"{1+2=}"
'1+2=3'
>>> f"{(1+2)*3=}"
'(1+2)*3=9'
```

This is described in [What's New In Python 3.8](https://docs.python.org/3/whatsnew/3.8.html#f-strings-support-for-self-documenting-expressions-and-debugging); this feature was realised nearly six years ago but I've never come across it before.
