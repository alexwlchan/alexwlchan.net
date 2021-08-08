---
layout: page
title: All posts
archive_variant: global
post_list_date_format: day_month
---

This is a list of every post on alexwlchan.net, sorted by date.
You can browse the list:

-   by date (this page)
-   [by tag](/all-posts-by-tag/)
-   [by filtering to my favourite posts](/best-of/)

You can subscribe to my posts [as an Atom feed](/atom.xml).

Jump to:
{% for year_entry in site.data["posts_by_year"] -%}
  <a href="#year-{{ year_entry[0] }}">{{ year_entry[0] }}</a>
  {%- if forloop.last == false %} / {% endif %}
{%- endfor %}

{% for year_entry in site.data["posts_by_year"] %}
  {% assign year = year_entry[0] %}
  {% assign posts = year_entry[1] %}
  <h2 id="year-{{ year }}">{{ year }}</h2>
  {% include archive_list.html %}
{% endfor %}
