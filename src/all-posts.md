---
layout: page
title: All posts
summary: A list of every post on alexwlchan.net, sorted by date.
---

This is a complete list of every post on alexwlchan.net, sorted by date.
If you're new to the blog, you might want to start with the shorter list of [my favourite posts](/best-of/).

You can subscribe to my posts [as an RSS feed](/atom.xml).

Jump to:
{% for year_entry in site.data["posts_by_year"] -%}
  <a href="#year-{{ year_entry[0] }}">{{ year_entry[0] }}</a>
  {%- if forloop.last == false %} / {% endif %}
{%- endfor %}

{% for year_entry in site.data["posts_by_year"] %}
  {% assign year = year_entry[0] %}
  {% assign posts = year_entry[1] %}
  <h2 id="year-{{ year }}">{{ year }}</h2>

  <ul class="post_cards">
  {% for post in posts %}
    {% if post.index == nil or post.index.exclude != true %}
      {% include post_card.html %}
    {% endif %}
  {% endfor %}
  </ul>
{% endfor %}
