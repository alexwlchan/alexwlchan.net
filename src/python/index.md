---
layout: topic
title: Python
date_updated: 2026-01-30 07:54:40 +00:00
---
Python is a programming language which is especially popular for automation, making websites, and scientific computing.
It's the first programming language I ever learnt, and I'm better in Python than any other language.

## Notes

{% with articles = site.notes | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
