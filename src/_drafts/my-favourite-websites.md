---
layout: post
title: Some cool websites from my bookmark collection
summary:
tags:
  - bookmarking
  - web development
colors:
  css_light: "#0000ff"
  css_dark:  "#00ddff"
---
Over the last three weeks, I've been writing about how I manage my bookmarks.
how I use a static site to store them, how I built a personal web archive by hand, and what I learnt about web development along the way.
I wanted to end this series on a lighter note, so here's a handful of my favorite sites I rediscovered while reviewing my bookmarks – fun, creative corners of the web that make me smile.

<blockquote class="toc">
  <p>This article is the final part of a four part bookmarking mini-series:</p>
  <ol>
    <li>
      <a href="/2025/bookmarks-static-site/"><strong>Creating a static site for all my bookmarks</strong></a> – why do I bookmark, why use a static site, and how does it work.
    </li>
    <li>
      <a href="/2025/creating-bookmark-archives"><strong>Creating a local archive of all my bookmarks</strong></a> – web archiving, automated vs manual, what I learnt about preserving web pages.
    </li>
    <li>
      <strong><a href="http://localhost:5757/2025/how-to-make-websites/">Learning how to make websites by reading two thousand web pages</a></strong>
    </li>
    <li>
      <a href="#"><strong>Some cool websites from my bookmark collection</strong></a> (this article)
    </li>
  </ol>
</blockquote>

<style>
  .toc {
    background: var(--background-color);
    border-color: var(--primary-color);
  }

  .toc ol > li:not(:last-child) {
    margin-bottom: 1em;
  }

  .toc ol > li > ul {
    list-style-type: disc;
  }

  .toc ol > li > ul > li > ul {
    list-style-type: circle;
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>

---

## The ever-changing "planets" of panic.org

Jason Kottke's website, [kottke.org], has a sidebar that shows four coloured circles, [different for every visitor][redesign].
There are nearly a trillion possible combinations, which feels fun and whimsical -- everyone gets their own unique version of the page.

<figure style="width: 600px;">
  {%
    picture
    filename="bookmarks/kottke.png"
    width="600"
    class="screenshot"
    alt="A web page with black text on a white background, and down the left hand side are four circles showing different textures in a variety of pink/red shades."
  %}
  <figcaption>
    I happened to capture a particularly aesthetically pleasing collection of reds and pinks in this preserved snapshot.
    They add a pop of colour to the page, but they don’t overwhelm it.
  </figcaption>
</figure>

I've tried adding this sort of randomness to my own sites, but it's easy to get wrong.
My experiments often failed because they lacked constraints -- for example, I'd pick random tint colours, but some combinations were unreadable.
The Kottke "planets" strike a nice balance: the randomness stands out, but it's reined in so it will always look good.

There are thousands of snapshots of kottke.org in the Wayback Machine, many saved automatically and never seen by a person.
That means there are unique combinations of circles already archived -- frozen moments that may only be seen by a future reader, long after this design has gone.
I rather like that: a tiny, quiet, time capsule on the web.

[kottke.org]: https://kottke.org/
[redesign]: https://kottke.org/24/03/kottkeorg-redesigns-with-2024-vibes#:~:text=Billions%20and%20Billions.





## Physical meets digital on panic.org

The software company [Panic] has a circular logo: [a stylised "P"][logo] on a two-tone blue background.
But for years, if you visited their website, you might see that logo in a different colour, like this:

<figure style="width: calc(600px + 10px); display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 10px;">
  {%
    picture
    filename="bookmarks/panic_blue.png"
    width="300"
    class="screenshot"
    alt="A screenshot of the Panic blog, with a dark blue P logo in the top left-hand corner."
    style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
  %}
  {%
    picture
    filename="bookmarks/panic_green.png"
    width="300"
    class="screenshot"
    alt="A screenshot of the Panic blog, with a red/green P logo in the top left-hand corner."
    style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
  %}
</figure>

Where did those colours come from?
The logo image was loaded from `signserver.panic.com`, which makes me think it reflected the current colours of [the physical sign on their building][panic_sign].
They even had a website where anybody could change the colours of the sign (though it's offline now -- they took the sign down when they moved offices).

I love this detail: a tiny bit of the physical world seeping into the digital.

[Panic]: https://panic.com
[logo]: https://commons.wikimedia.org/wiki/File:Panic_Inc_Logo.svg
[panic_sign]: https://panic.com/blog/the-panic-sign/



## A Tumblr theme that follows the sun

One of my [bookmarked Tumblr posts][vonnegut] has a remarkable theme by a Tumblr Laighlin called [Circadium 2.0][circadium].
Forget a binary light and dark mode, this is a theme that gradually changes the appearance through the entire day.
It cycles through noon, twilight, and dusk, before starting the same thing over again.

[vonnegut]: https://three--rings.tumblr.com/post/625948601747636224/when-i-was-15-i-spent-a-month-working-on-an
[circadium]: https://linthm.tumblr.com/post/626279447390257152/theme-28-circadium-20-yes-sweet-baby-jesus

* backgrounds that follow the sun / [[Screenshot 2024-11-07 at 21.59.20.png]] / [[Screenshot 2024-11-07 at 21.59.22.png]] / https://three--rings.tumblr.com/post/625948601747636224/when-i-was-15-i-spent-a-month-working-on-an

* owltastic

* The changing colours of Campo Santo

* Reblog graphs on Tumblr

* Stacking the bricks, literally

* The Obsidian icon picker

* fun comments

    mango.zone:

    ```
        <!-- NSA has been very good this year so let's give them a little treat -->
        <script async="" src="https://www.google-analytics.com/analytics.js"></script><script async="" src="https://www.googletagmanager.com/gtag/js?id=G-ZMYRY9GN5C"></script>

    ```



    Carl Flax:

    ```
    <!-- If you're reading this, go for a walk. :) -->
    ```
