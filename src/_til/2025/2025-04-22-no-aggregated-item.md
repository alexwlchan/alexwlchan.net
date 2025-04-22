---
layout: til
title: The error "No aggregated item, sequence was empty" comes from Jinja2
summary: |
  You get this error message if you try to use Jinja2's filters to get the min/max of an empty sequence.
date: 2025-04-22 09:59:52 +0100
tags:
  - python
  - python:jinja
---
I was debugging a Python app today, and I got an error message in my logs that I didn't recognise:

```
jinja2.exceptions.UndefinedError: No aggregated item, sequence was empty.
```

I didn't recognise this error, and I couldn't find anything about it in Google either.
I figured I'd write a few notes on where it came from.

## What causes this error?

After looking at the traceback, I was able to reduce this to a minimal example -- it comes from the Jinja2 `min()` and `max()` filters.
In particular, if you try to get the min/max of an empty sequence, you get this error rather than Python's usual "iterable is empty".

Here's an example:

```python
import jinja2

t = jinja2.Template("{% raw %}{{ 1 + (my_list|max) }}{% endraw %}")

print(t.render(my_list=[]))
```

Note that the `1 +` is required to cause the error -- you have to interact with the `my_list|max` value, otherwise it's undefined and gets rendered as an empty string.

If I'd remembered to [enable StrictUndefined][StrictUndefined] in this codebase, the error would be thrown even if I just rendered the value in the template, and didn't try to modify it.
For example:

```python
import jinja2

t = jinja2.Template("{% raw %}{{ my_list|max }}{% endraw %}", undefined=jinja2.StrictUndefined)

print(t.render(my_list=[]))
```

[StrictUndefined]: /2022/strict-jinja/

## Where does this error come from?

Once I knew this error came from Jinja2, I was able to search the Jinja2 codebase and [find the function][_min_or_max] where this error is being returned:

```python
def _min_or_max(
    environment: "Environment",
    value: "t.Iterable[V]",
    ...
) -> "t.Union[V, Undefined]":
    it = iter(value)

    try:
        first = next(it)
    except StopIteration:
        return environment.undefined("No aggregated item, sequence was empty.")

    ...
```

Until I saw this code, I didn't realise `Undefined` was an actual type -- I've only ever encountered it in the sense of "undefined variable", which is a fairly common programming error.

Digging into this a little further, I discovered that there's a class [`jinja2.Undefined`][Undefined], which is [used in several places][search] beyond "your template tried to use a variable that doesn't exist".

The documentation also explains why, when I wasn't using `StrictUndefined`, I had to interact with the variable before I could throw an error (emphasis mine):

> `class jinja2.Undefined` – The default undefined type. This can be printed, iterated, and treated as a boolean. **Any other operation will raise an UndefinedError.**

This is an interesting idea that I don't think I've come across before.
It's an empty value like `None` or `undefined` in other languages, but it includes an error message that can be helpful for debugging. 

[_min_or_max]: https://github.com/pallets/jinja/blob/220e67ae999c24e4077d7bf5bdc932757b65a338/src/jinja2/filters.py#L486-L503]
[Undefined]: https://jinja.palletsprojects.com/en/stable/api/#jinja2.Undefined
[search]: https://github.com/search?q=repo%3Apallets%2Fjinja%20environment.undefined&type=code
