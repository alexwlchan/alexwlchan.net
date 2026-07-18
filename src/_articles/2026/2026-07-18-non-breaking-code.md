---
layout: article
date: 2026-07-18 09:00:04 +01:00
title: Preventing line breaks in `<code>` elements
topic: Blogging about blogging
---
One of my favourite tiny details in this website is [my non-breaking spaces][me-nbsp].
I have code that looks for phrases like "5 cm", "New York", or "Objective-C", and inserts a non-breaking space/hyphen so they'll never be split across multiple lines.

This is the sort of typographical nicety that would be handled by a professional typesetter if I was writing a printed book with a fixed layout, but that's not how websites work.
My website is viewed at lots of different sizes, and browsers choose where to insert line breaks.
I add these [non-breaking characters][wiki-nbsp] so browsers know to avoid awkward line breaks.

Previously I was only applying this detail to body text, but today I implemented something similar for `<code>` elements.
  
I used a lot of inline code snippets in [my last post][me-byte-order-marks], and while reviewing it I noticed that several of those snippets had unhelpful line breaks.
For example, `(?-u:…)` was split into `(?-` and `u:…)`, while the flag `--multiline` was split with `-` on one line and `-multiline` on the other.
These line breaks make the post harder to read, with no benefit.

I can understand why they happened -- browsers look for characters where they can break lines, and in English that includes hyphens.
It's usually fine to split hyphenated words over multiple lines, but it's annoying when that happens in code.

I could fix this by replacing the hyphen in my `<code>` with a non-breaking hyphen, but people copy/paste code snippets and that might change the meaning.

Instead, I wrote a check that looks for `<code>` elements which are short and contain a line-breaking character, then adds the `nowrap` CSS class.

```python {"names":{"1":"re","2":"add_nowrap","3":"match","8":"contents","16":"text"}}
import re

def add_nowrap(match: re.Match[str]) -> str:
    """
    Add the `nowrap` class to a `<code>` element if it contains line
    breaking characters.
    """
    contents = match.group("contents")
    if "-" in contents or " " in contents:
        return f"<code class=\"nowrap\">{contents}</code>"
    return match.group(0)

text: str

# Add the `nowrap` class to <code> snippets which are short and
# contain line-breaking characters.
#
# The limit of 15 characters is arbitrary. In longer code snippets,
# wrapping is preferable to avoid leaving excessive whitespace on
# the previous line.
text = re.sub(r"<code>(?P<contents>[^<]{1,15})</code>", add_nowrap, text)
```

This is paired with a CSS rule that uses the [`text-wrap` property][mdn-text-wrap] to tell browsers not to wrap across lines:

```css {"names":{"1":"code","2":".nowrap"}}
code.nowrap {
  text-wrap: nowrap;
}
```

This wasn't necessary, but I think it makes the site slightly nicer.

[mdn-text-wrap]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap
[me-byte-order-marks]: /2026/byte-order-marks/
[me-nbsp]: /2020/adding-non-breaking-spaces-with-jekyll/
[wiki-nbsp]: https://en.wikipedia.org/wiki/Non-breaking_space
