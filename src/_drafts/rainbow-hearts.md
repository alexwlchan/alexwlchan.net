---
layout: post
title: Creating pairs of interlocking rainbow hearts 🌈
tags: glitch generative-art
link: https://rainbow-hearts.glitch.me/
---

Here's a fun project I made today: create pairs of interlocking rainbow hearts: <http://rainbow-hearts.glitch.me>

The app makes transparent SVGs, which you can resize and drop on top of any background.
Here's a few examples:

<style>
  #grid-container {
    display: grid;
    grid-template-columns: 66% 32%;
    grid-gap: 1%;
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
    width: 100%;
  }
</style>

<div id="grid-container">
  <div class="grid-item" id="grid-item1">
    <a href="/images/2021/heart_examples1.jpg">
      <img src="/images/2021/heart_examples1.jpg" srcset="/images/2021/heart_examples1_1x.jpg 1x, /images/2021/heart_examples1.jpg 2x" alt="Two interlocking hearts. The left heart is the colours of the asexual pride flag (black, grey, white, purple), and the right heart is the colours of the aromantic pride flag (dark green, light green, white, grey, black)."/>
    </a>
  </div>
  <div class="grid-item" id="grid-item2">
    <a href="/images/2021/heart_examples2.jpg">
      <img src="/images/2021/heart_examples2.jpg" srcset="/images/2021/heart_examples2_1x.jpg 1x, /images/2021/heart_examples2.jpg 2x" alt="Two interlocking hearts on a dark background. The left heart is the colours of the rainbow pride flag (red, orange, yellow, green, blue, purple), and the right heart is the colours of the trans pride flag (baby blue, baby pink, white, baby pink, baby blue)."/>
    </a>
  </div>
  <div class="grid-item" id="grid-item3">
    <a href="/images/2021/heart_examples3.jpg">
      <img src="/images/2021/heart_examples3.jpg" srcset="/images/2021/heart_examples3_1x.jpg 1x, /images/2021/heart_examples3.jpg 2x" alt="Two interlocking hearts. The left heart is the colours of the black trans pride flag (baby blue, baby pink, black, baby pink, baby blue), and the right heart is the colours of the bi pride flag (dark pink, purple, dark blue)."/>
    </a>
  </div>
</div>

This idea came from a [similar graphic I made for Valentine's Day](https://twitter.com/alexwlchan/status/1360919253738790915).
I used several tools to make it, and I had to assemble the final result by hand -- I wanted to see if I could create a pair of interlocked hearts as a single SVG.

Last year, I made an app for generating [rainbow Norse Valknuts](/2020/01/pride-valknuts/), and I was able to reuse some of the code -- but those were easier to draw then hearts.
Valknuts use all straight lines, so I could calculate exactly where each stripe should start/end.
Because hearts have curved sides, I had to do a bit more work to draw the overlaps.

I experimented with a combination of SVG clips and masks to get the final effect, and this was a fun project to learn how they work.
I write SVGs by hand, rather than using an app like Inkscape or Illustrator -- so understanding the core primitives is really useful.
I did learn a few useful things, which I'll write about as a separate blog post.

There is more that unites the LGBTQ+ community than divides us, and I like these hearts as a visual reminder of that.

