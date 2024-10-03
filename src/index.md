---
layout: page
title: ""
colors:
  css_light: "#17823e"
  css_dark:  "#26d967"
---

<style type="x-text/scss">
  @import "utils/functions.scss";

  @function create_leaf_svg($fill) {
    $fill: str-replace("#{$fill}", '#', '%23');
    $output: '<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" viewBox="0 0 98 98" width="50px">' +
             "<path fill=\"#{$fill}\" " +
             'd="M30.636,61.596c-1.006,1.497-1.859,2.997-2.56,4.5c-3.046,6.531-3.178,13.179-0.396,19.941  c0.536,1.304-0.087,2.797-1.391,3.333c-1.305,0.536-2.797-0.087-3.333-1.391c-3.354-8.155-3.195-16.171,0.476-24.045  c3.45-7.397,10.028-14.608,19.732-21.633c2.324-1.893,4.818-3.785,7.483-5.678c1.069-0.759,1.321-2.241,0.562-3.31  c-0.759-1.069-2.241-1.321-3.31-0.561C37.653,40.026,29.77,47.454,24.243,55.01c-2.331-13.176-0.587-23.597,5.221-31.032  c8.019-10.267,24.155-15.49,47.983-15.54c-0.048,23.828-5.272,39.965-15.538,47.984C54.43,62.264,43.927,63.992,30.636,61.596z"/>' +
             '</svg>';
    @return str-replace($output, '"', '%22');
  }

  hr {
    height: 50px;
    width: 50px;

    $light-svg-url: create_leaf_svg(rgba(#17823e, 0.2));
    $dark-svg-url:  create_leaf_svg(rgba(#26d967, 0.6));

    --hr-background-image: url("data:image/svg+xml;charset=UTF-8,#{$light-svg-url}");

    @media (prefers-color-scheme: dark) {
      --hr-background-image: url("data:image/svg+xml;charset=UTF-8,#{$dark-svg-url}");
    }
  }

  img#headshot {
    border-radius: 50%;
    margin-left:   var(--default-padding);
    margin-bottom: var(--default-padding);
  }

  @media screen and (min-width: 500px) {
    main {
      padding-top: calc(1.5 * var(--default-padding));
    }

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

**Hi, I’m Alex. I'm a software developer, writer, and hand crafter from the UK.**

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
If you want to know what's on my mind, check out [the articles I've written](/articles/), [the talks I've given](/tags/talks/), and [the lessons I've learned](/til/).

In my free time, I enjoy doing art and simple **hand crafts** to relax.
I've had a lot of fun doing [cross stitch](/tags/cross-stitch/), origami and paper craft, and doodling sketches of implausible sci-fi vehicles.

I'm **queer** and **trans**.
My pronouns are "they" or "she".

This website is a place to share stuff I find interesting or fun.
I hope you like it!



---



## Favourite articles

Here are some of my favourite things [that I've written](/articles/):

{% comment %}
  This component shows 6 featured articles.

  To keep things somewhat interesting, I have more than 6 such articles
  and I display a random selection.

  - The Jekyll build will pick a sample of 6 every time it's built
  - JavaScript on the page will shuffle the list on page reloads

{% endcomment %}

{% assign featured_articles = site.posts | where: "index.feature", true %}
{% assign sample_of_articles = featured_articles | sample: 6 %}

{% include article_card_styles.html selected_articles=featured_articles %}

<script>
  const featuredArticles = [
    {% for article in featured_articles %}
      {% capture articleHtml %}
        {% include article_card.html %}
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
  {% include article_card.html %}
{% endfor %}
</ul>

Here are some of the topics I write about:

<ul class="dot_list">
  {% for tag_name in site.data['popular_tags'] %}
    <li>{% include tag_link.html %}</li>
  {% endfor %}
</ul>



---



## Get in touch

The best way to get in touch with me is by email: **<{{ site.email }}>**, or you can [follow me on social media](/contact/).

If you like something I've made, perhaps [say thanks](/say-thanks/)?
I love hearing from readers! ☺️
