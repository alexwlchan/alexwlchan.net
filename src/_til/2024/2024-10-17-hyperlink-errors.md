---
layout: til
title: What errors can you get from `hyperlink.parse`?
summary: |
  Mostly you get `hyperlink.URLParseError`, but you can occasionally get a `ValueError` as well.
date: 2024-10-17 10:32:56 +01:00
date_updated: 2024-11-27 11:24:15 +00:00
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

But it can throw exceptions:

*   It throws a `URLParseError` for most invalid URLs:

    ```pycon
    >>> hyperlink.parse("http://http://")
    …
    hyperlink._url.URLParseError: port must not be empty: 'http:'
    ```

*   It throws a `ValueError` in a handful of cases, if you give it in an invalid scheme, say by extra whitespace or invalid characters:

    ```pycon
    >>> hyperlink.parse(" http://")
    …
    ValueError: invalid scheme: ' http'. Only alphanumeric, "+", "-", and "." allowed. Did you meant to call URL.from_text()?

    >>> hyperlink.parse("h_t_t_p://")
    …
    ValueError: invalid scheme: 'h_t_t_p'. Only alphanumeric, "+", "-", and "." allowed. Did you meant to call URL.from_text()?
    ```

*   It throws a `TypeError` if you pass a value that isn't a `str`:

    ```pycon
    >>> hyperlink.parse(b"")
    …
    TypeError: expected str for text, got b''
    ```

    All of my new code is type checked, so it's unlikely I'd encounter this in practice.

*   It throws a `UnicodeDecodeError` if you pass a value which can't be decoded in UTF-8:

    ```pycon
    >>> hyperlink.parse('%AD')
    …
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xad in position 0: invalid start byte
    ```

    I discovered this when looking at URLs that have returned 404 errors on my website -- somebody was trying to stuff in what looked like an exploit and it threw an error when I tried to analyse it.

Given that `URLParseError` and `UnicodeDecodeError` are subclasses of `ValueError`, it would be sensible to wrap calls to `hyperlink.parse` with `try … except ValueError`.
Based on a cursory read of the hyperlink source code, I can't see any places where it could throw a different exception type -- but I missed the possibility of the Unicode error, so maybe there are more I haven't found.
