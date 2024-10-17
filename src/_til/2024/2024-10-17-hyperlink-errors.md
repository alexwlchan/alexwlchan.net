---
layout: til
title: What errors can you get from `hyperlink.parse`?
summary: |
  Mostly you get `hyperlink.URLParseError`, but you can occasionally get a `ValueError` as well.
date: 2024-10-17 10:32:56 +0100
tags:
  - python
  - python:hyperlink
---
I write a lot of code that uses [`hyperlink.parse`](https://pypi.org/project/hyperlink/).
I want to make sure my code can handle all the exceptions which are thrown by hyperlink, and react accordingly.

The hyperlink URL parser is fairly robust, and handles quite a few strings that don't look like URLs to me, for example:

```pycon
>>> import hyperlink
>>> hyperlink.parse("")
DecodedURL(url=URL.from_text(''))
```

It throws a `URLParseError` for most invalid URLs:

```pycon
>>> hyperlink.parse("http://http://")
…
hyperlink._url.URLParseError: port must not be empty: 'http:'
```

It throws a `ValueError` in a handful of cases, if you include whitespace in the scheme:

```pycon
>>> hyperlink.parse(" http://")
…
ValueError: invalid scheme: ' http'. Only alphanumeric, "+", "-", and "." allowed. Did you meant to call URL.from_text()?
```

It throws a `TypeError` if you pass a value that isn't a `str`:

```pycon
>>> hyperlink.parse(b"")
…
TypeError: expected str for text, got b''
```

All of my new code is type checked, so it's unlikely I'd encounter this in practice.

Given that `URLParseError` is a subclass of `ValueError`, it would be sensible to wrap calls to `hyperlink.parse` with `try … except ValueError`.
Based on a cursory read of the hyperlink source code, I can't see any places where it could throw a different exception type.
