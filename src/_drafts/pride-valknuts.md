---
layout: post
title: Generating pride-themed Norse valknuts with Python 🌈
category: Glitch apps
link: https://rainbow-valknuts.glitch.me/
---

You might remember a couple of months back, I was playing with [alternative coordinate systems in SVG](/2019/09/triangular-coordinates-in-svg/).
There are some shapes which are easier to define with triangular coordinates than regular (*x*,*y*)-coordinates, and I created some Python functions to let me switch between the two coordinate systems.

One shape that's much easier to define in triangular coordinates is the [valknut], a symbol made from three interlocked triangles that appears on a lot of objects from ancient Germanic cultures:

[valknut]: https://en.wikipedia.org/wiki/Valknut

<figure style="width: 380px;">
  <img src="/images/2020/valknut.svg" alt="Three black interlocking triangles.">
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

<a href="https://rainbow-valknuts.glitch.me/?flag_0=aromantic&flag_1=non-binary&flag_2=pansexual">
  <img src="/images/2020/rainbow_valknuts_screenshot.png" alt="Three interlocking triangles, made from the stripes of the non-binary (yellow, white, purple, black), pansexual (pink, yellow, blue) and aromantic (green, grey, white, black) pride flags.">
</a>

It picks a random selection of three flags every time you reload the page, or you can get a permalink to save that particular image.
The list of flags comes from the [QueerJS website](https://queerjs.com/flags).

If you're interested, you can play with the app at <https://rainbow-valknuts.glitch.me/>, or browse the source code [on GitHub](https://github.com/alexwlchan/rainbow-valknuts).

This was a fun little project to work on, and I'm hoping to do more fun things like this in 2020.
I'm especially enjoying [Glitch](https://glitch.com) as a place to host these one-off, whimsical bits of code – I'll hopefully write more about it soon.
