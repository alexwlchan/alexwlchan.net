---
layout: page
title: Style sample
last_updated: 2018-06-06 07:05:43 +0100
---

This is a page that has examples of different elements on the site.

It's useful when I'm playing with the styling, and want to see what a change looks like.

---

This is a paragraph.

> In HTML and XHTML, the blockquote element defines "a section [within a document] that is quoted from another source". &mdash; [Blockquote element, Wikipedia](https://en.wikipedia.org/wiki/Blockquote_element) (retrieved 13 May 2018)

Blockquotes quote text from other sources.
I like to keep them short, but sometimes I want to quote a longer passage of text with multiple paragraphs:

> “So what do we do if we get bitten by something deadly?' I asked.
>
> He looked at me as if I were stupid.
>
> "You die, of course. That's what deadly means."
>
> &mdash; Douglas Adams, *Last Chance to See*

And after the blockquote, I might explain why I thought it was interesting or useful.

---

Because a lot of my blog posts are about programming, I have special styles for code.
I might use an inline `<code>` tag, or I might use `<pre>` if I have a longer block of code:

```python
def git(*args):
    """Run a Git command and return its output."""
    cmd = ['git'] + list(args)
    try:
        return subprocess.check_output(cmd).decode('ascii').strip()
    except subprocess.CalledProcessError as err:
        print(err)
        sys.exit(err.returncode)
```

Usually I'll explain what's going on in the `<pre>` tag.

I might break it down over multiple paragraphs, linking to documentation or other resources as appropriate.

---

I spend a lot of time on Twitter, so I have a way to embed tweets in my posts.
This is an example of an embedded tweet:

{% tweet https://twitter.com/nex3/status/991582200616271872 %}

They're rendered with a custom Jekyll plugin -- I don't use the native Twitter embeds, because they require loading a bunch of JavaScript.
Tweets are static content, so I render them with HTML and CSS.

Hashtags, mentions and links are rendered correctly:

{% tweet https://twitter.com/beamish_girl/status/981733542118993920 %}

I can also embed tweets with a single image:

{% tweet https://twitter.com/CHilton_BB/status/994150733921611777 %}

My plugin doesn't support multiple images, quote tweets, videos, or anything else -- just text and a single image.
I've never wanted to embed a more complicated tweet, so I've never extended the plugin to do that.

That's one of the perks of writing something that's just for me, not a general purpose tool -- I can be lazy, and only build features when *I* need them.

---

Sometimes I made an addition to a post after it was originally published.
For that, I have a Jekyll plugin that renders "update" blocks, which look a bit like this:

{% update 2018-05-06 %}
This is an update to my style sample to illustrate `update` blocks.

I can write the contents of these blocks in Markdown, [include links](https://en.wikipedia.org/wiki/Patch_(computing)), and use *formatting styles*.
{% endupdate %}
