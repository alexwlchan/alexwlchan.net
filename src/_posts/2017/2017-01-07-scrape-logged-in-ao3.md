---
date: 2017-01-07 23:10:00 +0000
layout: post
minipost: true
summary: AO3 doesn't have an official API for scraping data - but with a bit of Python,
  it might not be necessary.
tags: python, fandom
title: Experiments with AO3 and Python
---

Recently, I've been writing some scripts that need to get data from [AO3][ao3][^1].
Unfortunately, AO3 doesn't have an API (although it's apparently [on the roadmap][roadmap]), so you have to do everything by scraping pages and parsing HTML.
A bit yucky, but it can be made to work.

You can get to a lot of pages without having an AO3 account &ndash; which includes most of the fic.
If you want to get data from those pages, you can use any HTTP client to download the HTML, then parse or munge it as much as you like.
For example, in Python:

```python
import requests

req = requests.get('http://archiveofourown.org/works/9079264')
print(req.text)  # Prints the page's HTML
```

I have a script that takes this HTML, and which can extract metadata like word count and pairings.
(I use that to auto-tag my bookmarks on Pinboard, because I'm lazy that way.)

But there are some pages that require you to be logged in to an account.
For example, AO3 can track your reading history across the site.
If you try to access a private page with the approach above, you'll just get an error message:

<blockquote class="ao3_error">Sorry, you don't have permission to access the page you were trying to reach. Please log in.</blockquote>

Wouldn't it be nice if you could access those pages in a script as well?

I've struggled with this for a while, and I had some hacky workarounds, but nothing very good.
Tonight, I found quite a neat solution that seems much more reliable.

For this to work, you need an HTTP client that doesn't just do one-shot requests.
You really want to make two requests: one to log you in, another for the page you actually want.
You need to persist some login state from the first request to the second, so that AO3 remembers us on the second request.
Normally, this state is managed by your browser: in Python, we can do the same thing with [sessions][session].

After a bit of poking at [the AO3 login form][login], I've got the following code that seems to work:

```python
import requests

sess = requests.Session()

# Log in to AO3
sess.post('http://archiveofourown.org/user_sessions', params={
    'user_session[login]': USERNAME,
    'user_session[password]': PASSWORD,
})

# Fetch my private reading history
req = sess.get('https://archiveofourown.org/users/%s/readings' % USERNAME)
print(req.text)
```

Where previously this would return an error page, now I get my reading history.
There's more work to parse this into usable data, but we're past my previous stumbling block.

I think this is a useful milestone, and could form the basis for a Python-based AO3 API.
I've thought about writing such a library in the past, but it's a bit limited if you can't log in.
With that restriction lifted, there's a lot more you can potentially do.

I have a few ideas about what to do next, but I don't have much free time coming up.
I'm not promising anything &ndash; but you might want to watch this space.

[ao3]: https://archiveofourown.org
[roadmap]: http://archiveofourown.org/admin_posts/295
[requests]: http://python-requests.org/
[session]: http://docs.python-requests.org/en/master/user/advanced/#session-objects
[login]: http://archiveofourown.org/login

[^1]: Non-fannish types: AO3 is the *Archive of Our Own*, a popular website for sharing fanfiction.
