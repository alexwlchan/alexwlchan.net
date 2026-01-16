---
layout: post
date: 2022-08-10 22:10:42 +00:00
title: Drawing a circular arc in an SVG
summary: A Python function to help me draw circular arcs, as part of an upcoming project.
tags:
  - svg
  - drawing things
---

For an upcoming project, I need to draw some circular arcs in an SVG.
This feels like it should be easy -- it's one of the simplest curves -- but I have no idea what I'm doing.
I've never actually written an SVG curve from scratch; just modified a curve somebody else had written until it looked right.

This is the sort of thing I want:

<figure style="max-width: 600px;">
  {%
    inline_svg
    filename="circle_diagram.svg"
    alt="An illustration of a circular arc. There's a grey dashed circle, with a vertical line from the centre denoting zero degrees. Going clockwise, there's a blue angle labelled 'start', then a green angle labelled 'sweep'. Along the dashed circle is a thick black arc that follows the sweep angle."
  %}
</figure>

I want to be able to pick the centre and radius of the circle, the start and sweep angles.
I've chosen that vertical is 0&deg;, and I imagine drawing the arc in a clockwise direction.

I'm not interested in extending an existing path, or creating new lines beyond the arc -- I really just want a single arc.
I got it working, after lots of time spent in the MDN docs [for the `<path>` element][mdn].
It feels like something that might be useful elsewhere, so I've pulled it out as a standalone piece.

I wrote a small Python helper function:

{% download filename="create_circular_arc_paths.py" %}

This is a case where source code as plain text feels really limiting.
Both this snippet and the bigger project have a bunch of geometry code, and it'd be really useful to be able to insert small diagrams in the comments to explain what I'm doing.
Words are okay, but they're no substitute for pictures.

[mdn]: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#curve_commands
