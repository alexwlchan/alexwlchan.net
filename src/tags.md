---
layout: page
title: Tags
---

{% assign sorted_tags = site.tags|sort %}

<ul>
  {% for tag in sorted_tags %}
    {% assign tag_name = tag[0] %}
    {% assign posts = tag[1] %}
    <li><a href="#tag__{{ tag_name }}">{{ tag_name }}</a> ({{ posts.size }})</li>
  {% endfor %}
</ul>

{% for tag in sorted_tags %}
{% assign tag_name = tag[0] %}
{% assign posts = tag[1] %}
<h3 id="tag__{{ tag_name }}">{{ tag_name }}</h3>
<ul>
  {% for p in posts %}
  <li><a href="{{ p.url }}">{{ p.title }}</a></li>
  {% endfor %}
</ul>
{% endfor %}
