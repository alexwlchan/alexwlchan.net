---
layout: topic
title: London Ace Book Club
date_updated: 2026-03-23 23:09:54 +00:00
---

The [London Ace Book Club][bookclub] is a monthly book club that reads and discusses books with [asexual][wiki-asexual] and [aromantic][wiki-aromantic] themes.
I've been going since the book club started in September 2022, and I manage to attend more months than not.
It's also where I met my partner; we bonded over our love of books.

Here's a list of books I've read for Ace Book Club:

{% set reviews =
    site.book_reviews
      | filter_for_topic("London Ace Book Club")
      | sort(attribute="review.date_read") %}

{#
  Rearrange the books into book list order:

    reviews[0]  = Loveless, by Alice Oseman
    reviews[7]  = Ace, by Angela Chen
    reviews[13] = How to Be a Normal Person, by TJ Clune
#}
{% set reviews = ([reviews[0]] + [reviews[7]] + reviews[1:7] + reviews[8:13] + [reviews[13]] + reviews[14:]) | reverse | list %}

<div id="topic_entries">
  <section>
    <div>
      {%- include "partials/book_review_list.html" -%}
    </div>
  </section>
</div>

[bookclub]: https://aceandarolondon.org.uk/bookclub
[wiki-asexual]: https://en.wikipedia.org/wiki/Asexuality
[wiki-aromantic]: https://en.wikipedia.org/wiki/Aromanticism