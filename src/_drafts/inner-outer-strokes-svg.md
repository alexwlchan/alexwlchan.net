---
layout: post
title: Drawing inner/outer strokes in SVG
summary:
tags: svg
---

I make a lot of box-and-arrow diagrams, and I typically make them as [SVGs].
These simple diagrams work well as vector images, I can store them as text along source code, and they look sharp at any size.
I write most of my SVGs by hand, rather than using an app like Illustrator or Inkscape.
Although it's more effort, it forces me to really understand how SVG works.

<figure style="width: 200px; float: right; display: inline-block; margin-top: 0; margin-bottom: 0;">
{% inline_svg "_images/2021/hearts_rainbow_trans.svg" %}
</figure>

At the weekend, I wrote a fun little app to make SVGs of [interlocking rainbow hearts].
It was partly for fun, partly to play with some SVG features that I hadn't used before: [clipping and masking].

As part of the app, I came up with a way to draw inner and outer strokes using SVG.
This seems like something I might use again, and it helped me understand both features, so in this post I'm going to explain how I did this.


[SVGs]: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
[interlocking rainbow hearts]: /2021/03/rainbow-hearts/
[clipping and masking]: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Clipping_and_masking



## What are inner and outer strokes?

In vector graphics, a [*stroke*] is how you draw a path.
In this context, I'm thinking of the path that encloses an entire shape; its outline.

Normally, the stroke is centred on the boundary of the shape: that is, half of the stroke is inside the shape, and half of it is outside.
This means the visible width of the shape is actually the width of the shape *plus* the width of the stroke.
(You get an extra half a stroke's width on both sides of the shape -- thus, an extra stroke width.)

In some graphics programs, you can choose to draw an *inner stroke* (which puts the entire stroke inside the shape) or an *outer stroke* (which puts the entire stroke outside the shape):

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_1_types.svg" %}
</figure>

Although the square is the same size in all three cases, notice how the stroke alignment changes the size of the final image.

There have been several proposals to make stroke alignment part of the SVG spec, so you could use `stroke-alignment="inner"` to position your strokes, but so far none of them have been accepted.
I found a [Stack Overflow thread] that links to several of the proposals, and which also gave me some ideas about how I'd implement this myself.

[*stroke*]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke
[Stack Overflow thread]: https://stackoverflow.com/q/7241393/1558022



## Why do I want inner and outer strokes?

When I made my initial heart graphic in [OmniGraffle], I combined inner and outer strokes to create something that looked like a striped stroke.

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_2_combined.svg" %}
</figure>

By adding more strokes of different widths, you can create more complex stripes.
For example, to draw four stripes, you could draw two outer strokes and two inner strokes.

I wanted to replicate this effect in SVG so that I could construct shapes with striped strokes.

This tends to look better than combining different sizes of the same shape.
Using inner/outer strokes gives a consistent, even line around the whole shape, whereas combining multiple sizes gives a messier result.
Notice how the red stripe is much thicker than the blue stripe, and the width of the blue stripe is inconsistent:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_3_sizes.svg" %}
</figure>

For more complex shapes, it gets even harder (sometimes impossible) to combine multiple sizes in a way that doesn't leave gaps.

[OmniGraffle]: https://www.omnigroup.com/omnigraffle



## Drawing an inner stroke with clipping

You can draw an inside stroke by drawing a double-width centred stroke, and discarding the half of the stroke outside the boundary of the shape -- or alternatively, only including the half that's inside the shape.

We can achieve this effect with an SVG feature called *clipping*.

A clip defines an outline, and only the area inside the outline is visible.
For example, if I had [a picture of the Earth] and I wanted to remove the background around it, I could add a circular clip, and only the planet would be shown:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_4_circular_clip.svg" %}
</figure>

Here's how the clipped image works:

```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="insideCircleOnly">
      <circle cx="50" cy="50" r="45"/>
    </clipPath>
  </defs>

  <image
    href="globe.jpg" height="100" width="100"
    clip-path="url(#insideCircleOnly)"/>
</svg>
```

We start by defining a `<clipPath>`, which contains a single shape -- the circle we want to clip.
Then we reference the clipPath in the `clip-path` attribute of our image, and the SVG renderer only shows the parts of the image inside the circle.

But a clip isn't restricted to simple geometric shapes like circles and squares -- a clip can follow an arbitrary path, including along the path of the shape we want to outline.
This is how we can draw inner strokes:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_5_clip_inner_stroke.svg" %}
</figure>

And here's what that looks like:

```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Based on the heart from https://thenounproject.com/search/?q=heart&i=585522 -->
    <path id="heart" d="m 31,11.375 c -14.986319,0 -25,12.30467 -25,26 0,12.8493 7.296975,23.9547 16.21875,32.7188 8.921775,8.764 19.568704,15.2612 26.875,19.0312 a 2.0002,2.0002 0 0 0 1.8125,0 c 7.306296,-3.77 17.953225,-10.2672 26.875,-19.0312 C 86.703025,61.3297 94,50.2243 94,37.375 c 0,-13.69533 -10.013684,-26 -25,-26 -8.834204,0 -14.702885,4.50444 -19,10.59375 C 45.702885,15.87944 39.834204,11.375 31,11.375 z"/>

    <clipPath id="insideHeartOnly">
      <use xlink:href="#heart"/>
    </clipPath>
  </defs>

  <use
    xlink:href="#heart"
    stroke-width="20" stroke="black" fill="white"
    clip-path="url(#insideHeartOnly)"/>
</svg>
```

By changing the `<path>`, you change the shape -- and in turn, it changes the clip which helps to draw the inner stroke.

[a picture of the Earth]: https://wellcomecollection.org/works/uhemygps

---
---
---
---
---
---

AAAAAA

## Drawing an outer stroke with clipping

We might be tempted to use a similar approach to draw an outer stroke.
Draw a double-width centred stroke, and discard the half of the stroke inside the boundary of the shape -- or use a clip to only include the half that's outside.

As far as I know, there's no builtin way to "invert" a clip -- that is, to show everything outside rather than inside.

One way to do this is to draw a rectangle around the boundary of your entire drawing, and then create a zero-width "bridge" from the rectangle to your original clip -- this new clip would surround everything *except* that original clip.
I've exaggerated the width of the bridge in the illustration, but hopefully you get the idea:

<img src="/images/2021/bridged_clip.png" style="width: 686px;">

This works, but it's not ideal -- it may not be obvious where we need to create this "bridge", and you might have to move it if the clip changes.
Is there a better way?



## Drawing an outer stroke with masks

SVG has another feature called *masking*, which is a more powerful way to select parts of an image.
Rather than providing a simple "on/off", it allows us to control the opacity of the underlying image.

A *mask* is a black-and-white graphic.
When you overlay a mask on an image, anything under the black parts of the mask is completely hidden, and anything under the white parts is fully shown.
For example, we can recreate our original circular clip using a mask:

<img src="/images/2021/circular_mask.png" style="width: 686px;">

Here's what the SVG looks like:

```xml
SVG GOES HERE
```

Masks allow more sophisticated effects -- by picking shades of grey, we can precisely control the opacity of the image that shines through.
I'll include an example here, because this fine-grained control is the key difference between clips and masks, but we're not going to use it again in this post.

<img src="/images/2021/checkerboard_mask.png" style="width: 686px;">

If we start with an all-white background, then add our shape in black, we have a mask that will discard everything inside the boundary of the shape.
This gives us a way to draw outside strokes:

<img src="/images/2021/outer_stroke_mask.png" style="width: 686px;">

Here's what the corresponding SVG looks like:

```xml
SVG GOES HERE
```

As with the inner stroke, you can adapt this to any shape by changing the `<path>`.



## Putting it all together

Although I have the code to do inner and outer strokes, for the hearts app I ended up just using centred strokes and inner strokes.
If you put the inner stripes on top of a double-width centred stroke, you get the same effect, and this was slightly simpler to implement:

<img src="/images/2021/stacked_stripe_stroke.png" style="width: 686px;">

And to create the interlocking hearts, I created some masks to cut out a part of each heart where it was crossed by the other:

<img src="/images/2021/linked_hearts_mask.png" style="width: 686px;">
