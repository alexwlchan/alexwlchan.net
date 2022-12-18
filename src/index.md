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

<p class="fullwidth_img">
  <picture>
    <source
      srcset="/images/profile_green_1x.webp 1x,
              /images/profile_green_2x.webp 2x,
              /images/profile_green_3x.webp 3x,
              /images/profile_green_4x.webp 4x"
      type="image/webp"
    >
    <source
      srcset="/images/profile_green_1x.jpg 1x,
              /images/profile_green_2x.jpg 2x,
              /images/profile_green_3x.jpg 3x,
              /images/profile_green_4x.jpg 4x"
      type="image/jpeg"
    >
    <img
      src="/images/profile_green_1x.jpg"
      alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants."
      class="rounded_corners"
      width="750"
      height="563"
    >
  </picture>
</p>

## Hi, I'm Alex.

I've put a bunch of things on the Internet, including:

*   [**My personal blog**](/all-posts/), which covers a range of topics, from programming to photography, from colour theory to Chinese dictionaries.
    I've been writing at this domain for over a decade, and I post new articles several times a month.

*   **Everything I do for [Wellcome Collection](/projects/#wellcome-collection)**, a museum and library in London.
    I'm a software engineer, and I'm part of a team that builds the public website, the online [collections search][search], and our cloud-based [preservation storage][storage].

*   **A bunch of [open-source tools and utilities][oss]**.
    I've contributed fixes and patches to dozens of projects, and I've shared a few of my own, including my tool for [managing my scanned files](https://github.com/alexwlchan/docstore) and a way to find the [dominant colours in an image](https://github.com/alexwlchan/dominant_colours).

*   [**Fun and amusing art projects**][fun_stuff], like measuring data [by shelf space in floppy disks](https://howlongismydata.glitch.me/), or controlling a rocket [with the &lt;marquee&gt; tag](https://marquee-rocket.glitch.me/).

When I'm not online, I can often be found with needle in hand, working on some cross-stitch or embroidery, or with shoes on feet, tapping away to a funky jazz number at a swing dance class.
I have two left feet, but what I lack in skill I make up for in enthusiasm.

I'm trans, and I loosely describe as a genderfluid shapeshifter (which may mean more to me than anyone else).
My pronouns vary; on the web, either "they" or "she" are safe choices.

This site is a one-stop shop for everything I've put online -- it's either here, or linked to from here.
If you're new, you might want to start with [my blog](/all-posts/) or [my list of projects](/projects/).

I hope you enjoy it.

[search]: https://stacks.wellcomecollection.org/building-our-new-unified-collections-search-ed399c412b01
[storage]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e
[oss]: /projects/#personal-tools
[fun_stuff]: /projects/#fun-stuff



  {% separator "leaf.svg" %}



## Get in touch

You can email me at <a href="mailto:alex@alexwlchan.net" aria-label="alex at alex w l chan dot net" aria-braillelabel="alex@alexwlchan.net">alex@alexwlchan.net</a>, or contact me [another way](/contact/).

If you enjoy what I've made, perhaps [say thanks](/say-thanks/)?
I always love hearing from readers! ☺️


  {% separator "leaf.svg" %}


## Recent blog posts

I write about anything I find interesting or fun – there’s plenty of programming, but lots of other stuff too.
Here are some posts I've written recently:

{% assign recent_posts = site.posts | sort: "date" | reverse | slice: 0, 4 %}

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

{% assign last_post = recent_posts | last %}

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
{% for post in recent_posts %}
  {% include post_card.html %}
{% endfor %}
</ul>

If you want to stay up-to-date with new posts, you can [subscribe to the RSS feed](/atom.xml).
You can also find every post I've written [in the archive](/all-posts/).



  {% separator "leaf.svg" %}



## You may have missed

I've been writing blog posts for over a decade.
These are a few of my favourites:

{% assign old_favourites = "snapped-elastic forth-bridge inner-outer-strokes-svg maths-is-about-facing-ambiguity-not-avoiding-it" | split: " " %}

{% assign sorted_posts = site.posts | sort: "date" | reverse | slice: 0, 4 %}

<ul class="post_cards">
{% for slug in old_favourites %}
  {% assign post = site.posts | where: "slug", slug | first %}
  {% include post_card.html %}
{% endfor %}
</ul>

{% assign last_slug = old_favourites | last %}

<style>
  @media screen and (max-width: 500px) {
    #{{ last_slug }} {
      display: none;
    }
  }

  @media screen and (min-width: 1000px) {
    #{{ last_slug }} {
      display: none;
    }
  }
</style>
