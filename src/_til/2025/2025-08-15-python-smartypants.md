---
layout: til
title: My preferred options for SmartyPants in Python
summary: "`smartypants.smartypants(…, Attr.default | Attr.u)`"
date: 2025-08-15 09:43:00 +0100
tags:
  - python
---
I wanted to add curly quotes and dashes to some text in Python, so I looked at the [smartypants library](https://smartypants.readthedocs.io/en/latest/introduction.html).
This is the code I used:

```python
import smartypants

text = '"hello world"'
attrs = smartypants.Attr.default | smartypants.Attr.u

print(smartypants.smartypants(text, attrs))  # “hello world”
```

I set two [processing attributes](https://smartypants.readthedocs.io/en/latest/usage.html#attributes) that control the behaviour, which you combine with bitwise *OR*:

*   `Attr.default` is the default set of attributes, which converts curly quotes, backticks, dashes, and ellipses
*   `Attr.u` returns Unicode characters instead of numeric character references, for example `“hello world”` instead of `&#8220;hello world&#8221;`.
    You can include UTF-8 in HTML files, and the Unicode characters are easier to read in non-HTML contexts.