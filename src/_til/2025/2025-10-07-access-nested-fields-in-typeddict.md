---
layout: til
title: Look at the `__annotations__` to learn about the definition of a TypedDict
date: 2025-10-07 21:52:13 +0100
tags:
  - python
  - python:typing
---
Here's a TypedDict from my code:

{% code lang="python" names="0:MicroblogPost 2:site 5:body" %}
class MicroblogPost(PostBase):
    """
    A post from a microblogging service.
    """

    site: typing.Literal["bluesky", "mastodon", "threads", "twitter", "x"]
    body: list[MicroblogData]
{% endcode %}

I wanted to get the list of `Literal` values in the `site` attribute.
I know I can use `typing.get_args()` to [get a list of `typing.Literal[…]`][getargs] values, but how do I get the `Literal[…]` value here?

[getargs]: https://alexwlchan.net/til/2025/typing-getargs/

## Option 1: Extract the `Literal` as a separate type

{% code lang="python" names="0:MicroblogSites 3:MicroblogPost 5:site 7:body" %}
MicroblogSites = typing.Literal["bluesky", "mastodon", "threads", "twitter", "x"]


class MicroblogPost(PostBase):
    """
    A post from a microblogging service.
    """

    site: MicroblogSites
    body: list[MicroblogData]
{% endcode %}

and then I can use `typing.get_args()` on `MicroblogSites`.
This is the approach I ended up using, but I wondered if there's another way (say, if I don't control the type).

## Option 2: Look at the `__annotations__` variable on the TypedDict

This allows me to extract the `Literal` value, and then I could inspect it as I wish:

{% code lang="pycon" %}
>>> MicroblogPost.__annotations__
{'body': list[models.post.MicroblogData],
 'id': <class 'str'>,
 'meta': <class 'models.post.Meta'>,
 'site': typing.Literal['bluesky', 'mastodon', 'threads', 'twitter', 'x']}
>>> MicroblogPost.__annotations__['site']
typing.Literal['bluesky', 'mastodon', 'threads', 'twitter', 'x']
{% endcode %}

This definitely works, but I'm not sure i should be using `__annotations__` directly.
In particular, the [Python docs for `type.__annotations__`][datadocs] say:

> For best practices on working with [`__annotations__`](https://docs.python.org/3/reference/datamodel.html#object.__annotations__), please see [`annotationlib`](https://docs.python.org/3/library/annotationlib.html#module-annotationlib). Use [`annotationlib.get_annotations()`](https://docs.python.org/3/library/annotationlib.html#annotationlib.get_annotations) instead of accessing this attribute directly.

I'm not going to pursue that path today, but noting if I need this in future.

[datadocs]: https://docs.python.org/3/reference/datamodel.html#type.__annotations__
