---
layout: post
date: 2020-01-16 22:56:51 +0000
title: Generating pride-themed Norse valknuts with Python 🌈
summary: A web app to generate mashups of Norse valknuts and Pride flags.
link: https://alexwlchan.net/fun-stuff/rainbow-valknuts/
tags:
  - python
  - glitch
  - generative art
  - fun stuff
  - drawing things
colors:
  index_light: "#e31b85"
  index_dark:  "#c8c8c8"
---

You might remember a couple of months back, I was playing with [alternative coordinate systems in SVG](/2019/triangular-coordinates-in-svg/).
There are some shapes which are easier to define with triangular coordinates than regular (*x*,*y*)-coordinates, and I created some Python functions to let me switch between the two coordinate systems.

One shape that's much easier to define in triangular coordinates is the [valknut], a symbol made from three interlocked triangles that appears on a lot of objects from ancient Germanic cultures:

[valknut]: https://en.wikipedia.org/wiki/Valknut

<figure style="width: 380px;">
  {%
    inline_svg
    filename="valknut.svg"
    alt="Three black interlocking triangles"
  %}
  <figcaption>
    Image of a Valknut created by Wikipedia users <a href="https://commons.wikimedia.org/wiki/File:Valknut.svg">Nyo and Liftarn</a>.
    Used under CC-BY.
  </figcaption>
</figure>

There are two variables here: the width of the bars, and the width of the gaps.
If you start at the lower left-hand corner, you can use triangular coordinates to define every point on this shape in terms of those two variables.
This is what I wanted to draw using SVG.

So why was I trying to draw a valknut?

The valknut is also used by some white nationalist groups, which prompted [this tweet by @KlezmerGryphon](https://twitter.com/KlezmerGryphon/status/1173897515843735553).
*"Hey, Nazis, I got a message for ya from Odin"*, along with a picture of a valknut coloured with the stripes of several pride flags.
I liked their design, and I wanted to try reproducing it as an SVG.

The original post was some of my early research into triangular coordinates, but it wasn't until recently that I came back to the rainbow valknuts.

About two weeks ago, I got the code working, and created a small [Flask] app that generates valknuts made from different pride flags.
This is what it looks like:

[Flask]: https://flask.palletsprojects.com/en/1.1.x/

{%
  picture
  filename="rainbow_valknuts_screenshot.png"
  width="652"
  alt="Three interlocking triangles, made from the stripes of the non-binary (yellow, white, purple, black), pansexual (pink, yellow, blue) and aromantic (green, grey, white, black) pride flags."
  link_to="/fun-stuff/rainbow-valknuts/?flag_0=aromantic&flag_1=non-binary&flag_2=pansexual"
  class="dark_aware screenshot"
%}

It picks a random selection of three flags every time you reload the page, or you can get a permalink to save that particular image.
The list of flags comes from the [QueerJS website](https://queerjs.com/flags).

If you're interested, you can play with the app at [alexwlchan.net/fun-stuff/rainbow-valknuts/](/fun-stuff/rainbow-valknuts/).
