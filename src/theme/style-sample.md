---
layout: page
title: Style sample
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
