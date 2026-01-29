---
layout: page
title: Books I've read
breadcrumb:
  - label: Entertainment
---
{% set reviews = site.pages | selectattr("layout", "eq", "book_review") | sort(attribute="review.date_read", reverse=True) %}

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
