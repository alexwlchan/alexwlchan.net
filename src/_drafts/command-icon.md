---
layout: post
title: Doodling with the Mac's command icon
summary:
tags:
  - generative-art
  - drawing-things
colors:
  css_light: "#014df4"
  css_dark:  "#67a7ff"
---
The command key (⌘) has been a ubiquitious part of the Mac for [over forty years][folklore].
It was originally chosen by legendary icon designer Susan Kare, who picked it from a symbol dictionary -- it was used in Sweden to highlight an interesting feature on a map.
It's an abstract and pleasant shape, and can still be seen today on road signs and keyboards alike.

[folklore]: https://www.folklore.org/Swedish_Campground.html

<figure>
  {%
    picture
    filename="Nähtävyys_liikennemerkki_20170523.jpg"
    alt="Here is some alt text"
    width="750"
  %}
  <figcaption>
    A place of interest sign somewhere in Finland (the first country to use this symbol to mark places of interest).
    Photographed by Santeri Viinamäki, from <a href="https://commons.wikimedia.org/wiki/File:N%C3%A4ht%C3%A4vyys_liikennemerkki_20170523.jpg">Wikimedia Commons</a>, used under CC BY-SA 4.0.
  </figcaption>
</figure>

I spend a lot of time doodling shapes that look like the command icon.
The original shape is already quite pleasant, and then I try variations like making the loops bigger or smaller, or changing the number of loops in the shape.
While I was bored and had a pen and paper, I've drawn dozens of little looped squares.

But part of the beauty of this symbol is the rotational symmetry, and that's hard to capture in a free-hand sketch – at least one of my loops or lines would look different to the others.
But computers are very good at drawing repetitive, symmetric shapes, so I wanted to see if I could draw the command icon and its variants in SVG.

I started with Susan Kare's original pixel icon from System 1.0, and I tried to recreate that as an SVG path.
I had to re-read the [MDN tutorial on SVG arcs](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs) several times, but I did eventually manage to write a `<path>` that reproduces the original icon as a smooth curve:

<figure class="two_columns">
  {%
    inline_svg
    filename="kare_command.svg"
  %}

  {%
    inline_svg
    filename="alex_command.svg"
  %}
</figure>

<style>
  figure.two_columns {
    max-width: 600px;
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: var(--grid-gap);
  }

  figure.two_columns svg {
    width: 100%;
  }
</style>

This was fairly simple, because I can match the coordinates in the pixel version to the curves I'm trying to draw.
The 4-way symmetry and right angles make the geometries quite simple.

What if I wanted to do something more complicated, like vary the number of loops or increase the distance between them?
That's harder to write by hand, so I wanted to do that programatically.
This meant doing some trionometry, and it took a while to get the details right.

## The idea

One way to imagine symbols like this is being made of multiple "looped hooks".

{%
  inline_svg
  filename="command_looped_hook.svg"
  style="width: 400px;"
%}

If you take a collection of these, rotate them around a central point, and join them together, you'd get the complete shape.

There are three variables we can change:

*   How many sides/loops are there in the shape?
*   How long are the straight edges?
*   How big are the circular loops?

Let's work out how to draw one of these hooks given these inputs.



<script>
MathJax = {
  loader: {load: ['[tex]/ams']},
  tex: {
    inlineMath: [['$', '$']],
    displayMath: [
      ['$$', '$$']
    ],
    packages: {'[+]': ['ams']}
  },
  svg: {
    fontCache: 'global'
  }
};
</script>

<!-- From https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js, retrieved 30 June 2024 -->
<script id="MathJax-script" async src="/static/2024/tex-chtml.js"></script>





## Tackling the trigonometry

*This next section features a walkthrough of the trigonometry involved in drawing these hook shapes. It's probably not 100% rigorous, but it's the bit I find most interesting and omitting it entirely would feel like saying ["and then draw the rest of the owl"](https://knowyourmeme.com/memes/how-to-draw-an-owl), but if it's not your cup of tea, you can skip to the pretty pictures.*

**Let's start by considering the straight line, up to the loop.**
This is the part I'm thinking about:

{%
  inline_svg
  filename="command_icons/straight_edge_focus.svg"
  style="width: 400px;"
%}

We know the length of this line (which I'll denote $L$) and the number of sides.
Let's assume we also know the centre of rotation, which I'll mark with a blue circles.
We need to work out the coordinates of the start and end points of this line, which I'll mark with blue dots.

{%
  inline_svg
  filename="straight_edge.svg"
  style="width: 400px;"
%}

The interesting variable here is $h$, because we can use it to define the start/end points of the line:

$$
\begin{align*}
\text{start} &= (\text{centre}_x - L/2, \text{centre}_y - h) \\[2pt]
\text{end} &= (\text{centre}_x + L/2, \text{centre}_y - h)
\end{align*}
$$

How can we work out the angle $\theta$?
Notice that in the final shape, these line segments form a regular polygon:

{%
  inline_svg
  filename="command_icons/regular_polygon.svg"
  style="width: 400px;"
%}

The angles around a point sum to $360^\circ$, and this angle will be the same for every side (by rotational symmetry), so we can calculate $\theta$:

$$
\theta = \frac{360^\circ}{\text{number of sides}}
$$

Using some right-angled triangle geometry, we can then work out the height $h$:

$$
h = \frac{L\tan(\theta/2)}{2}
$$

The SVG syntax for drawing this line is then

```
<path d="M {start_x} {start_y} L {end_x} {end_y}"/>
```

**Next, let's think about the curved loops.**
We know the number of sides and the radius of each loop (denoted $r$).
We need to work out where the circular arc starts and where it ends.
There are two unknowns here: the angle swept out by the loop (denoted $\psi$) and the length of the straight line segment before the circular arc starts (denoted $s$).

{%
  inline_svg
  filename="command_icons/loop.svg"
  style="width: 400px;"
%}

The two straight line segments are tangents to the circular arc -- they form a right angle with the radii marked in dashed lines.

How do we work out the angle $\psi$?



---
---
---
---



**Next let's draw the circular arc.**
We know the radius of the arc (which I'll denote $r$) and the start point (which is the end point of the straight line).
To draw this arc in SVG, we need to work out the end point.

{%
  inline_svg
  filename="circular_arc.svg"
  style="width: 400px;"
%}

We have one of these circular arcs for each side in the shape, and after we've changed directly through all of them, we should be facing the same direction we started.
That means the sum of the gaps in all the arcs sums to $360^\circ$, which allows us to calculate the angle $\psi$:

$$
\psi = 360^\circ\left(1 - \frac{1}{\text{number of sides}}\right)
$$

We can also work out the centre of the circle:

$$
\text{centre of circle} =
(\text{start of arc}_x, \; \text{start of arc}_y - r)
$$

We can then use trigonometry to work out the end of the arc:

$$
\text{end of circle} =
(\text{start of arc}_x + r \sin(\psi), \; \text{start of arc}_y - r + r \cos(\psi))
$$

The SVG syntax for drawing this circular arc is then

```
<path d="M {start_x} {start_y} A {r} {r} 0 1 0 {end_x} {end_y}"/>
```

The `0 1 0` are part of the [SVG arc syntax](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs).
The first `0` is `x-axis-rotation`, which we leave at the default.
Then we have to choose between the four possible arcs that connect the start/end points: in this case `large-arc-flag = 1` and `sweep-flag = 0` give us the arc we need.

**Finally, let's work out the centre of rotation.**
Everything is defined in relation to this point.
Intuitively we're going to put it in the middle of our SVG canvas, but how big should that canvas be?
This depends on how large our straight lines and circular arcs are going to be, because bigger shapes need more space.

So let's ask a different question: what's the furthest point on the shape from the centre of rotation?

I believe you can find this point by drawing a line from the centre of rotation to the centre of the circular arc, and then continuing until it intersects the arc:

{%
  inline_svg
  filename="furthest_point.svg"
  style="width: 400px;"
%}

What's the alternative?
Any other point on the arc is closer to the centre of rotation (using the [triangle inequality](https://en.wikipedia.org/wiki/Triangle_inequality)).
Any point on the line is closer to the centre of the rotation (the furthest points are at the ends, then the circular arc is further than that).

[Pythagoras' theorem](https://en.wikipedia.org/wiki/Pythagorean_theorem) gets us the distance to the center of the circle, and then we add on the radius.
This means the further point from the centre of rotation is:

$$
\text{max distance} = r + \sqrt{(L/2)^2 + (h+r)^2}
$$

Let's double that and add some padding, and use that as the width/height of our SVG canvas.
This should give us enough space to draw our shape.
