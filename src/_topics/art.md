---
layout: topic
title: Art and creativity
---

These entries show off my more creative side: my illustrations, my cross-stitch, my fiction.

Sub-topics:

<ul>
  {%- for c in page.topic.children | sort(attribute="name") -%}
  <li>
    <a href="{{ c.href }}">{{ c.name }}</a>
  </li>
  {%- endfor -%}
</ul>

