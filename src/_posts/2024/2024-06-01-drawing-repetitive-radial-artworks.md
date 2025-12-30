---
layout: post
date: 2024-06-01 10:20:51 +0000
title: Drawing repetitive radial artworks
summary: |
  Using polar coordinates to draw leaf- and flower-like patterns that repeat in circles around a point.
tags:
  - generative art
  - drawing things
is_featured: true
---
I was waiting for a meeting to start the other day, and I was idly doodling in my notebook.
I'd just had a text from a friend about an upcoming trip to Ireland, and she'd sent me the four-leafed clover emoji (🍀), so I was sketching some petal-like shapes.
These are a few of my doodles:

{%
  picture
  filename="doodles.jpg"
  width="750"
  alt="A couple of sheets of paper with various hand-drawn doodles showing simple geometric shapes and circles."
%}

I was trying to draw various patterns that could be repeated around a central point.
This is easy to imagine, but quite fiddly to do by hand.
Fortunately, computers.

After my meeting, I cracked out Python and started experimenting.
I wrote some scripts to generate SVG images -- I'm bashing lines and curves together, and I've done [similar stuff before](/2022/graph-generative-art/).

<style type="x-text/scss">
  @use "components/checkerboard";
  @use "components/hero_grid";

  .hero_grid {
    --grid-light-color: #fcdbd9;
    --grid-dark-color:  #d01c11;
  }
</style>

<style>
  .coordinates {
    display: grid;
    grid-gap: calc(2 * var(--grid-gap));
    grid-template-columns: 200px auto;
    padding-left:  1em;
    padding-right: 1em;
  }

  @media screen and (max-width: 500px) {
    .coordinates {
      padding: 0;
    }
  }

  @media screen and (max-width: 400px) {
    .coordinates {
      grid-template-columns: auto;
    }
  }

  .coordinates figcaption {
    margin-top:    auto;
    margin-bottom: auto;
  }

  .hero_grid svg:nth-child(1) path,
  .hero_grid svg:nth-child(1) line,
  .hero_grid svg:nth-child(7) path,
  .hero_grid svg:nth-child(7) line {
    stroke-width: 3px;
  }
</style>

Here's a sample of some of the art I was able to create:

<div class="hero_grid grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/angled_barely_poiny.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_4.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/round_petals_lots.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_radius_3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/hooks_8.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_few_pointy.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/hooks_4.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_lots_of_outie.svg"
    class="dark_aware"
  %}
</div>

Read on to find out how I made it, and see more examples.

## Polar coordinates

Normally when you draw shapes in SVG, you work in [Cartesian coordinates](https://en.wikipedia.org/wiki/Cartesian_coordinate_system), where points are determined by their horizontal (*x*) and vertical (*y*) distance from an origin.

Note that in SVG, the origin is the top left-hand corner of your diagram: as *x* increases, you move from right-to-left, and as *y* increases, you move from bottom-to-top.
This can be confusing at first, because we're used to *y* increasing in the opposite direction.

<figure class="coordinates">
  {%
    inline_svg
    filename="cartesian_coordinates.svg"
    class="dark_aware"
    style="width: 200px;"
  %}
  <figcaption>
    Two points in the Cartesian coordinate system used by SVG.
    In green, the point with horizontal distance 4 and vertical distance 2 or (4,&nbsp;2).
    In blue, the point (1,&nbsp;3).
  </figcaption>
</figure>

But for drawing patterns that repeat in a circle around a point, it's easier to use [polar coordinates](https://en.wikipedia.org/wiki/Polar_coordinate_system), an alternative coordinate system where points are determined by:

* their distance from a central point (the *radius*)
* their angle from a specified direction (the *angle*)

I chose to work in a polar coordinate system where angles are measured clockwise from the upwards vertical axis, like so:

<figure class="coordinates">
  {%
    inline_svg
    filename="polar_coordinates.svg"
    class="dark_aware"
    style="width: 200px;"
  %}
  <figcaption>
    Two points in a polar coordinate system.
    In green, the point with radius&nbsp;9 and angular coordinate 40&nbsp;degrees or (9,&nbsp;40°).
    In blue, the point (6,&nbsp;120°).
  </figcaption>
</figure>

This choice of coordinates gives you a straightforward conversion between polar and Cartesian:

{% code lang="python" names="0:math 1:polar_to_cartesian 2:origin_x 3:origin_y 4:radius 5:angle" %}
import math


def polar_to_cartesian(origin_x, origin_y, radius, angle):
    return {
        "x": origin_x + radius * math.cos(angle),
        "y": origin_y + radius * math.sin(angle),
    }
{% endcode %}

This helper function allows me to define my shapes with polar coordinates, then convert to Cartesian when I want to actually draw them in the SVG.

## The sketches

First I drew "spokes" that emanate from the centre of the diagram.
I picked a random number, then draw that many spokes which are equally-spaced around the centre:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/spokes_4.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/spokes_lots.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/spokes_7.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/spokes_some.svg"
    class="dark_aware"
  %}
</div>

I added a random offset angle, to rotate all the spokes slightly -- this was to avoid creating a series of diagrams that all had the same vertical upward spoke at 0°.
Notice how, for example, the four spokes in the first diagram aren't perfectly horizontal or vertical.

---

Next I wanted to connect the spokes, to create something vaguely resembling flower petals.
Initially I connected their ends with straight lines, creating sets of equal-sized triangles:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/triangles_straightish.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/triangles_4.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/triangles_circleish.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/triangles_6.svg"
    class="dark_aware"
  %}
</div>

That first one reminded me of looking down at a spiral staircase.
I went and manually added some colours to create the illusion of steps, and then I kept playing with more varieties:

<script>
    function animateStaircases() {
        document.querySelectorAll('#staircases svg').forEach(function(svg) {
            const fillValues =
                Array.from(svg.querySelectorAll('path'))
                    .map(path => path.getAttribute('fill'));
            svg.querySelectorAll('path').forEach(function(path) {
                const index = fillValues.indexOf(path.getAttribute('fill'));
                const animationElement = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
                animationElement.setAttribute('attributeName', 'fill');
                animationElement.setAttribute('dur', '5s');
                animationElement.setAttribute('repeatCount', 'indefinite');

                const newValues =
                  index === 0
                    ? fillValues.join('; ')
                    : index === fillValues.length - 1
                    ? (
                        fillValues[fillValues.length - 1] + ';' +
                        fillValues.slice(0, index - 1).join('; ')
                    )
                    : (
                        fillValues.slice(index, fillValues.length).join('; ') + ';' +
                        fillValues.slice(0, index).join('; ')
                    );

                animationElement.setAttribute('values', newValues);
                path.appendChild(animationElement);
            });
        });
    }
</script>

<div class="grid_4up checkerboard" id="staircases">
  {%
    inline_svg
    filename="petals/staircase1.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/staircase2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/staircase3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/staircase4.svg"
    class="dark_aware"
  %}
</div>

These colours are static and hard-coded.
I also played with adding animation, to create a basic colour spinner -- there are a few rough edges and it's a bit jerky, but if you're interested, <a onclick="javascript:animateStaircases()" href="#staircases">you can see</a> what the animation looks like.

---

Returning to the line art, I wanted to replace those straight lines with something a bit more visually interesting.

I started with spiky "petals".
I allowed my script to choose randomly: would the spikes bend inward or outward, and by how much.
The pictures I got back remind me of stars and flowers:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/angled_very_pointy.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_barely_poiny.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_somewhat_innie.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_five_point.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_square.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_lots_of_outie.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_slightly_pointy.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/angled_few_pointy.svg"
    class="dark_aware"
  %}
</div>

But the thing I really wanted was round petals -- where each spoke would continue outwards, follow a circular arc, and come back to join the next spoke along.
This involved a bit of trigonometry to work out the angles, and my first few attempts didn't work -- but I think they have a certain beauty all the same:

<div class="grid_4up">
  {%
    inline_svg
    filename="petals/bad_petals1.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/bad_petals4.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/bad_petals2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/bad_petals3.svg"
    class="dark_aware"
  %}
</div>

But eventually I got it all figured out, and I was able to reproduce my original idea: flower "petals" with circular ends.
(And despite generating over 60 examples, I never got one with four parts.
Whatever your medium, a four-leafed clover is a tricksy and elusive thing.)

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/round_petals_3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/round_petals_many.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/round_petals8.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/round_petals_lots.svg"
    class="dark_aware"
  %}
</div>

And once I'd worked out the angles required to make a single curve work, I was able to stack them so there could be multiple arcs along the edge of each segment, like so:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/multi_petals_2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/multi_petals_8.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/multi_petals_3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/multi_petals_5.svg"
    class="dark_aware"
  %}
</div>

I like the ones with fewer segments, so you can really see the extra arcs.
The eight-segment one reminds me of a citrus fruit.

---

It was at this point that I noticed that all my diagrams looked quite… symmetrical.
I'd pick a random starting value, and then repeat that value throughout the picture.
What if I allowed even more randomness?

First I tried varying the radius of different segments.
In my first version of this code, I had a bug where I didn't join the extra-wide segments properly, leading to a rather fun "hook" effect:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/hooks_1.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/hooks_2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/hooks_8.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/hooks_4.svg"
    class="dark_aware"
  %}
</div>

After I fixed the bugs, I was able to get petals with different radii:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/random_radius_1.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_radius_2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_radius_3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_radius_4.svg"
    class="dark_aware"
  %}
</div>

Then play with the angles:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/random_angles_1.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_angles_2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_angles_3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/random_angles_4.svg"
    class="dark_aware"
  %}
</div>

It took me a couple of tries to work out how to partition 360° in a way that isn't very lopsided -- I ended up picking a random float in [0,&nbsp;1] for each segment, then scaling those values up so their total was 360.

---

Here's a final set of doodles, which are all "mistakes" where the code didn't do what I was expecting, but made something pretty anyway:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="petals/remainder_1.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_2.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_3.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_4.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_5.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_6.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_7.svg"
    class="dark_aware"
  %}
  {%
    inline_svg
    filename="petals/remainder_8.svg"
    class="dark_aware"
  %}
</div>

There are more things I could try, like adding colour and moving the centre, but this is all I had time for.
That's okay.
I was only drawing to have fun and because I wanted to make some pretty pictures, and I did both of those.
I like how far I was able to get from a single idea: "what if I repeated a pattern in a circle around a central point".
