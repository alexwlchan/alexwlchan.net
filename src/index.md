---
layout: page
title: ""
colors:
  css_light: "#17823e"
  css_dark:  "#26d967"
---

<style>
  main {
    padding-top: calc(1.5 * var(--default-padding));
  }

  svg[role="separator"] {
    display: block;
  }

  img#headshot {
    border-radius: 50%;
    margin-left:   var(--default-padding);
    margin-bottom: var(--default-padding);
  }

  @media screen and (min-width: 500px) {
    img#headshot {
      float: right;
    }
  }

  @media screen and (max-width: 500px) {
    img#headshot {
      display: block;
      margin-top: var(--default-padding);
      margin-left:  auto;
      margin-right: auto;
    }
  }
</style>

**My name is _Alex Chan_, but I usually go by _Alex_ or _Lexie_. I'm a software developer, writer, and hand crafter from the UK.**

{%
  picture
  filename="profile_green_square.jpg"
  id="headshot"
  parent="/images"
  width="230"
  alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants."
  class="rounded_corners"
%}

I build systems for **digital preservation** -- making sure that digital archives remain safe and accessible into the far future.
Currently I think about photos at <a href="https://www.flickr.org">the Flickr Foundation</a>, and before that I helped build services to store and search the museum and library collections at <a href="https://wellcomecollection.org/">Wellcome Collection</a>.

I enjoy **writing**, and I've been posting at this domain since 2012.
I write about a variety of non-fiction topics, with a particular focus on software development.
If you want to know what's on my mind, check out [the articles I've written](/articles/), [the talks I've given](/articles/?tag=talks), and [the lessons I've learned](/til/).

In my free time, I enjoy doing art and simple **hand crafts** to relax.
I've had a lot of fun doing [cross stitch](/articles/?tag=cross-stitch), origami and paper craft, and doodling sketches of implausible sci-fi vehicles.

I'm **queer** and **trans**.
My pronouns are "they" or "she".

This website is a place to share stuff I find interesting or fun.
I hope you like it!



  {% separator "leaf.svg" %}



## Favourite articles

My [articles](/articles/) cover a variety of non-fiction topics.
Here are a few of my favourites:

{% assign featured_articles = site.posts | where: "index.feature", true %}
{% assign sample_of_articles = featured_articles | sample: 6 %}

{% include article_card_styles.html selected_articles=featured_articles %}

<script>
  const featuredArticles = [
    {% for article in featured_articles %}
      {% capture articleHtml %}
        {% include article_card.html hide_date="true" %}
      {% endcapture %}
      {{ articleHtml | strip | jsonify }},
    {% endfor %}
  ];

  window.addEventListener("DOMContentLoaded", function() {
    document.querySelector("#featured_articles").innerHTML =
      featuredArticles
        .sort(() => 0.5 - Math.random())
        .slice(0, 6)
        .join("");
  });
</script>

<ul class="article_cards" id="featured_articles">
{% for article in sample_of_articles %}
  {% include article_card.html hide_date="true" %}
{% endfor %}
</ul>


  {% separator "leaf.svg" %}


## My newest articles

I typically write three or four new articles a month.
If you want to find out when I post something new, you can [subscribe to my RSS feed](/atom.xml) or [follow me on social media](/contact/).

Here's what I've written recently:

{% comment %}
  The styles in "article_cards.scss" will switch between three layouts:

  *   a 1×3 column (mobile devices)
  *   a 2×2 grid (regular screens)
  *   a 3×1 row (wide screens)

  This is meant to be a sample of posts, not a full list.  I don't want
  too many on mobile devices, and I don't want a single item on its own
  on the second row on a wide screen.

  This CSS will hide the fourth post on mobile/wide screens.
{% endcomment %}

<style>
  @media screen and (max-width: 500px) {
    #recent_articles li:nth-child(4) {
      display: none;
    }
  }

  @media screen and (min-width: 1000px) {
    #recent_articles li:nth-child(4) {
      display: none;
    }
  }
</style>

{% assign recent_articles = site.posts | sort: "date" | reverse | slice: 0, 4 %}

{% comment %}
  For consistency with the "all posts" page, any blog posts that don't
  set an explicit colour get tinted the default red on the homepage.
{% endcomment %}

{% assign is_index = true %}

{% include article_card_styles.html selected_articles=recent_articles %}

<ul id="recent_articles" class="article_cards">
{% for article in recent_articles %}
  {% include article_card.html %}
{% endfor %}
</ul>

[Read more articles &rarr;](/articles/)






  {% separator "leaf.svg" %}



## Get in touch

The best way to get in touch with me is by email: **<{{ site.email }}>**.

If you like something I've made, perhaps [say thanks](/say-thanks/)?
I love hearing from readers! ☺️
