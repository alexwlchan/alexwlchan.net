---
layout: topic
title: Books I've read
topics: 
  - Entertainment
date_updated: 2026-01-30 18:28:55 +00:00
---
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

I love reading!
I always have a book on the go, and I can often be found between the shelves of my local library.
I worked as a software developer at [Wellcome Collection](https://wellcomecollection.org) for seven years, where I got to see what makes a library tick.

I'm also a regular attendee of the [London Ace Book Club](https://aceandarolondon.org.uk/bookclub/), and have been since it started running in October 2022.
It's where I met my partner; we bonded over our love of books.

This page is where I keep notes on all the books I've read:

{% set this_topic = site.topics[page.title] %}
{% set pages = this_topic.pages_in_topic %}

{% from "partials/topic_entries.html" import topic_section %}
{% set featured = pages | selectattr("template_name", "eq", "post.html") | selectattr("is_featured") | sort(attribute="date", reverse=True) %}

<div id="topic_entries">
  {{ topic_section(featured, "article_cards") }}
  <section>
  {% set reviews = site.book_reviews | sort(attribute="review.date_read", reverse=True) %}

  <ul>
  {% for rev in reviews %}
    <li><a href="{{ rev.url }}"><em>{{ rev.book.title }}</em></a>, {{ rev.attribution_line }}</li>
  {% endfor %}
  </ul>
  </section>
</div>

