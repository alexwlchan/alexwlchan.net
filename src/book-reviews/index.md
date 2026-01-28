---
layout: page
title: Books I've read
breadcrumb:
  - label: Entertainment
---
{% set reviews = site.pages | selectattr("layout", "eq", "book_review") | sort(attribute="review.date_read", reverse=True) %}

<ul>
{% for rev in reviews %}
  <li><a href="{{ rev.url }}">{{ rev.title }}</a></li>
{% endfor %}
</ul>
