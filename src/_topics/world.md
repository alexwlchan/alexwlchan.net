---
layout: topic
title: The world around us
---

This is a bit of a catch-all topic for anything that occurs outside a computer -- geography, history, politics, whatever catches my eye.

Sub-topics:

<ul>
  {%- for c in get_topic_by_name(page.title).children | sort(attribute="name") -%}
  <li>
    <a href="{{ c.href }}">{{ c.name }}</a>
  </li>
  {%- endfor -%}
</ul>
