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



---
---
---
---
---
---



## Why do I want inner and outer strokes?

When I made my initial heart graphic in [OmniGraffle](https://www.omnigroup.com/omnigraffle), I used inner and outer strokes to create a striped effect.
By combining inner and outer strokes on the same shape, you can create the impression of a striped stroke:

<img src="/images/2021/stroked_hearts.png" style="width: 686px;">

By adding more strokes of varying width, you can create more complex stripes.

This tends to look better than nesting different sizes of the same shape.
Using inner/outer strokes gives a consistent, even line around the whole shape, whereas combining multiple sizes gives a messier result.
Notice how the blue stripe is narrower at the bottom of the heart than at the top, and the bottom of the red heart is curved rather than pointed:

<img src="/images/2021/uneven_stripes.png" style="width: 686px;">

I wanted to replicate this effect in SVG so that I could construct shapes with striped strokes.



## Drawing an inner stroke using clipping

You can get the same effect as an inside stroke by drawing a double-width centred stroke, and discarding the half of the stroke outside the boundary of the shape -- or alternatively, only including the half that's inside the shape.

We can achieve this effect with an SVG feature called *clipping*.

A clip defines an outline, and only the area inside the outline is visible.
For example, if I had a picture of Earth and I wanted to remove the space around it, I could add a circular clip, and only the planet would be shown:

<img src="/images/2021/planet_clip.png" style="width: 686px;">

<!-- https://mars.nasa.gov/resources/6453/valles-marineris-hemisphere-enhanced/ -->

Here's what the corresponding SVG looks like:

```xml
SVG GOES HERE
```

But a clip isn't restricted to simple geometric shapes -- a clip can follow an arbitrary path, including along the path of the shape we want to outline.
This gives us a way to draw inside strokes:

<img src="/images/2021/inner_stroke_clip.png" style="width: 686px;">

And here's what the corresponding SVG looks like:

```xml
SVG GOES HERE
```

By changing the `<path>`, you can change the shape -- and in turn it changes the clip that helps to draw the inner stroke.

  https://wellcomecollection.org/works/a36zvzxj/images?id=mspae9x6



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
