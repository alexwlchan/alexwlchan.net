---
layout: page
title: Today I Learned (TIL)
nav_section: til
---
There's nothing here yet, but soon it'll have a list of things I've learned.

<ul>
{% for til in site.til %}
  <li>
    <a href="{{ til.url }}">{{ til.title }}</a>
  </li>
{% endfor %}
</ul>