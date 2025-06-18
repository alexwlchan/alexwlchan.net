---
layout: til
title: The error "No aggregated item, sequence was empty" comes from Jinja2
summary: |
  You get this error message if you try to use Jinja2's filters to get the min/max of an empty sequence.
date: 2025-06-18 07:42:59 +0100
tags:
  - python
  - python:jinja
---
I was debugging a Python app recently, and I saw an error message in my logs that I didn't recognise:

```
jinja2.exceptions.UndefinedError: No aggregated item, sequence was empty.
```

I didn't recognise this error, and I couldn't find anything about it in Google either.
(The only search result for this error is a [forum thread about home automation](https://community.home-assistant.io/t/templateerror-undefinederror-no-aggregated-item-sequence-was-empty-while-processing-template/487681), which has the same issue which only hints at the issue.)

I did some debugging and I worked out where it came from -- here are my notes.

## What causes this error?

In my traceback, I could see this was coming from Jinja2's `min()` and `max()` filters.
If you try to get the min and max of an empty list, that causes the error:

```python
import jinja2

t = jinja2.Template("{% raw %}{{ 1 + (my_list|max) }}{% endraw %}")

print(t.render(my_list=[]))
```

Note that the `1 +` is required to cause the error -- you have to interact with the `my_list|max` value, otherwise it's undefined and gets rendered as an empty string.

If I'd [enabled `StrictUndefined`][StrictUndefined], the error would be thrown even if I just rendered the value in the template, and didn't try to modify it.
Here's another example:

```python
import jinja2

t = jinja2.Template("{% raw %}{{ my_list|max }}{% endraw %}", undefined=jinja2.StrictUndefined)

print(t.render(my_list=[]))
```

The fix is to ensure you're not trying to get the `min()` or `max()` of an empty list -- if you're not certain the input list will be non-empty, add a check beforehand.

[StrictUndefined]: /2022/strict-jinja/

## Where does this error come from?

Once I knew this error came from Jinja2, I was able to search the Jinja2 codebase and [find the function][_min_or_max] where this error is being returned:

{%
  annotatedhighlight
  lang="python"
  line_numbers="486-488,492-498"
  src="https://github.com/pallets/jinja/blob/220e67ae999c24e4077d7bf5bdc932757b65a338/src/jinja2/filters.py#L486-L503"
%}
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
{% endannotatedhighlight %}

Until I saw this code, I didn't realise `Undefined` was an actual type -- I've only ever encountered it in the sense of "undefined variable", which is a fairly common programming error, and not necessarily associated with a type.

Digging into this a little further, I discovered that there's a class [`jinja2.Undefined`][Undefined], which is [used in several places][search] beyond "your template tried to use a variable that doesn't exist".

The documentation also explains why, when I wasn't using `StrictUndefined`, I had to interact with the variable before I could throw an error (emphasis mine):

> `class jinja2.Undefined` – The default undefined type. This can be printed, iterated, and treated as a boolean. **Any other operation will raise an UndefinedError.**

This is an interesting idea that I don't think I've come across before.
There are lots of languages that have an empty value like `null` or `undefined`, but I can't recall seeing any where you can attach an error message that can be used for debugging.
It feels similar to something like an `Option` or an `Err` type, but a value being undefined isn't necessarily an error.

[_min_or_max]: https://github.com/pallets/jinja/blob/220e67ae999c24e4077d7bf5bdc932757b65a338/src/jinja2/filters.py#L486-L503]
[Undefined]: https://jinja.palletsprojects.com/en/stable/api/#jinja2.Undefined
[search]: https://github.com/search?q=repo%3Apallets%2Fjinja%20environment.undefined&type=code
