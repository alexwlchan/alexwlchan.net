---
layout: topic
title: Books I've read
---
I love reading!
I always have a book on the go, and I can often be found between the shelves of my local library.
I worked as a software developer at [Wellcome Collection](https://wellcomecollection.org) for seven years, where I got to see what makes a library tick.

I'm also a regular attendee of the [London Ace Book Club](https://aceandarolondon.org.uk/bookclub/), and have been since it started running in October 2022.
It's where I met my partner; we bonded over our love of books.

This page is where I keep notes on all the books I've read:



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
