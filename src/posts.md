---
layout: page
title: Posts
---

<link rel="stylesheet" href="/theme/article_cards.css">

I've been writing my blog since 2012, which is now over 300 posts and 300,000 words.
If you're new to the site, this page has some of my favourite posts from the archive -- or if you're looking for something specific, you can [see a list of everything I've posted](/all-posts/).

<ul class="post_cards">
{% assign posts_by_date = site.posts | sort: "date" | reverse %}
{% for post in posts_by_date %}
  {% if post.index.best_of %}
    {% if post.index.tint_color or post.theme.color %}
      {% if post.index.tint_color %}
        {% assign color = post.index.tint_color %}
      {% else %}
        {% assign color = post.theme.color %}
      {% endif %}
    <style>
      #{{ post.slug }}.card {
        border-color: {{ color }};
      }

      #{{ post.slug }} .card_title {
        color: {{ color }};
      }

      #{{ post.slug }}.card a:hover {
        background: {{ color | rgba: 0.2 }};
      }
    </style>
    {% endif %}

    {% if post.index.image %}
      {% assign image = post.index.image %}
    {% elsif post.theme.image %}
      {% assign image = post.theme.image %}
    {% else %}
      {% assign image = "" %}
    {% endif %}

    <li class="card" id="{{ post.slug }}">
      <a href="{{ post.url }}">

        <!--
          Intentionally omit the alt text on promos, so screen reader users
          don't have to listen to the alt text before hearing the title
          of the item in the list.

          See https://github.com/wellcomecollection/wellcomecollection.org/issues/6007
        -->
        <p class="card_image"><img src="{{ image }}" alt=""/></p>

        <p class="card_title">{{ post.title }}</p>
        <p class="card_description">
          {{ post.summary | smartify }}
          {{ post.date | date: "%B&nbsp;%Y" }}.
        </p>
      </a>
    </li>
  {% endif %}
{% endfor %}
</ul>
