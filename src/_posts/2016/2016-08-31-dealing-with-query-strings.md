---
layout: post
date: 2016-08-31 20:05:00 +0000
tags: python
title: 'Python snippet: dealing with query strings in URLs'
theme:
  minipost: true
---

I spend a lot of time dealing with URLs: in particular, with URL [query strings][wiki_qs].
The query string is the set of key-value pairs that comes after the question mark in a URL.
For example:

<pre>
http://example.net?<strong>name=alex&amp;color=red</strong>
</pre>

Typically I want to do one of two things: get the value(s) associated with a particular key, or create a new URL with a different key-value pair.

This is possible with the Python standard library's [`urllib.parse`][url_parse] module, but it's a bit fiddly and requires chaining several functions together.
Since I do this fairly often, I have a pair of helper functions that I copy-and-paste into new projects when I need to do this.
And since it's fairly generic, I thought it might be worth sharing more widely.

<!-- summary -->

### Get the value(s) associated with a particular key

It's easy to imagine a query string as like a Python dict: it's a series of key-value pairs.
But unlike a dictionary, the same key can appear twice in the same query string.
For example, this is perfectly legal:

<pre>
http://example.net?<strong>name=alex&amp;name=anna</strong>
</pre>

So we might have a single value associated with a given key, or multiple values.
The most flexible approach is to return a list of values associated with a key, and let the caller decide which (if any of them) they care about.
Doing so requires chaining together a couple of standard library functions, and looks like this:

```python
from urllib.parse import parse_qs, urlparse


def get_query_field(url, field):
    try:
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []
```

I used the term "field" rather than "key" because that's what the [Wikipedia article][wiki_qs] uses, although I don't actually see that terminology in [RFC&nbsp;3986][rfc3986].

### Setting the value for a particular key

Setting a value takes slightly more work: quite a few calls into bits of `urllib`, then constructing an entirely new tuple of URL components to "unparse".
This is what the code looks like:

```python
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def set_query_field(url, field, value, replace=False):
    # Parse out the different parts of the URL.
    components = urlparse(url)
    query_pairs = parse_qsl(urlparse(url).query)

    if replace:
        query_pairs = [(f, v) for (f, v) in query_pairs if f != field]
    query_pairs.append((field, value))

    new_query_str = urlencode(query_pairs)

    # Finally, construct the new URL
    new_components = (
        components.scheme,
        components.netloc,
        components.path,
        components.params,
        new_query_str,
        components.fragment
    )
    return urlunparse(new_components)
```

Because the same key can appear twice, when you're adding a new key-value pair, you have to decide whether to just add another pair, or replace the existing pair (if it exists): that's what the `replace` parameter is for.
If it's `False`, any existing pairs are preserved, and the new pair is added to the end of the URL.
If it's `True`, all the existing pairs with the same key are discarded before adding the new pair.

There are definitely some edge cases this doesn't cover – for example, if the exact ordering matters, or you only want to replace the first instance of an existing key – but in practice, this covers all of my usage.
I'll need extra code if I want something more complicated.

### Getting the code

The complete code [is in a Gist][gist].
That includes docstrings, usage examples, and imports for Python 2/3 compatibility.
Only requires standard library imports.

When I use this code, I just copy and paste it into the new project; there's no PyPI module.
It's too small to matter, and in general I don't like having lots of small dependencies.

[wiki_qs]: https://en.wikipedia.org/wiki/Query_string
[url_parse]: https://docs.python.org/3.5/library/urllib.parse.html
[rfc3986]: https://tools.ietf.org/html/rfc3986#section-3.4
[gist]: https://gist.github.com/alexwlchan/1956efe1acb1f2947cbd575651a3d529
[leftpad]: http://www.theregister.co.uk/2016/03/23/npm_left_pad_chaos/