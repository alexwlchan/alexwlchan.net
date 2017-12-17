---
layout: page
title: Tags
---

{% assign sorted_tags = site.tags|sort %}

<ul>
  {% for tag in sorted_tags %}
    {% assign tag_name = tag[0] %}
    {% assign posts = tag[1] %}
    <li><a href="/tag/{{ tag_name }}">{{ tag_name }}</a> ({{ posts.size }})</li>
  {% endfor %}
</ul>
