---
layout: post
date: 2024-06-06 16:14:24 +0000
title: The surprising utility of a Flickr URL parser
summary: I made a library that knows how to read lots of different forms of Flickr.com URL, and I used `hyperlink` to do it.
link: https://www.flickr.org/the-surprising-utility-of-a-flickr-url-parser/
tags:
  - flickr
  - flickr foundation
  - python
colors:
  index_light: "#785a28"
  index_dark:  "#cdae58"
---
{% comment %}
  Card image from https://www.flickr.com/photos/usnationalarchives/4727552068/
{% endcomment %}

As part of my work at the Flickr Foundation, I wrote a little Python library that can be used to parse Flickr URLs.
For example:

```console
$ flickr_url_parser 'https://www.flickr.com/photos/usnationalarchives/4727552068/'
{"type": "single_photo", "photo_id": "4727552068"}
```

This started as a simple project, and grew as I discovered more and more variants of Flickr URL.
I've written about the library and how we're using it in [a new article](https://www.flickr.org/the-surprising-utility-of-a-flickr-url-parser/) on the Flickr Foundation blog.

At the heart of the project is a Python library called [hyperlink](https://hyperlink.readthedocs.io/en/latest/).
This is a URL parsing library that I first came across several years ago, when I made a few contributions to the python-hyper library.
It has quite a nice API for breaking apart URLs:

{% code lang="pycon" names="0:hyperlink 1:url" %}
>>> import hyperlink
>>> url = hyperlink.parse("https://www.flickr.com/photo_exif.gne?id=4727552068")
>>> url.host
'www.flickr.com'
>>> url.path
('photo_exif.gne',)
>>> url.fragment
''
{% endcode %}

There is a [`urlparse` module](https://docs.python.org/3/library/urllib.parse.html) in the standard library, but I prefer Hyperlink because of how it handles query strings.
It does the work of parsing query strings and reversing any URL decoding in a single step, whereas it's several steps with the standard library.

Compare:

{% code lang="pycon" names="0:url" %}
>>> url = hyperlink.parse('https://example.com/?greeting=hello%20world&place=caf%c3%a9')
>>> url.query
(('greeting', 'hello world'), ('place', 'café'))
>>> url.get('place')
['café']
{% endcode %}

with:

{% code lang="pycon" names="0:url" %}
>>> url = urllib.parse.urlparse('https://example.com/?greeting=hello%20world&place=caf%c3%a9')
>>> url.query
'greeting=hello%20world&place=caf%c3%a9'
>>> urllib.parse.parse_qs(url.query)
{'greeting': ['hello world'], 'place': ['café']}
>>> urllib.parse.parse_qs(url.query)['place']
['café']
{% endcode %}

I find the former easier to write and to read.
It also has a nice API for [manipulating query parameters](https://hyperlink.readthedocs.io/en/latest/api.html#query-parameters), which I use in a lot of projects.

If you want to learn more about the flickr-url-parser library, check out [the GitHub repo](https://github.com/flickr-foundation/flickr-url-parser) or [my article on flickr.org](https://www.flickr.org/the-surprising-utility-of-a-flickr-url-parser/).
