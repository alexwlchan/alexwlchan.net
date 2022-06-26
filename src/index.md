---
layout: page
title: ""
theme:
  color: "#17823e"
---

<img src="/images/profile_green_1x.jpg" srcset="/images/profile_green_1x.jpg 1x, /images/profile_green_2x.jpg 2x" alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants.">

## Hi, I'm Alex.

I'm a software developer at [Wellcome Collection][wellcome], a free museum and library in London.
I help to search and store [the collections][collections], with a particular interest in digital preservation.

I have a fairly active online presence -- I [tweet a lot](https://twitter.com/alexwlchan), and [my blog](/best-of/) is where I share ideas that don't fit into a tweet.
You can read my posts on the web, or subscribe to them [as an RSS feed](/atom.xml).

I write about anything I find interesting or fun -- there's plenty of programming, but lots of other stuff too.
Past topics include [accessibility](/2019/01/monki-gras-the-curb-cut-effect/), [Chinese dictionaries](/2019/06/reading-a-chinese-dictionary/), and [Welsh waterfalls](/2018/11/aberdulais-waterfall/).

If you'd like to see everything I've been up to, my [projects page](/projects/) is a good starting point.
It includes links to everything I've published online.

I'm trans, genderfluid, and my pronouns vary.
If you're not sure, "they/them" is a safe default.

I hope you enjoy the site.

[wellcome]: https://wellcomecollection.org/
[collections]: https://wellcomecollection.org/collections



## Blog posts

Here are some posts I've written recently:

{% assign best_posts = site.posts | sort: "date" | reverse | slice: 0, 4 %}

<!--
  The styles in "article_cards.scss" will switch between three layouts:

  *   a 1×3 column (mobile devices)
  *   a 2×2 grid (regular screens)
  *   a 3×1 row (wide screens)

  This is meant to be a sample of posts, not a full list.  I don't want
  too many on mobile devices, and I don't want a single item on its own
  on the second row on a wide screen.

  This CSS will hide the fourth post on mobile/wide screens.
-->

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

<ul class="post_cards">
{% for post in best_posts %}
  {% include post_card.html %}
{% endfor %}
</ul>

You can see [more of my blog posts](/all-posts/), or [subscribe to the RSS feed](/atom.xml).

## Contact

You can email me at {{ site.emails.personal | create_mailto_link }}, or I'm [@alexwlchan](https://twitter.com/alexwlchan) on Twitter.

For anything related to Wellcome, email {{ site.emails.wellcome | create_mailto_link }}.

If you enjoy what I write, perhaps [say thanks](/say-thanks/)?
