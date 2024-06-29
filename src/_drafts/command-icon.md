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

We can imagine this symbol as being made up of multiple "hooks", rotated around a central point.
Each hook is made up of two parts: a straight line and a circular arc.
Here's a single hook:

{%
  inline_svg
  filename="command_hook.svg"
  style="width: 400px;"
%}

Imagine taking four copies of that hook, and rotating them around then joining them together -- that would create the looped square in the previous illustrations.

If we can work out how to draw one of these hooks for an arbitrary size and loop count, we can take that hook and rotate it as many times as we need for the full shape.





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

<script id="MathJax-script" async src="/static/2019/tex-mml-chtml.js"></script>





## Tackling the trigonometry

*This next section features a walkthrough of the trigonometry involved in drawing these hook shapes. This is the bit I find most interesting and omitting it would feel like saying "draw the rest of the owl", but if it's not your cup of tea, you can skip to the pretty pictures.*

There are three variables we can change:

*   How many sides/loops are there in the shape?
*   How long are the straight edges?
*   How big are the circular loops?

We need to define the path for these hooks in terms of these three variables.

**Let's start by working out how to draw the straight line.**
We know the length of the straight edge (which I'll denote $L$) and the number of sides.
Let's assume we also know the centre of rotation, which I'll mark with a blue dot.
We need to work out the coordinates of start and end points, also marked with blue dots.

We can draw an [isoceles triangle](https://en.wikipedia.org/wiki/Isosceles_triangle) with the centre of rotation at the intersection of the two legs, and the straight line as the base:

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

Because we'll have one of these triangles for each side in the shape, we can work out the angle $\theta$:

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
\psi = 360^\circ\Biggl(1 - \frac{1}{\text{number of sides}}\Biggr)
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
