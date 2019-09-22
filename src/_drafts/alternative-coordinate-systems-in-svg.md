---
layout: post
title: Drawing with triangular coordinates in SVG
summary:
category: Programming and code
---

If you've been paying close attention to my recent posts, you might have noticed that I've started to use [SVG images][svg] for some of my diagrams.
I like SVGs because they tend to be sharper than bitmap images, and I can generate them programatically (rather than with a GUI app).

[svg]: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics

One of the things I've been playing with is alternative coordinate systems -- in particular, drawing images that fit on a triangular grid.
This feels like it might have other applications, so in this post I'm going to walk through how it works.
It's helpful if you remember some trigonometry from school, but if not I'll explain it was we go along.



<script>
MathJax = {
  loader: {load: ['[tex]/ams']},
  tex: {
    inlineMath: [['$', '$']],
    displayMath: [['\\[', '\\]']],
    packages: {'[+]': ['ams']}
  },
  svg: {
    fontCache: 'global'
  }
};
</script>

<script
  type="text/javascript"
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>




## Choosing a coordinate system

A quick primer: a *coordinate system* is a way to represent points in 2D space -- for example, the corners of a shape.
We can define a shape by its coordinates, and use those to tell an SVG renderer what to draw.

For example, the coordinates in this SVG define a black square:

```xml
<!-- square.svg -->
<svg viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg">
  <polygon points="10,10 20,10 20,20 10,20" fill="black" />
</svg>
```

Here's what that image looks like (the grey dashed line marks the edge of the SVG):

<figure style="width: 350px;">
  <svg viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg">
    <polygon points="1,1 1,29 29,29 29,1" stroke="#ccc" fill="none" stroke-width="0.25" stroke-dasharray="0.25,0.25" />

    <polygon points="10,10 20,10 20,20 10,20" fill="black" />

    <circle cx="10" cy="10" r="0.75" fill="#d01c11" />
    <text x="9" y="9" fill="#d01c11" font-size="1.8px" text-anchor="end" font-family="serif">(10, 10)</text>

    <circle cx="20" cy="10" r="0.75" fill="#d01c11" />
    <text x="21" y="9" fill="#d01c11" font-size="1.8px" text-anchor="start" font-family="serif">(20, 10)</text>

    <circle cx="20" cy="20" r="0.75" fill="#d01c11" />
    <text x="21" y="22" fill="#d01c11" font-size="1.8px" text-anchor="start" font-family="serif">(20, 20)</text>

    <circle cx="10" cy="20" r="0.75" fill="#d01c11" />
    <text x="9" y="22" fill="#d01c11" font-size="1.8px" text-anchor="end" font-family="serif">(10, 20)</text>
  </svg>
</figure>

The coordinate system most people are familiar with is [Cartesian coordinates][cartesian], or $(x,y)$-coordinates.
There's a vertical and a horizontal axis, and the $(x,y)$-coordinates of a point are measured by how far you have to move along the axis to get to the point.

[cartesian]: https://en.wikipedia.org/wiki/Cartesian_coordinate_system

SVG flips this on its head (literally), because the $y$-axis moves down rather than up, but otherwise the principle is the same.
Here's what it looks like:

<figure style="width: 350px;">
  <img src="/images/2019/cartesian_coordinates.svg">
</figure>

This sort of coordinate system is great if you're drawing rectangular shapes, but for other types of diagram it's not so easy.
Let's suppose, for example, that we wanted to draw this hexagonal grid as an SVG:

<figure style="width: 450px;">
  <img src="/images/2019/hex_board.png">
</figure>

We could try to define it with Cartesian coordinates, and do a bunch of moderately fiddly trigonometry for each of the points.
But it's much easier to define if you're working on a triangular grid -- every point neatly snaps to one of the points on the grid.

Here's a set of triangular coordinates: we define $\langle 1, 0 \rangle$ to be a step of 1 unit to the right, and $\langle 0, 1 \rangle$ to be a step of 1 unit at a $60^\circ$ angle.
I'm using the $\langle \cdots \rangle$ brackets to distinguish between triangular and $(x,y)$-coordinates.

<figure style="width: 480px;">
  <img src="/images/2019/triangular_coordinates.svg">
</figure>

The choice of a $60^\circ$ angle means the grid divides into [equilateral triangles][equilateral] (equal sides, equal angles).
This is a convenient choice for lots of diagrams, but the process below will work for any choice of angle.

[equilateral]: https://en.wikipedia.org/wiki/Equilateral_triangle

Writing out the points of a regular hexagon in this coordinate system is much simpler than doing so in Cartesian coordinates.
Rather than mucking around with any trig, we get neat integer points:

<figure style="width: 350px;">
  <img src="/images/2019/hex_diagram.svg">
</figure>

So now we have a coordinate system that lets us define triangular shapes -- but we can't use it in an SVG image.
The SVG coordinate system is fixed -- we still need to do the translation from triangular to Cartesian coordinates.
Let's tackle that next.


## Translating between coordinate systems

We want a function that takes a point $\langle a, b \rangle$ in triangular coordinates and returns $(x,y)$ in Cartesian coordinates.
If we can work out what $\langle 1, 0 \rangle$ and $\langle 0, 1 \rangle$ in triangular coordinates become in Cartesian coordinates, that's enough -- we can then add those together to get the coordinates for $(a, b)$.

The first is simple: $\langle 1, 0 \rangle$ is the same in both triangular and Cartesian coordinates.

What about $\langle 0, 1 \rangle$?
Let's draw a diagram of this point:

<figure style="width: 200px;">
  <svg viewBox="0 0 40 45" xmlns="http://www.w3.org/2000/svg">
    <polygon points="5,5 25,5 25,39.641016151" stroke="#ccc" fill="none" stroke-width="0.5" stroke-dasharray="0.25,0.25" />

    <polygon points="25,5 22,5 22,8 25,8" stroke="#aaa" fill="none" stroke-width="0.25" />

    <path d="M 8 10.196152423
             A 6 6 0 0 0 11 5" stroke="#aaa" fill="none" stroke-width="0.25" />

    <line stroke-width="0.5"
          x1="5" y1="5"
          x2="25" y2="39.641016151" stroke="black" />

    <text x="15" y="3.5" font-size="4px" fill="#888" font-family="serif" font-style="italic" dominant-baseline="baseline">x</text>
    <text x="27" y="22.5" font-size="4px" fill="#888" font-family="serif" font-style="italic" dominant-baseline="baseline">y</text>

    <text x="11" y="10.5" font-size="4px" fill="#888" font-family="serif">60&#176;</text>

    <text x="10" y="27" font-size="4px" font-family="serif">1</text>

    <circle cx="25" cy="39.641016151" r="1.5" fill="#d01c11" />
    <text x="28" y="39.641016151" fill="#d01c11" font-size="4px" font-family="serif" dominant-baseline="middle">&#12296;1, 0&#12297;</text>
  </svg>
</figure>

This is a right-angled triangle where the longest side has length $1$, and the other two sides have lengths $x$ and $y$.
We can use trig identities to work out the value of $x$ and $y$.

If we remember [some trigonometric functions][trig], we get:

AAA BBB CCC ddd eee fff ggg hhh iii jjj kkk lll


[trig]: https://en.wikipedia.org/wiki/Trigonometric_functions#Right-angled_triangle_definitions

## Why not just use SVG transforms?

