---
layout: til
date: 2024-01-12 21:35:45 +00:00
title: Use the `{% capture %}` tag to assign complex strings to variables
summary: |
  If you want to get a string that's semi-complicated to construct, you can put a "mini-template" in the `{% capture %}` tag to build it over multiple lines.
tags:
  - liquid
---
You can use the [capture tag] to create a new variable:

```liquid
{% raw %}{% capture variable %}
  value
{% endcapture %}{% endraw %}
```

This could be quite useful for building up complex variables with several conditionals or loops, inside the template.

I first saw this variable being used in [an article by Jesse Squires][squires], and although I don't have a use for it right now, it's a useful one to remember.

[capture tag]: https://shopify.dev/docs/api/liquid/tags/capture
[squires]: https://www.jessesquires.com/blog/2021/06/06/rss-feeds-jekyll-and-absolute-versus-relative-urls/
