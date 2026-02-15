---
layout: note
title: Use `typing.getargs()` to get a list of `typing.Literal[…]` values
date: 2025-06-25 14:20:15 +01:00
topic: Python
---
Here's a [handy little function](https://docs.python.org/3/library/typing.html#typing.get_args) I discovered while reading the docs for the `typing` module:

```pycon {"names":{"1":"typing","2":"Color"}}
>>> import typing

>>> Color = typing.Literal['red', 'green', 'blue']

>>> typing.get_args(Color)
('red', 'green', 'blue')
```

I use `typing.Literal` in a bunch of places, and being able to iterate through the values like this could be really helpful.
