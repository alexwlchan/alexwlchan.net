---
layout: page
title: ""
colors:
  css_light: "#17823e"
  css_dark:  "#26d967"
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

  svg[role="separator"] {
    display: block;
  }
</style>

<p class="fullwidth_img">
  {%
    picture
    filename="profile_green.jpg"
    parent="/images"
    visible_width="750px"
    extra_widths="500px, 640px, 1000px, 1250px"
    alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants."
    class="rounded_corners"
  %}
</p>

## Hi, I'm Alex.

I've put a bunch of things on the Internet, including:

*   [**My personal blog**](/posts/), which covers a range of topics, from programming to photography, from colour theory to Chinese dictionaries.
    I've been writing at this domain for over a decade, and I post new articles several times a month.

*   **Everything I do for [Wellcome Collection](/projects/#wellcome-collection)**, a museum and library in London.
    I'm a software engineer, and I'm part of a team that builds the public website, the online [collections search][search], and our cloud-based [preservation storage][storage].

*   **A bunch of [open-source tools and utilities][oss]**.
    I've contributed fixes and patches to dozens of projects, and I've shared a few of my own, including my tool for [managing my scanned files](https://github.com/alexwlchan/docstore) and a way to find the [dominant colours in an image](https://github.com/alexwlchan/dominant_colours).

*   [**Fun and amusing art projects**][fun_stuff], like measuring data [by shelf space in floppy disks](https://howlongismydata.glitch.me/), or controlling a rocket [with the &lt;marquee&gt; tag](https://marquee-rocket.glitch.me/).

When I'm not online, I can often be found with needle in hand, working on some cross-stitch or embroidery, or with shoes on feet, tapping away to a funky jazz number at a swing dance class.
I have two left feet, but what I lack in skill I make up for in enthusiasm.

I'm queer, trans, and I loosely describe as a genderfluid shapeshifter (which may mean more to me than anyone else).
My pronouns vary; on the web, either "they" or "she" are safe choices. 🏳️‍🌈

This site is a one-stop shop for everything I've put online -- it's either here, or linked to from here.
If you're new, you might want to start with [my blog](/posts/) or [my list of projects](/projects/).

I hope you enjoy it.

[search]: https://stacks.wellcomecollection.org/building-our-new-unified-collections-search-ed399c412b01
[storage]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e
[oss]: /projects/#personal-tools
[fun_stuff]: /projects/#fun-stuff



  {% separator "leaf.svg" %}



<h2 id="contact">Get in touch</h2>

The best way to get in touch with me is by email:

{% include contact/emails.html %}

{% comment %}
  You can also follow me on social media, where I often cross-post links to new articles and share shorter updates about my life:

  {% include contact/socials.html %}
{% endcomment %}

If you enjoy something I've made, perhaps [say thanks](/say-thanks/)?
I always love hearing from readers! ☺️


  {% separator "leaf.svg" %}


## My writing

I write about anything I find interesting or fun – there’s plenty of programming, but lots of other stuff too.
Here are some of my favourite posts:

{%
  include
  eggbox.html
  eggbox_posts="snapped-elastic bure-valley moomin-mathematics graph-generative-art archival-storage-service 2022-in-reading"
%}

If you want to read more, there are plenty more [in the archive](/posts/).


  {% separator "leaf.svg" %}


## My newest posts

I typically write three or four new posts a month.
If you want to hear about them, you can [subscribe to my RSS feed](/atom.xml) or [follow me on social media](/contact/).

Here's what I've written recently:

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

<style>
  @media screen and (max-width: 500px) {
    #recent_posts li:nth-child(4) {
      display: none;
    }
  }

  @media screen and (min-width: 1000px) {
    #recent_posts li:nth-child(4) {
      display: none;
    }
  }
</style>

{% comment %}
  For consistency with the "all posts" page, any blog posts that don't
  set an explicit colour get tinted the default red on the homepage.
{% endcomment %}
{% assign is_index = true %}

<ul id="recent_posts" class="post_cards">
{% for post in recent_posts %}
  {% include post_card.html %}
{% endfor %}
</ul>
