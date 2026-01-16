---
layout: til
title: Print a comma-separated number in Python with `{num:,}`
summary: You can use `{num:,}` to insert a comma every three digits, `{num:_}` to insert an underscore every three digits, and `{num:n}` to insert a locale-aware digit separator.
date: 2025-05-28 17:39:19 +01:00
tags:
  - python
---
## Insert a comma every three digits

I forget exactly how I discovered this, but if you want to pretty-print a number with commas every three digits in Python, you can use the `,` format specifier.
For example:

```pycon
>>> num = 123456789
>>> f"{num:,}"
'123,456,789'
```

This will [always insert a comma](https://docs.python.org/3/library/string.html), regardless of locale.

## Insert an underscore every three digits

There's a similar option which inserts underscores every three digits:

```pycon
>>> f"{num:_}"
'123_456_789'
```

This could be useful when writing custom `__repr__` methods -- Python allows you to insert underscores in long numbers to make them more readable:

```pycon
>>> 123_456_789
123456789
>>> eval('123_456_789')
123456789
```

## Insert a locale-aware digit separator

The `,` and `_` format specifiers are both fixed; they always use the same character as a digit separator.

If you use the `n` format specifier, you get a locale-aware digit separator every three digits.

When I start a new Python REPL session, there's no locale, so there's no digit separator:

```pycon
>>> f"{num:n}"
'123456789'
```

If I set the locale to British English, I see the commas I'm familiar with:

```pycon
>>> import locale
>>> locale.setlocale(locale.LC_NUMERIC, "en_GB")
>>> f"{num:n}"
'123,456,789'
```

If I set the locale to French, I see thin spaces:

```pycon
>>> locale.setlocale(locale.LC_NUMERIC, "fr_FR")
>>> f"{num:n}"
'123\u202f456\u202f789'
>>> print(_)
123 456 789
```

If I set the locale to Swiss German, I see apostrophes:

```pycon
>>> locale.setlocale(locale.LC_NUMERIC, "de_CH")
'de_CH'
>>> f"{num:n}"
'123’456’789'
```

And so on.

## Will I use this?

In the past I've used the [humanize library](https://github.com/python-humanize/humanize) for this sort of pretty printing, specifically the `intcomma()` function:

```pycon
>>> import humanize
>>> humanize.intcomma(123456789)
'123,456,789'
```

This means a third-party dependency, but I like the explicitness of this code. If you don't know what this does, it's probably easier to look up this function than try to find Python's string format specifiers.
(I struggled to find the reference page, despite knowing what I was looking for!)

It's also much harder to delete or typo -- it's obvious that this formatting is doing *something*, and isn't just a copy-paste error or similar.

Maybe next time I have to do this, I write my own `intcomma()` function which uses the builtin format specifier, and includes an explanatory comment and link to the Python docs.
