---
layout: til
date: 2024-07-05 12:29:09 +01:00
title: Build a URL with query string parameters with curl
summary: |
  A combination of `--get` and `--data`/`--data-urlencode` allows you to write curl commands which are readable and expressive.
tags:
  - curl
---
I want to write an HTTP GET in curl which:

*   somebody can copy/paste to run themselves
*   would allow somebody else to make the same request in their HTTP library of choice
*   has easily readable URL query parameters

How can I do that with curl?

## Motivation

I'm writing some documentation for the Wikimedia Commons API, and I want to include some runnable examples.
The various query parameters get baked into a single GET URL, but that makes it quite difficult to see what's going on:

{% code lang="shell" wrap="true" %}
curl 'https://commons.wikimedia.org/w/api.php?action=query&list=logevents&letitle=File%3AMugeni%20Elijah%20-%20Behind%20tha%20sin%20ArtWork.png&format=xml&letype=delete'
{% endcode %}

There are five query parameters being passed to that URL!
But this syntax makes it quite difficult to read and translate into another HTTP library.

In Python, I'm used to expressing the query parameters as a structured object (which also handles the URL encoding for you), for example:

{% code lang="python" names="0:httpx" %}
import httpx

httpx.get(
    "https://commons.wikimedia.org/w/api.php",
    params={
        "action": "query",
        "list": "logevents",
        "letitle": "File:Mugeni Elijah - Behind tha sin ArtWork.png",
        "format": "xml",
        "letype": "delete"
    }
)
{% endcode %}

Compared to the curl command, this is easier for somebody to read and translate to another language, but it's harder to copy/paste for a quick experiment.

## Solution

I looked at the [curl manpage](https://curl.se/docs/manpage.html), and I found the [`-G`, `--get` flag](https://curl.se/docs/manpage.html#-G) (emphasis mine):

> When used, this option makes all data specified with `-d`, `--data`, `--data-binary` or `--data-urlencode` to be used in an HTTP GET request instead of the POST request that otherwise would be used. **curl appends the provided data to the URL as a query string.**

This allows me to write the curl command in a more verbose, expressive way so somebody can see what's going on:

```shell
curl --get 'https://commons.wikimedia.org/w/api.php' \
  --data 'action=query' \
  --data 'list=logevents' \
  --data-urlencode 'letitle=File:Mugeni Elijah - Behind tha sin ArtWork.png' \
  --data 'format=xml' \
  --data 'letype=delete'
```

(The `--data-urlencode` flag was a bonus discovery, which saves me from URL encoding parameters by hand.)
