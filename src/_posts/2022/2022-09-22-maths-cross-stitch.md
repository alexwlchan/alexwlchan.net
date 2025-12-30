---
layout: post
date: 2022-09-22 21:32:14 +0000
title: The maths cross-stitch that hangs behind me
summary: When I’m on video calls, my backdrop has some maths-related art that I helped to make.
tags:
  - cross-stitch
  - maths
colors:
  css_light: "#742a0c"
  css_dark:  "#b7834f"
is_featured: true
---

<style>
  .me_on_a_video_call {
    width: 245px;
  }

  /* This is a sneaky wheeze to make the photo appear:
   *
   *    1) inline with the text on desktop browsers
   *    2) in its own paragraph on mobile browsers
   */
  .desktop_only {
    display: none;
  }

  @media screen and (max-width: 500px) {
    .desktop_only {
      display: none;
    }

    .mobile_only {
      display: block;
    }
  }

  @media screen and (min-width: 500px) {
    .desktop_only {
      display: inline-block;
      float: right;
    }

    .mobile_only {
      display: none;
    }
  }
</style>

<p>
  {%
    picture
    filename="me_on_a_video_call.jpg"
    width="245"
    alt="A thumbnail of me on a video call. Behind me is a featureless grey wall, a white door, and a wooden-framed picture with indistinct coloured squares."
    class="me_on_a_video_call desktop_only"
  %}
  I was chatting to a new colleague last week, and she asked about the picture that hangs behind me when I’m on video calls – which made me realise I’ve never posted about it here.
  It’s a rather nice piece that I’m quite pleased with, and it’s worth sharing.
</p>

{%
  picture
  filename="me_on_a_video_call.jpg"
  width="245"
  alt="A thumbnail of me on a video call. Behind me is a featureless grey wall, a white door, and a wooden-framed picture with indistinct coloured squares."
  class="me_on_a_video_call mobile_only"
%}

Most of my backdrop is pretty dull: a closed white door and some grey walls.
I want to paint this room and add some colour, but disassembling my desk so I can redecorate is a challenge I have yet to tackle.
In the meantime, I added a small piece of art.

I deliberately picked something small but colourful.
I wanted to make my backdrop a bit more interesting than a grey wall, but I didn't want something too big.
I still want to be the main focus of my video, especially if I’m a post-it note sized tile in a large conference call.

This is what it looks like up close:

{%
  picture
  filename="maths_sampler.1.jpg"
  alt="A wodden frame around a cross-stitch picture. The picture is sixteen brightly-coloured squares, arranged in a four-by-four grid. Each square has a different mathematically-related symbol, including a Klein bottle, the digits of pi, a chalkboard, and a sine wave."
  width="950"
  class="wide_img"
%}

It's a piece of cross-stitch I made at the end of 2020.
People are often surprised – when we're on a video call, they think it's a painting!

The pattern is a [maths sampler][pattern] I bought from [Mathysphere], who makes some gorgeous designs.
I did have to adjust a couple of the colours (in particular the hypercube and dodecahedron, which I'm still not 100% happy with), but mostly it's straight from the pattern.
Like a lot of my other pieces, it was framed by [Landseer Picture Framing].

There are explanations (and close-up photos) of what's in each square on [Mathysphere's Tumblr][tumblr].
I'm a big fan of their work: the designs are lovely, the colours are great, and the patterns are easy to follow.
I'm also working my way through the Pride Planets series, and I've bought their patterns for several people.
I suspect I’ll do another sampler soon, but I'm not sure which.

It took about two months from start to finish (and then another few weeks to frame).
If you're looking for a project, this was fun to make, not too long, and I love the final result.

[pattern]: https://www.etsy.com/uk/listing/498963139/math-sampler-cross-stitch-pattern-pdf
[Mathysphere]: https://www.etsy.com/uk/shop/Mathysphere
[Landseer Picture Framing]: https://landseerpictureframes.co.uk/
[tumblr]: https://mathysphere.tumblr.com/tagged/math%20sampler
