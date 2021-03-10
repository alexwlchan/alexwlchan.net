---
layout: post
title: Drawing inner/outer strokes in SVG
summary:
tags: svg
---

Over the last year or so, I've been trying to use SVG for more images.
A lot of the images I make are simple diagrams that work well as SVGs, and having images that look sharp at any size and get stored as text is a nice bonus.
I write most of my SVGs by hand, rather than using an app like Illustrator or Inkscape.
Although it's more work, it forces me to really understand how SVG works.

At the weekend, I made [a little app](/2021/03/rainbow-hearts/) that creates SVG images of interlocking hearts.
It was partly for fun, partly to play with some SVG features that I haven't used before: [clipping and masking](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Clipping_and_masking).

As part of the app, I came up with some code to draw inner and outer strokes using SVG.
This seems like something I might use again, and it helped me understand both features, so in this post I'm going to write up my notes on how I did this.



## What are inner and outer strokes?

The [*stroke*](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke) is the outline of a shape.

Normally, the stroke is centered on the boundary of the shape; that is, half of the stroke is inside the shape, and half of it is outside.
This means the visible width of the shape is actually the width of the shape *plus* the width of the stroke.
(You get half the stroke's width on both sides of the shape -- thus, an extra stroke width.)

In some graphics programs, you can choose to draw an *inner stroke* (which puts the entire stroke inside the shape) or an *outer stroke* (which puts the entire stroke outside the shape):

<img src="/images/2021/strokes.png" style="width: 686px;">

Although the square is the same size in all three cases, notice how the stroke alignment changes the size of the final image.

They have been several proposals to add stroke alignment to the SVG spec, so you could use `stroke-alignment="inner"` to modify a shape, but at time of writing, none of them have been accepted.
This [Stack Overflow thread](https://stackoverflow.com/q/7241393/1558022) links to several of the proposals, and also gave me some ideas for how I'd implement it myself.



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



## Drawing an inside stroke using clipping

You can get the same effect as an inside stroke by drawing a double-width centred stroke, and discarding the half of the stroke outside the boundary of the shape -- or alternatively, only including the half that's inside the shape.

We can achieve this effect with an SVG feature called *clipping*.

A clip defines an outline, and only the area inside the outline is visible.
For example, if I had a picture of Mars and I wanted to remove the space around it, I could add a circular clip, and only the planet would be shown:

<img src="/images/2021/mars_clip.png" style="width: 686px;">

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