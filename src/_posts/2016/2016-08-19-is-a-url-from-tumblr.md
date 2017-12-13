---
date: 2016-08-19 23:34:00 +0000
layout: post
tags: tumblr python
title: 'Python snippets: Is a URL from a Tumblr post?'
theme:
  minipost: true
---

I've been writing some code recently that takes a URL, and performs some special actions if that URL is a Tumblr post.
The problem is working out whether a given URL points to Tumblr.

Most Tumblrs use a consistent naming scheme: `username.tumblr.com`, so I can detect them with a regular expression.
But some Tumblrs use custom URLs, and mask their underlying platform: for example, <http://travelingcolors.net> or <http://wordstuck.co.vu>.
Unfortunately, I encounter enough of these that I can't just hard-code them, and I really should handle them properly.

So how can I know if an arbitrary URL belongs to Tumblr?

I've had to do this a couple of times now, so I thought it was worth writing up what to do – partly for my future reference, partly in case anybody else finds it useful.

In the HTTP headers on a Tumblr page, there are a couple of "X-Tumblr" headers.
These are custom headers, defined by Tumblr – they aren't part of the official HTTP spec.
They aren't documented anywhere, but it's clear who's sending them, and I'd be quite surprised to see another site send them.
For my purposes, this is a sufficiently reliable indicator.

So this is the function I use to detect Tumblr URLs:

```python
try:
    from urllib.parse import urlparse
except ImportError:  # Python 2
    from urlparse import urlparse

import requests


def is_tumblr_url(url):
    if urlparse(url).netloc.endswith('.tumblr.com'):
        return True
    else:
        req = requests.head(url)
        return any(h.startswith('X-Tumblr') for h in req.headers)
```

It's by no means perfect, but it's a step-up from basic string matching, and accurate and fast enough that I can usually get by.
