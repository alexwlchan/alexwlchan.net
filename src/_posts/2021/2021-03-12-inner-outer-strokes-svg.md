---
layout: post
date: 2021-03-12 14:04:58 +0000
title: Drawing inner/outer strokes in SVG (clips and masks)
summary:
tags: svg
index:
  best_of: true
---

I make a lot of box-and-arrow diagrams, and I typically make them as [SVGs].
Simple diagrams work well as vector images, I can store them as text alongside source code, and they look sharp at any size.
I write most of my SVGs by hand, rather than using an app like Illustrator or Inkscape.
Although it's more effort, I can write much simpler images by hand than with an app, and it forces me to really understand how SVG works.

<figure style="width: 200px; float: right; display: inline-block; margin-top: 0; margin-bottom: 0;">
{% inline_svg "_images/2021/hearts_rainbow_trans.svg" %}
</figure>

At the weekend, I wrote a fun little app to make SVGs of [interlocking rainbow hearts].
It was partly for fun, partly to play with some SVG features that I hadn't used before: [clipping and masking].

As part of the app, I came up with a way to draw inner and outer strokes in SVG.
This seems like something I might use again, and it helped me understand both features, so in this post I'm going to explain how I did it.


[SVGs]: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
[interlocking rainbow hearts]: /2021/03/rainbow-hearts/
[clipping and masking]: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Clipping_and_masking


{% separator "paintbrush.svg" %}


## What are inner and outer strokes?

In vector graphics, a [*stroke*] is a visible line that you draw along a path -- think of it like the stroke of a brush.
In this context, I'm thinking of the path that encloses an entire shape; its outline.

Normally, the stroke is centred on the boundary of the shape: that is, half of the stroke is inside the shape, and half of it is outside.
This means the visible width of the shape is actually the width of the shape *plus* the width of the stroke.
(You get an extra half a stroke's width on both sides of the shape -- thus, an extra stroke width.)

In some graphics programs, you can choose to draw an *inner stroke* (which puts the entire stroke inside the shape) or an *outer stroke* (which puts the entire stroke outside the shape):

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_1_types.svg" %}
</figure>

Although the square is the same size in all three cases, notice how the stroke alignment changes the size of the final shape.

There have been several proposals to make stroke alignment part of the SVG spec, so you could write something like `stroke-alignment="inner"` to position your strokes, but so far none of them have been accepted.
If you're interested, I found a [Stack Overflow thread] that links to several of the proposals -- it also gave me some ideas about how I'd implement this myself.

[*stroke*]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke
[Stack Overflow thread]: https://stackoverflow.com/q/7241393/1558022


{% separator "paintbrush.svg" %}


## Why do I want inner and outer strokes?

When I made my initial heart graphic in [OmniGraffle], I combined inner and outer strokes to create something that looked like a striped stroke.

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_2_combined.svg" %}
</figure>

By adding more strokes of different widths, you can create more complex stripes.
For example, to draw four stripes, you could draw two outer strokes and two inner strokes.

I wanted to replicate this effect in SVG, so that I create the stripes programatically, rather than fiddling around with a graphics program.

Using inner/outer strokes tends to look better than combining different sizes of the same shape.
It gives a consistent, even line around the whole shape, whereas combining different sizes gives a messier result.
Notice how the red stripe is much thicker than the blue stripe, and the width of the blue stripe is inconsistent:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_3_sizes.svg" %}
</figure>

For more complex shapes, it gets even harder (sometimes impossible) to combine different sizes in a way that doesn't leave gaps.

[OmniGraffle]: https://www.omnigroup.com/omnigraffle


{% separator "paintbrush.svg" %}


## Drawing an inner stroke with clipping

You can get an inner stroke by drawing a double-width centred stroke, then discarding everything outside the boundary of the shape -- or alternatively, only showing everything inside the shape.

We can achieve the latter with an SVG feature called *clipping*.

A clip defines an outline, and only the area inside the outline is visible.
For example, if I had [an illustration of the Earth] and I wanted to remove the background around it, I could add a circular clip, and only the planet would be shown:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_4_circular_clip.svg" %}
</figure>

Here's how the clipped image works:

```
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

We start by defining a `<clipPath>`, which contains a single shape -- the circle we want to remain visible.
Then we reference the clipPath in the `clip-path` attribute on our image, and the SVG renderer only shows the parts of the image that fall inside the circle.

If we put a more complex shape in our `<clipPath>`, we can use it to clip when we actually draw the shape -- and only the half of the stroke inside the shape will be shown.
Thus, we get an inner stroke:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_5_clip_inner_stroke.svg" %}
</figure>

And here's what the SVG looks like:

```
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
    stroke-width="10" stroke="red" fill="none"
clip-path="url(#insideHeartOnly)"/>
</svg>
```

The path can be arbitrarily complicated, but you'll always get the same inner stroke effect.

[an illustration of the Earth]: https://wellcomecollection.org/works/uhemygps


{% separator "paintbrush.svg" %}


## Drawing an outer stroke with clipping

We can use a similar approach to draw an outer stroke.
Draw a double-width centred stroke, and discard the half of the stroke inside the boundary of the shape -- or only include the half that's outside.

Unfortunately, as far as I know, there's no easy way to do this with clips.
You can't "invert" a clip -- that is, to show everything outside rather than inside.

One way you could do this is to draw a rectangle around the boundary of your entire drawing, and then create a zero-width "bridge" from the rectangle to your original clip -- this new clip would enclose everything *except* that original clip.
I've exaggerated the width of the bridge in the illustration, but hopefully you get the idea:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_6_clip_outer_stroke.svg" %}
</figure>

This works, but it's not ideal -- we need modify our shape to add the bridge, and depending on how our shape is defined, that may be non-trivial.

I think this might be possible using multiple shapes the [clip-rule attribute], but I wasn't able to come up with a working example.

Is there another way to achieve this effect?

[clip-rule attribute]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clip-rule


{% separator "paintbrush.svg" %}


## Drawing an outer stroke with masks

SVG has another feature called *masking*, which is a more powerful way to select parts of an image.
Rather than providing a simple "on/off", it allows us to control the opacity of the underlying image -- that is, how much of it shows through.

A *mask* is a black-and-white graphic.
When you overlay a mask on an image, anything under the black parts of the mask is completely hidden, and anything under the white parts is fully shown.
For example, we can remove the globe by putting a black circle in the middle of a white mask:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_7_mask_globe.svg" %}
</figure>

Here's how this SVG works:

```
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <mask id="globeOuterOnly">
      <rect x="0" y="0" width="100" height="100" fill="white"/>
      <circle cx="50" cy="50" r="45" fill="black"/>
    </mask>
  </defs>

  <image
    href="globe.jpg" height="100" width="100"
    mask="url(#globeOuterOnly)"/>
</svg>
```

We start by defining a `<mask>`, in which we draw the black and white shapes that make up the mask.
Then we reference it in the `mask` attribute of our image, and the SVG renderer only shows the parts of the image that are below a white part of the mask.

Masks allow more sophisticated effects than clips: as well as a simple black/white--off/on, we can use shades of grey to more precisely control the opacity of the image that shows through.
The darker the shade, the lower the opacity of the original image.

For example, I could cut out the globe, and then highlight a single part of it:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_8_mask_cutout.svg" %}
</figure>

Although we don't need any shades of grey to draw inner/outer strokes, it's a nice example of the power allowed by masks: we can compose multiple shapes for a more complex effect.
This particular mask has three shapes: a black rectangle, a grey circle, and a white outline of Africa.

By creating a mask with a white background and a black shape, we can discard the half of a double-width stroke that falls inside the image -- and thus, an outer stroke:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_9_mask_outer_stroke.svg" %}
</figure>

And here's some more SVG:

```
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Based on the heart from https://thenounproject.com/search/?q=heart&i=585522 -->
    <path id="heart" d="m 31,11.375 c -14.986319,0 -25,12.30467 -25,26 0,12.8493 7.296975,23.9547 16.21875,32.7188 8.921775,8.764 19.568704,15.2612 26.875,19.0312 a 2.0002,2.0002 0 0 0 1.8125,0 c 7.306296,-3.77 17.953225,-10.2672 26.875,-19.0312 C 86.703025,61.3297 94,50.2243 94,37.375 c 0,-13.69533 -10.013684,-26 -25,-26 -8.834204,0 -14.702885,4.50444 -19,10.59375 C 45.702885,15.87944 39.834204,11.375 31,11.375 z"/>

    <mask id="outsideHeartOnly">
      <rect x="0" y="0" width="100" height="100" fill="white"/>
      <use xlink:href="#heart" fill="black"/>
    </mask>
  </defs>

  <use
    xlink:href="#heart"
    stroke-width="10" stroke="blue" fill="none"
    mask="url(#outsideHeartOnly)"/>
</svg>
```

As with the inner stroke, you can adapt this to any shape by changing the path.


{% separator "paintbrush.svg" %}


## Putting it all together

Although I have the code to do inner and outer strokes, for the hearts app I ended up just using centred strokes and inner strokes.
If you put the inner stroke on top of a double-width centred stroke, you get the same effect, and that was slightly simpler to implement:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_10_overlay.svg" %}
</figure>

To create the interlocking hearts, I created some masks that cut out a part of each heart where it was crossed by the other.
Here's one of the two masks:

<figure style="width: 686px;">
{% inline_svg "_images/2021/strokes_11_cutouts.svg" %}
</figure>

Clips and masks are among the SVG features that I've brushed up against before, but never used properly.
Having a small, self-contained project in which I could experiment has really helped me understand how they work, and I'll be able to use them much more confidently in future.

I learnt a lot making my hearts app, and even more writing this blog post -- and I hope you found it useful too.
