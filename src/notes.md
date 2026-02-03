---
layout: topic
title: Notes
colors:
  css_light: "#115bda"
  css_dark:  "#40c3ff"
---

Notes are snippets of information that I find useful and wanted to write down, but aren't long or original enough to be articles.
I expect most people will find these notes by browsing my list of topics or from a search engine.

{% with articles = site.notes %}
{% include "partials/article_links.html" %}
{% endwith %}
