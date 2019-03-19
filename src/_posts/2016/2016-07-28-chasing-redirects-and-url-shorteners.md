---
layout: post
date: 2016-07-28 21:03:00 +0000
summary: A quick Python function to follow a redirect to its eventual conclusion.
tags: python
title: 'Python snippets: Chasing redirects and URL shorteners'
theme:
  minipost: true
category: Programming and code
---

Quick post today.
A few years back, there was a proliferation of link shorteners on Twitter: tinyurl, bit.ly, j.mp, goo.gl, and so on.
When characters are precious, you don't want to waste them with a long URL.
This is frustrating for several reasons:

*   It becomes harder to see where a particular link goes.
*   If the link shortener goes away, all the links break, even if the pages behind the links are still up.
*   Often the same link would be wrapped multiple times: a j.mp link would redirect to goo.gl, then adf.ly, before finally getting to the destination.

Twitter have tried to address this with their [t.co link shortener](https://en.wikipedia.org/wiki/Twitter#URL_shortener).
All links in Twitter get wrapped with t.co, so long URLs no longer penalise your character count, and they show a short preview of the destination URL.
But this is still fragile &ndash; Twitter may not last forever &ndash; and people still wrap links in multiple shorteners.

When I'm storing data with shortened links, I like to record where the link is supposed to go.
I keep the shortened and the resolved link, which tends to be pretty future-proof.

To find out where a shortened URL goes, I could just open it in a web browser.
But that's slow and manual, and doesn't work if I want to save the URL as part of a scripted pipeline.
So I have a couple of utility functions to help me out.

<!-- summary -->

All the good link shorteners use [HTTP&nbsp;3XX redirects](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#3xx_Redirection) to send you to the next URL in the chain.
A lot of HTTP libraries will just follow those if you make a GET request, so it's enough to make a GET request and see where you end up.
Here's what that looks like with [python-requests](http://docs.python-requests.org/en/master/):

```python
import requests

def resolve_url(base_url):
    r = requests.get(base_url)
    return r.url

if __name__ == '__main__':
    import sys
    print(resolve_url(sys.argv[1]))
```

When run from the command-line, this just prints the final URL.

Sometimes I also want to see the intermediate links involved in the resolution: for example, if a site "helpfully" redirects any broken pages to a generic 404.
In that case, I make individual HEAD requests and follow the redirects manually:

```python
import requests

def chase_redirects(url):
    while True:
        yield url
        r = requests.head(url)
        if 300 < r.status_code < 400:
            url = r.headers['location']
        else:
            break

if __name__ == '__main__':
    import sys
    for url in chase_redirects(sys.argv[1]):
        print(url)
```

This prints each URL involved in the chain.
It's useful for debugging a particular URL, or working out where a redirect chain falls over.
I don't use it as much, but it's useful to have around.

There are definitely weird setups where these functions fall over (for example, a pair of pages which redirect to each other), but in the vast majority of cases they're completely fine.

I have these two scripts saved as `resolve_url` and `chase_url`.
I can invoke them from a shell prompt, or incorporate them in scripts.
They're handy little programs: incredibly simple, quick, and perform one task very well.