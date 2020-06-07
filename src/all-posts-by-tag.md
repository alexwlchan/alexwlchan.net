---
layout: page
title: All posts by tag
archive_variant: global
---

<p>
  <em>
    Browse the archive:
      <a href="/all-posts/">by date</a> /
      by tag /
      <a href="/all-posts-by-post-type/">by post type</a>
  </em>
</p>

<h3>Tags</h3>

<ul class="dot_list" id="tag_list">
  {% assign posts_by_tag = site.data["posts_by_tag"] | sort %}
  {% for tag_entry in posts_by_tag %}
    <li>
      <a href="#{{ tag_entry[0] }}">{{ tag_entry[0] | replace: "-", "&#8209;" }}</a>
    </li>
  {% endfor %}
</ul>

<div class="post__separator" aria-hidden="true">&#9670;</div>

{% for tag_entry in posts_by_tag %}
  <h3 id="{{ tag_entry[0] }}">{{ tag_entry[0] }}</h3>

  {% assign posts = tag_entry[1] %}
  {% include archive_list.html %}
{% endfor %}

<br/>
