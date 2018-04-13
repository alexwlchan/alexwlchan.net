---
layout: page
title: Tags
---

{% assign sorted_tags = site.tags|sort %}

<p class="tags__cloud">
{% assign tag_cloud = sorted_tags|build_tag_cloud %}
{% for tag in tag_cloud %}
  {% assign tag_name = tag[0] %}
  {% assign data = tag[1] %}
  <a href="#tag__{{ tag_name }}"
     style="font-size: {{ data["size"] }}pt; color: #{{ data["red"] }}{{ data["green"] }}{{ data["blue"] }};">{{ tag_name }}</a>
{% endfor %}
</p>

<div class="post__separator" aria-hidden="true">&#9671;</div>

{% for tag in sorted_tags %}
{% assign tag_name = tag[0] %}
{% assign posts = tag[1] %}

{% assign aliases = site.data["tag_aliases"][tag_name] %}
{% for a in aliases %}
<a id="tag__{{ a }}"></a>
{% endfor %}

<h3 id="tag__{{ tag_name }}">{{ tag_name }}</h3>
<ul>
  {% for p in posts %}
  <li><a href="{{ p.url }}">{{ p.title }}</a></li>
  {% endfor %}
</ul>
{% endfor %}
