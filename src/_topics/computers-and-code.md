---
layout: topic
title: Computers and code
---

I've been a professional software developer since 2014, and a hobbyist for several years before that.
This blog started as a way for me to share code snippets, and writing about my code has become a key part of how I learn and think about computers.

These entries cover the range of development work: from writing code to running it in production.

<p>
  Sub-topics:
  <ul class="dot_list">
    {%- for c in get_topic_by_name(page.title).children | sort(attribute="name") -%}
    <li>
      <a href="{{ c.href }}">{{ c.name }}</a>
    </li>
    {%- endfor -%}
  </ul>
</p>