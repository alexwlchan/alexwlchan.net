---
layout: topic
title: Python
---
Python is a programming language which is especially popular for automation, making websites, and scientific computing.
It's the first programming language I ever learnt, and I'm better in Python than any other language.

## Notes about {{ page.title }}

{% with articles = site.notes | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
