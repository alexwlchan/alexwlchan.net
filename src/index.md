---
layout: page
title: ""
theme:
  color: "#17823e"
---

<style>
  h2 {
    margin-top: 1em;
  }

  @media screen and (min-width: 750px) {
    img.rounded_corners {
      border-radius: 10px;
    }
  }
</style>

<img src="/images/profile_green_1x.jpg" class="fullwidth_img rounded_corners" srcset="/images/profile_green_1x.jpg 1x, /images/profile_green_2x.jpg 2x" alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants.">

## Hi, I'm Alex.

I've put a bunch of things on the Internet, including:

*   [My personal blog](/all-posts/), which covers a range of topics, from programming to photography, from colour theory to Chinese dictionaries.

*   Everything I do for [Wellcome Collection](/projects/#wellcome-collection), a museum and library where I'm part of a team working on digital preservation, the website, and the online catalogue.

*   A bunch of open-source tools and utilities, including for [managing my scanned files](https://github.com/alexwlchan/docstore), finding the [dominant colours in an image](https://github.com/alexwlchan/dominant_colours), and [web scraping for AO3](https://github.com/alexwlchan/ao3).

*   Silly art projects, like measuring [data in floppy disks](https://howlongismydata.glitch.me/), or controlling a rocket [with the &lt;marquee&gt; tag](https://marquee-rocket.glitch.me/).

*   My [Twitter feed](https://twitter.com/alexwlchan), where I share work-in-progress and think out loud about new ideas.

This site is a one-stop shop for everything I've made -- it's either here, or linked to from here.
If you're new, you might want to start with [my blog](/all-posts/) or [my list of projects](/projects/).

I'm trans, genderfluid, and my pronouns vary.
If we're strangers, "they/them" is a safe default.

I hope you enjoy the site.

{% separator "leaf.svg" %}

## Blog posts

I write about anything I find interesting or fun – there’s plenty of programming, but lots of other stuff too.
Here are some posts I've written recently:

{% assign best_posts = site.posts | sort: "date" | reverse | slice: 0, 4 %}

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

{% assign last_post = best_posts | last %}

<style>
  @media screen and (max-width: 500px) {
    #{{ last_post.slug }} {
      display: none;
    }
  }

  @media screen and (min-width: 1000px) {
    #{{ last_post.slug }} {
      display: none;
    }
  }
</style>

{% comment %}
  For consistency with the "all posts" page, any blog posts that don't
  set an explicit colour get tinted the default red on the homepage.
{% endcomment %}
{% assign is_index = true %}

<ul class="post_cards">
{% for post in best_posts %}
  {% include post_card.html %}
{% endfor %}
</ul>

You can see [more of my blog posts](/all-posts/), or [subscribe to the RSS feed](/atom.xml).

{% separator "leaf.svg" %}

## Contact

You can email me at <a href="mailto:alex@alexwlchan.net" aria-label="alex at alex w l chan dot net" aria-braillelabel="alex@alexwlchan.net">alex@alexwlchan.net</a>, or I'm <a href="https://twitter.com/alexwlchan" aria-label="alex w l chan" aria-braillelabel="@alexwlchan">@alexwlchan</a> on Twitter.

If you enjoy what I've made, perhaps [say thanks](/say-thanks/)?
I always love hearing from readers! ☺️
