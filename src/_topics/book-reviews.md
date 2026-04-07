---
layout: topic
title: Books I've read
---
I love reading!
I always have a book on the go, and I can often be found between the shelves of my local library.
I worked as a software developer at [Wellcome Collection](https://wellcomecollection.org) for seven years, where I got to see what makes a library tick.

I'm also a regular attendee of the [London Ace Book Club](/ace-book-club/), and have been since it started running in September 2022.
It's where I met my partner; we bonded over our love of books.

This page is where I keep notes on all the books I've read:

{%- from "macros/article_cards.html" import article_cards -%}

<style>
  @use "components/list_of_posts";
</style>

<style>
  #list_of_posts section:nth-child(2n + 1) {
    background: var(--section-bg-color);
  }
</style>

<div id="list_of_posts">
  {% set end_of_year_faves = site.articles
    | selectattr("is_featured")
    | filter_for_topic("Books I've read") %}
  
  {{- article_cards(articles=end_of_year_faves) -}}

  {% set per_year_reviews =
      site.book_reviews
        | sort(attribute="review.date_read", reverse=True)
        | groupby("review.date_read.year")
        | sort(reverse=True) %}

  {%- for year, reviews in per_year_reviews -%}
    <section class="plinks">
      <div>
        {%- if loop.index == 1 -%}
        <ul class="dot_list">
          {%- for year, _ in per_year_reviews -%}
          <li><a href="#books-{{ year }}">{{ year }}</a></li>
          {%- endfor -%}
        </ul>
        {%- endif -%}
        <h2 id="books-{{ year }}">Books I read in {{ year }}</h2>
        <p>
          {%- if site.time.year == year -%}
          I’ve read {{ reviews|count }} book{% if reviews|count > 1 %}s{% endif %} so far this year:
          {%- else -%}
          I read {{ reviews|count }} book{% if reviews|count > 1 %}s{% endif %}:
          {%- endif %}
        </p>
        {%- include "partials/book_review_list.html" -%}
      </div>
    </section>
  {%- endfor -%}
</div>

