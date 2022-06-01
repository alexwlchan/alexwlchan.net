---
layout: page
title: Posts
---

46 posts

<style>
  .card {
    border: 2px solid red;
    border-radius: 5px;
/*          width: 400px;*/
/*          height: 320px;*/
    overflow: hidden;
  }

  .card a {
    color: black;
    text-decoration: none;
    display: block;
    height: 100%;
  }

  .card:hover {
    background: yellow;
  }

  .card:hover img {
    opacity: 0.85;
    background: green;
  }

  .card:hover .card_image {
    background: green;
  }

  .card_image {
    margin-top: 0;
    margin-bottom: 0;
  }

  .card_metadata {
    margin: 0;
    padding: 1em;
  }

  .card_title {
    margin-top: 0;
/*    margin-bottom: 0.5em;*/
  }

  .card_description {
/*    margin-top: 0.5em;*/
    font-size: 85%;
    line-height: 1.45em;
    margin-bottom: 0;
  }

  ul.post_cards {
    list-style-type: none;
    padding-left: 0px !important;
    display: grid;
    grid-template-columns: auto auto;
/*            grid-template-rows:    calc(50% - 5px) calc(50% - 5px);*/
    grid-gap: 1em;
  }

</style>

<ul class="post_cards">
{% for post in site.posts %}
  {% if post.index.best_of %}
    <li class="card">
      <a href="{{ post.url }}">
        <p class="card_image"><img src="{{ post.theme.image }}" alt=""/></p>
        <p class="card_metadata">
          <span class="card_title">{{ post.title }}</span><br/>
          <span class="card_description">
            {{ post.summary }}
            {{ post.date | date: "%B %Y" }}.
          </span>
        </p>
      </a>
    </li>
  {% endif %}
{% endfor %}
</ul>
