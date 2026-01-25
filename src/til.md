---
layout: page
title: Today I Learned (TIL)
nav_section: til
---
TIL stands for **today I learned**.
This is a collection of small, interesting things I've learnt, which I thought were worth remembering and sharing with other people.

If you want to follow along, these posts have [their own RSS feed](/til/atom.xml).

---

{% set tils = site.pages | selectattr("layout", "eq", "til") | sort(attribute="date", reverse=True) %}

{% with articles = tils %}
  {% include "partials/article_links.html" %}
{% endwith %}
