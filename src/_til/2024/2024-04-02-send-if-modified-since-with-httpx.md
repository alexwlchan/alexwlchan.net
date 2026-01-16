---
layout: til
date: 2024-04-02 18:55:13 +01:00
title: Checking if a URL has changed when you fetch it over HTTP
summary: |
  When you make an HTTP request, you can use the `If-Modified-Since` header to get a 304 Not Modified if nothing has changed since your last request.
tags:
  - http
  - python
  - python:httpx
---
I was writing a small crawler for my RSS feed, and I know my RSS feed doesn't change that often, so I was looking for a way to speed up fetches when nothing has changed.

I had a vague recollection that there's something for this in vanilla HTTP, and that led me to rediscover the [`If-Modified-Since` header][header].
If you send this header in your request, and the URL hasn't changed, you get an HTTP 304 Not Modified rather than a 200 OK:

```console
$ curl -s -o /dev/null -w "%{http_code}\n" "https://alexwlchan.net/atom.xml"
200

$ curl -s -o /dev/null -w "%{http_code}\n" -H "If-Modified-Since: Tue, 2 Apr 2024 19:05:00 GMT" "https://alexwlchan.net/atom.xml"
304
```

In my limited testing, adding the `If-Modified-Since` header made my requests a bit faster -- not a lot, but not zero.
Handy!

[header]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Modified-Since

## Getting the format of the header right

The header is very particular about how you format the date.
Here's the syntax from MDN:

```
If-Modified-Since: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
```

And here's their example:

```
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
```

One thing of note is that the timezone is always GMT: *HTTP dates are always expressed in GMT, never in local time*.
When I was testing against my site hosted on Netlify, it would ignore the timezone and treat it as GMT regardless.

Here's how to construct the header in various languages:

*   Python:

    ```python
    import datetime

    now = datetime.datetime.now(datetime.UTC)  # GMT and UTC are the same
    if_modified_since = now.strftime("%a, %d %b %Y %H:%M:%S %Z")
    ```

*   Bash/shell scripting:

    ```shell
    TZ=GMT date +"%a, %d %b %Y %H:%M:%S %Z"
    ```

## Some Python snippets

I was writing my feed crawler in Python, so I ended up building this behaviour around [httpx](https://www.python-httpx.org/), the HTTP client I was using at the time.

Here's a little snippet I wrote to test this behaviour:

```python
import datetime

import httpx


client = httpx.Client()

resp = client.get("https://alexwlchan.net/atom.xml")
print(resp)  # <Response [200 OK]>

now = datetime.datetime.now(datetime.UTC)
client.headers["If-Modified-Since"] = now.strftime("%a, %d %b %Y %H:%M:%S %Z")

resp = client.get("https://alexwlchan.net/atom.xml")
print(resp)  # <Response [304 Not Modified]>
```

I haven't settled on a good pattern for using these 304 responses.
In some cases, it's enough to know that I got a 304 and nothing needs to be done.
In other cases, I might need to retrieve a previously cached response from somewhere.
I'm not entirely sure how I'll use it.