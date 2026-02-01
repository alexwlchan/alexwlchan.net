---
layout: topic
title: Books I've read
topics: 
  - Entertainment
date_updated: 2026-01-30 18:28:55 +00:00
---
{% set reviews = site.book_reviews | sort(attribute="review.date_read", reverse=True) %}

<style>
  @use "components/under_construction";
</style>

<blockquote class="under_construction">
  <p>
    <strong>This page is under construction!</strong>
  </p>
  <p>
    I used to write book reviews on <a href="https://books.alexwlchan.net/">books.alexwlchan.net</a>, but I’m gradually moving them here as I consolidate everything on this domain.
    More books will appear here soon!
  </p>
</blockquote>

<ul>
{% for rev in reviews %}
  <li><a href="{{ rev.url }}"><em>{{ rev.book.title }}</em></a>, {{ rev.attribution_line }}</li>
{% endfor %}
</ul>
