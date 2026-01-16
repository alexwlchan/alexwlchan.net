---
layout: til
date: 2024-06-08 11:11:25 +01:00
title: Removing letterboxing from a video screenshot with ImageMagick
summary: |
  Using `-trim` will remove the black portions and leave you the unletterboxed image.
tags:
  - imagemagick
---
I was doing some work today with screenshots of a video that had [black "letterboxing" bars](https://en.wikipedia.org/wiki/Letterboxing_%28filming%29) around it.
If you use `convert [input] -trim [output]`, you can remove this with ImageMagick.

If the bars aren't pure black, you can add `-fuzz 10%` to pick up dark greys also.

<style>
  #examples {
    display: grid;
    grid-template-columns: 250px auto;
    grid-gap: 1em;
    align-items: center;
  }

  #examples pre {
    margin: 0;
  }
</style>

<div id="examples">
  <img src="/images/2024/Windowboxed.jpg" alt="">
  <p>
    Original file, from <a href="https://en.wikipedia.org/wiki/File:Windowboxed.jpg">Wikimedia Commons</a>
  </p>

  <img src="/images/2024/Unboxed.jpg" alt="">
  <pre><code>convert Windowboxed.jpg -trim Unboxed.jpg</code></pre>

  <img src="/images/2024/Unboxed_10.jpg" alt="">
  <pre><code>convert Windowboxed.jpg -fuzz 10% -trim Unboxed.jpg</code></pre>
</div>
