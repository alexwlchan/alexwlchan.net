---
layout: post
date: 2021-03-07 10:53:24 +00:00
title: Creating pairs of interlocking rainbow hearts 🌈
summary: A web app for creating pairs of hearts based on Pride flags.
tags:
  - glitch
  - generative art
  - fun stuff
link: https://alexwlchan.net/fun-stuff/rainbow-hearts/
colors:
  index_light: "#870788"
  index_dark:  "#a86da8"
---

<style type="x-text/scss">
  #grid-container {
    display: grid;
    grid-template-columns: 66% 32%;
    grid-gap: var(--grid-gap);
    height: 50%;
  }

  #grid-item1 {
    grid-column: 1;
    grid-row: 1 / 3;
  }

  #grid-item2 {
    grid-column: 2;
    grid-row: 1;
  }

  #grid-item3 {
    grid-column: 2;
    grid-row: 2;
  }

  .grid-item img {
    object-fit: cover;
    height: 100%;
    width:  100%;
  }
</style>

Here's a fun project I made today: create pairs of interlocking rainbow hearts: [alexwlchan.net/fun-stuff/rainbow-hearts/](/fun-stuff/rainbow-hearts/)

The app makes transparent SVGs based on pride flags, which you can resize and drop on top of any background.
Here's a few examples:

<div id="grid-container">
  <div class="grid-item" id="grid-item1">
    {%
      picture
      filename="heart_examples1.jpg"
      alt="Two interlocking hearts. The left heart is the colours of the asexual pride flag (black, grey, white, purple), and the right heart is the colours of the aromantic pride flag (dark green, light green, white, grey, black)."
      width="495"
    %}
  </div>
  <div class="grid-item" id="grid-item2">
    {%
      picture
      filename="heart_examples2.jpg"
      alt="Two interlocking hearts on a dark background. The left heart is the colours of the rainbow pride flag (red, orange, yellow, green, blue, purple), and the right heart is the colours of the trans pride flag (baby blue, baby pink, white, baby pink, baby blue)."
      width="248"
    %}
  </div>
  <div class="grid-item" id="grid-item3">
    {%
      picture
      filename="heart_examples3.jpg"
      alt="Two interlocking hearts. The left heart is the colours of the black trans pride flag (baby blue, baby pink, black, baby pink, baby blue), and the right heart is the colours of the bi pride flag (dark pink, purple, dark blue)."
      width="248"
    %}
  </div>
</div>

This idea came from a [similar graphic I made for Valentine's Day](https://twitter.com/alexwlchan/status/1360919253738790915).
I used several tools to make it, and I had to assemble the final result by hand -- I wanted to see if I could create a pair of interlocked hearts as a single SVG.

Last year, I made an app for generating [rainbow Norse Valknuts](/2020/pride-valknuts/), and I was able to reuse some of the code -- although those were easier to draw then hearts.
Valknuts use all straight lines, so I could calculate exactly where each stripe should start/end.
Because hearts have curved sides, I had to do a bit more work to draw the overlaps.

I experimented with a combination of SVG clips and masks to get the final effect, and this was a fun project to learn how they work.
I write SVGs by hand, rather than using an app like Inkscape or Illustrator -- so understanding the core primitives is really useful.
I did learn a few useful things, which I'll write about as a separate blog post.

You can create your own hearts at [alexwlchan.net/fun-stuff/rainbow-hearts/](/fun-stuff/rainbow-hearts/).

There is more that unites the LGBTQ+ community than divides us, and I like these hearts as a visual reminder of that.

