---
layout: til
title: How to find the Pygments token type for a short name
summary: Look at the source code of `pygments.token`.
date: 2025-10-22 19:37:54 +01:00
topic: Python
---
When I use Pygments or Rouge to apply syntax highlighting to some code, for example this Python snippet:

```
print("hello world")
```

they produce some HTML where each token type is identified by a short name, like `nf` or `p` or `sh`:

{% code lang="html" wrap="true" %}
<span class="nf">print</span><span class="p">(</span><span class="sh">"</span><span class="s">hello world</span><span class="sh">"</span><span class="p">)</span>
{% endcode %}

If I find a short name I don't recognise, I can look it up in the [`pygments.token` source code](https://pygments-doc.readthedocs.io/en/latest/_modules/pygments/token.html), which includes the mapping from tokens to short names:

{% code lang="python" %}
# Map standard token types to short names, used in CSS class naming.
# If you add a new item, please be sure to run this file to perform
# a consistency check for duplicate values.

STANDARD_TYPES = {
    Token:                         '',

    Text:                          '',
    Whitespace:                    'w',
    Error:                         'err',
    Other:                         'x',
    …
{% endcode %}
