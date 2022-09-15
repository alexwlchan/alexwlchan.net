---
layout: page
title: All posts
summary: A list of every post on alexwlchan.net, sorted by date.
---

This is a list of all my posts, sorted by date.
If you're new to the blog, you might want to start with the shorter list of [my favourite posts](/best-of/).

You can subscribe to my posts [as an RSS feed](/atom.xml).

<script src="/scripts/tag-filters.js"></script>

<div id="tag_filter">
  {% assign tag_selection = site.data["tag_tally"] | sort %}

  <p>Filter by tag:
    <select id="tag_selection" onchange="applyTagFilters()">
      <option value="_nofilter_">(no filter)</option>
      {% for tag in tag_selection %}
        {% if tag[1] > 1 %}
          <option value="{{ tag[0] }}">{{ tag[0] }} ({{ tag[1] }})</option>
        {% endif %}
      {% endfor %}
    </select>
  </p>
</div>

<style>
  select {
    font-size: 130%;
  }

  /* Ensure the label and list of years appear on the same line */
  #jumpto_label, #jumpto_list {
    display: inline-block;
    margin: 0;
  }

  #jumpto_list {
    list-style-type: none;
    padding-left: 0px !important;
  }

  /* Ensure they all display in a line */
  #jumpto_list li {
    display: inline;
  }

  /* This inserts the slashes between years.  See the comment in tag-filters.js
     for more on how/why this works. */
  #jumpto_list li:not(:first-child)::before {
    content: " / ";
  }

  #jumpto_list li.first_visible_jumpto::before {
    content: "";
  }
</style>

<p id="jumpto_label">
  Jump to:&nbsp;<ul id="jumpto_list">
  {% for year_entry in site.data["posts_by_year"] -%}
    <li data-jumpto-year="{{ year_entry[0] }}">
      <a href="#year-{{ year_entry[0] }}">{{ year_entry[0] }}</a>
    </li>
  {%- endfor %}
  </ul>
</p>

{% for year_entry in site.data["posts_by_year"] %}
{% assign year = year_entry[0] %}
{% assign posts = year_entry[1] %}

<div class="year_group" data-group-year="{{ year }}" id="posts-{{ year }}">
  <h2 id="year-{{ year }}">{{ year }}</h2>

  <ul class="post_cards">
  {% for post in posts %}
    {% unless post.index.exclude %}
      {% include post_card.html %}
    {% endunless %}
  {% endfor %}
  </ul>
</div>
{% endfor %}
