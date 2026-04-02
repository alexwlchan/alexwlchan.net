---
layout: page
title: Articles
colors:
  css_light: "#115bda"
  css_dark:  "#40c3ff"
---

Articles are longer, more substantial pieces of writing.
Unlike my shorter [notes](/notes/), these contain original thoughts and ideas meant to be read from start to finish.

{% from "macros/list_of_posts.html" import list_of_posts %}

{{ list_of_posts(site.articles) }}
