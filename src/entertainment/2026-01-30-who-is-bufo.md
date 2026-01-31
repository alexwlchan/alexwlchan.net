---
layout: note
title: Who is Bufo the frog?
date: 2026-01-30 18:30:44 +00:00
summary: Unpicking the history of a Slack icon.
topic: Entertainment

colors:
  css_light: "#5d7847"
  css_dark:  "#7d946a"
---
When I joined Tailscale, one of the things I had to get used to was "Bufo", a cartoon frog who appears in a variety of poses and emoji.
This is a taste of the over 350 different variants of Bufo emoji in the Tailscale Slack:

<style>
  #bufo_examples {
    display: grid;
    grid-template-columns: repeat(7, auto);
    gap: 1em;
    justify-content: center;
  }
</style>

<figure id="bufo_examples">
  {%
    picture
    filename="bufo-blank-stare.png"
    width="64"
    alt="A green cartoon frog staring blankly into space"
  %}
  {%
    picture
    filename="bufo-bless.png"
    width="64"
    alt="A green cartoon frog holding its hands in prayer"
  %}
  {%
    picture
    filename="bufo-cant-find-a-pull-request.png"
    width="64"
    alt="A green cartoon frog shrugging next to a pull request icon"
  %}
  {%
    picture
    filename="bufo-investigates.png"
    width="64"
    alt="A green cartoon frog stroking his chin and holding up a magnifying glass"
  %}
  {%
    picture
    filename="bufo-thumbs-up.png"
    width="64"
    alt="A green cartoon frog giving you a thumbs up"
  %}
  {%
    picture
    filename="bufo-offers-a-cookie.png"
    width="64"
    alt="A green cartoon frog holding up a cookie"
  %}
  {%
    picture
    filename="bufo-offers-you-a-gdpr-compliant-cookie.png"
    width="64"
    alt="A green cartoon frog holding up a cookie with a GDPR consent form on top of it"
  %}
</figure>

Although I'd never heard of Bufo, his popularity extends well beyond Tailscale -- <a href="https://bufo.fun">bufo.fun</a> is a site with over 1200 Bufos, and <a href="https://bufo.tools">bufo.tools</a> lets you make your own Bufo emoji where he's holding different items.

Where did he come from?

A [GitHub repo][gh-all-the-bufo] with even more Bufo emojis pointed me in the right direction (emphasis mine):

> Bufo also known as Froge or Concerned Frog refers to a set of Discord emotes of a worried or concerned frog expressing various emotions, similar to Pepe emotes. **The frog image comes from the now-inactive mobile game Froge, released in 2014 by Fandom Inc.** and became popularized as a set of Discord emotes starting in 2020.

Fandom Inc. has long-since disappeared from the Internet, but you can see their old website [in the Wayback Machine][wm-fandom-inc].
This is what their homepage looked like in October 2014, about three months after Froge launched:

<figure style="width: 600px;">
  {%
    picture
    filename="fandom_inc.png"
    width="600"
    class="screenshot"
    alt="A web page with a black background, and several areas of content with bright yellow borders. There's a hero image that says ‘welcome’, a list of the team and affiliates, a grid of technology logos, and a carousel of games that Fandom, Inc made."
  %}
  <figcaption>
    Three games coming soon but no mention of the cartoon frog who’d eventually be Fandom,&nbsp;Inc’s most popular character?
    :bufo-looks-sad:
  </figcaption>
</figure>

Although no product page for Froge survives, we can look for other URLs [saved under fandominc.com][wb-fandom-inc-urls], which points to four screenshots and a background image for the game:

<style>
  #screenshots {
    width: 600px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--grid-gap);
    
    a:nth-child(1) img {
      border-top-right-radius:    0;
      border-bottom-left-radius:  0;
      border-bottom-right-radius: 0;
    }
    
    a:nth-child(2) img {
      border-top-left-radius:     0;
      border-bottom-left-radius:  0;
      border-bottom-right-radius: 0;
    }
    
    a:nth-child(3), :nth-child(4) {
      img {
        border-radius: 0;
      }
    }
    
    a:nth-child(5) {
      grid-column: 1 / span 2;
      
      img {
        border-top-left-radius:  0;
        border-top-right-radius: 0;
      }
    }
  }
</style>

<figure id="screenshots">
  {%
    picture
    filename="froge1.png"
    width="300"
    alt="A frog jumping between two lilypads and saying ‘Much jump!!’"
    class="screenshot"
    link_to="https://web.archive.org/web/20190104003053/http://www.fandominc.com/wp-content/uploads/2016/02/thumb/FROGE/1.png"
  %}
  {%
    picture
    filename="froge2.png"
    width="300"
    alt="A frog jumping past a brown frog and saying ‘Very dodge!!’"
    class="screenshot"
    link_to="https://web.archive.org/web/20190104230251/http://www.fandominc.com/wp-content/uploads/2016/02/thumb/FROGE/2.png"
  %}
  {%
    picture
    filename="froge3.png"
    width="300"
    alt="A frog jumping with a burst of yellow energy and saying ‘Chaaaaarge!!!’"
    class="screenshot"
    link_to="https://web.archive.org/web/20190709123350/http://www.fandominc.com/wp-content/uploads/2016/02/thumb/FROGE/3.png"
  %}
  {%
    picture
    filename="froge4.png"
    width="300"
    alt="A frog in a shopkeeper outfit with coins saying ‘Shop!’"
    class="screenshot"
    link_to="https://web.archive.org/web/20190709120408/http://www.fandominc.com/wp-content/uploads/2016/02/thumb/FROGE/4.png"
  %}
  {%
    picture
    filename="frog_e_bg.jpg"
    width="600"
    alt="A game background with the frog in the foreground, some lilypads and the title ‘Froge’ in the background."
    class="screenshot"
    link_to="https://web.archive.org/web/20190709141634/http://www2.fandominc.com/wp-content/uploads/2016/02/frog_e_bg.jpg"
  %}
</figure>

This style of speaking is referencing the [Doge meme][wiki-doge-meme], which became popular in 2013, only a year or so before Froge was released.

The game was released on iOS and Android, and the Wayback Machine has also captured [the Google Play Store page][wb-google-play-store].
That includes a description, several more screenshots, and a video.

The video is broken on that page, but it's an embedded YouTube video, and the original video page has also [been captured by the Wayback Machine][wb-youtube-video].
It leans even harder into the Doge memes, and includes some brief clips of gameplay:

<figure style="width: 540px;">
  <video controls poster="/images/2026/Froge Tips from Froge [AC-grTPpQ2Y].jpg" src="/images/2026/Froge Tips from Froge [AC-grTPpQ2Y].mp4" class="screenshot" style="aspect-ratio: 540 / 360; width: 540px;"></video>
  <figcaption>
    <em>Froge Tips from Froge</em> by Fandom, Inc.
    Originally posted at <a href="https://www.youtube.com/watch?v=AC-grTPpQ2Y">on YouTube</a> in June 2014, and downloaded from <a href="https://web.archive.org/web/20240508235850/youtube.com/watch?v%3DAC-grTPpQ2Y">the Wayback Machine</a> in January 2026.
  </figcaption>
</figure>

Perhaps most interesting is that this includes somebody saying the word "Froge", which sounds like "fro" as in "frolick", "ge" as in "get".
I was expecting something similar to the way "doge" is pronounced, which sounds like "do" as in "dough", "ge" as in "rage".

The existence of this game doesn't explain why Froge became popularised as a Discord and later Slack emote, but that's enough digging for today.
I'll update this note if I find out more information.

[gh-all-the-bufo]: https://github.com/knobiknows/all-the-bufo
[wm-fandom-inc]: https://web.archive.org/web/20141007210811/http://fandominc.com/#/Home
[wb-fandom-inc-urls]: https://web.archive.org/web/*/http://fandominc.com/*
[wb-google-play-store]: https://web.archive.org/web/20141003064418/https://play.google.com/store/apps/details?id=com.fandominc.frogefree
[wiki-doge-meme]: https://en.wikipedia.org/wiki/Doge_(meme)
[wb-youtube-video]: https://web.archive.org/web/20240508235850/youtube.com/watch?v%3DAC-grTPpQ2Y
