---
layout: til
title: Use `typing.getargs()` to get a list of `typing.Literal[…]` values
date: 2025-06-25 14:20:15 +0100
tags:
  - python
  - python:typing
---
Here's a [handy little function](https://docs.python.org/3/library/typing.html#typing.get_args) I discovered while reading the docs for the `typing` module:

```python
>>> import typing

>>> Color = typing.Literal['red', 'green', 'blue']

>>> typing.get_args(Color)
('red', 'green', 'blue')
```

I use `typing.Literal` in a bunch of places, and being able to iterate through the values like this could be really helpful.
