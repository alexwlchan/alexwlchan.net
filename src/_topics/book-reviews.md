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


{% from "partials/topic_entries.html" import featured_articles %}

<div id="topic_entries">
  {{ featured_articles(topic_name="Books I've read") }}

  {% set per_year_reviews =
      site.book_reviews
        | sort(attribute="review.date_read", reverse=True)
        | groupby("review.date_read.year")
        | sort(reverse=True) %}

  {%- for year, reviews in per_year_reviews -%}
    <section>
      <div>
        <h2>Books I read in {{ year }}</h2>
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

