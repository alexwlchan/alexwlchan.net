---
layout: topic
title: Entertainment
date_updated: 2026-01-30 18:25:48 +00:00
---
Stuff I find fun or enjoyable.
Books, theatre, TV shows, movies.

## Sub-topics

<ul>
{% for topic in site.topics[page.title].children %}
  <li><a href="{{ topic.url }}">{{ topic.label | markdownify_oneline }}</a></li>
{% endfor %}
</ul>
