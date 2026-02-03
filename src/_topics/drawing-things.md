---
layout: topic
title: Drawing things
---

I like using computers to draw art; this topic has the pictures I've made.

Sub-topics:

<ul>
  {%- for c in get_topic_by_name(page.title).children | sort(attribute="name") -%}
  <li>
    <a href="{{ c.href }}">{{ c.name }}</a>
  </li>
  {%- endfor -%}
</ul>
