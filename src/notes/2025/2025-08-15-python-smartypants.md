---
layout: note
title: My preferred options for SmartyPants in Python
summary: "`smartypants.smartypants(…, Attr.q | Attr.D | Attr.e | Attr.u)`"
date: 2025-08-15 09:43:00 +01:00
date_updated: 2026-03-01 23:03:17 +00:00
topic: Python
---
I use the [smartypants library][smartypants], which adds curly quotes and dashes to some text in Python.
This is my current configuration:

```python {"names":{"1":"smartypants","2":"smartify","3":"text","6":"text","9":"attrs"}}
import smartypants


def smartify(text: str) -> str:
    """
    Add curly quotes and smart dashes to a string.
    """
    # Undo some escaping from Mistune.
    text = text.replace("&quot;", '"')

    attrs = (
        # normal quotes (" and ') to curly ones
        smartypants.Attr.q
        |
        # typewriter dashes (--) to en-dashes and dashes (---) to em-dashes
        smartypants.Attr.D
        |
        # dashes (...) to ellipses
        smartypants.Attr.e
        |
        # output Unicode chars instead of numeric character references
        smartypants.Attr.u
    )

    return smartypants.smartypants(text, attrs)
```

I set four [processing attributes][smartypants-attrs] to control the behaviour.

[Mistune][mistune] is the Python Markdown parser I use, which converts double quotes to `&quot;`.
I don't think there's a way to disable that behaviour.

Here's a set of tests that check it's doing what I expect:

```python {"names":{"1":"pytest","5":"test_smartify","6":"text","8":"expected","10":"actual"}}
import pytest


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Isn't it delightful -- she said", "Isn’t it delightful – she said"),
        ("Are you ... sure?", "Are you … sure?"),
        ("<h2>Isn't it delightful?</h2>", "<h2>Isn’t it delightful?</h2>"),
        ("<li>Isn't it delightful?</li>", "<li>Isn’t it delightful?</li>"),
        ("<p>&quot;It's nice&quot;, he said</p>", "<p>“It’s nice”, he said</p>"),
    ],
)
def test_smartify(text: str, expected: str) -> None:
    """
    Test smartify().
    """
    actual = t.smartify(text)
    assert actual == expected
```

[mistune]: https://mistune.lepture.com/en/latest/
[smartypants]: https://smartypants.readthedocs.io/en/latest/introduction.html
[smartypants-attrs]: https://smartypants.readthedocs.io/en/latest/usage.html#attributes
