---
layout: page
title: Articles
nav_section: articles
---
There's nothing here yet, but soon it'll have a list of things I've written.

<ul id="list_of_articles">
{% for article in site.articles reversed %}

  <li class="article_card">
    {% include article_card.html %}
  </li>
{% endfor %}
</ul>
