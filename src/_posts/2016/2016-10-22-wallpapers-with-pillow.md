---
layout: post
date: 2016-10-22 21:03:00 +00:00
title: Creating low contrast wallpapers with Pillow
summary: "Take a regular tiling of the plane, apply a random colouring, and voila: a unique wallpaper, courtesy of the Python Imaging Library."
tags:
  - python
  - python:pillow
  - drawing things
  - generative art
colors:
  index_light: "#98291d"
  index_dark:  "#ffd20b"
---

In my [last post](/2016/tiling-the-plane-with-pillow/), I explained how I'd been using Pillow to draw regular tilings of the plane.
What I was actually trying to do was get some new desktop wallpapers, and getting to use a new Python library was just a nice bonus.

A while back, the [Code Review Stack Exchange](http://codereview.stackexchange.com) got a fresh design that featured, among other things, a low-contrast background of coloured squares:

{%
  picture
  filename="code_review.png"
  width="240"
  alt="The name 'Code Review' in dark grey text, a grey magnifying glass, and a background of light-grey squares."
%}

I was quite keen on the effect, and wanted to use it as my desktop wallpaper, albeit in different colours.
I like using low contrast wallpapers, and this was a nice pattern to try to mimic.
My usual work is entirely text-based; this was a fun way to dip my toe into the world of graphics.
And a few hours of Python later, I could generate these patterns in arbitrary colours:

<table>
  <tr>
    <td style="padding: 5px;"><img src="/images/2016/specktre_demo_sq.png" alt="A grid of squares in varying shades of red."></td>
    <td style="padding: 5px;"><img src="/images/2016/specktre_demo_tr.png" alt="A pattern of triangles in varying shades of yellow."></td>
    <td style="padding: 5px;"><img src="/images/2016/specktre_demo_hex.png" alt="A pattern of hexagons in varying shades of blue."></td>
  </tr>
</table>

In this post, I'll explain how I went from having a tiling of the plane, to generating these wallpapers in arbitrary colours.

In the previous post, we had three generators, which generated the coordinates for individual polygons in a tiling of the plane.
We want to give each polygon its own colour, so we need another generator to create random colours.

One way to represent a colour in Pillow is to use the RGB colour space, and then a colour is a 3-tuple of integers between 0 and 255.
For convenience, I've defined a [namedtuple][namedtuple] for storing colour data.
So a generator of random colours from anywhere in the RGB space looks like this:

{% code lang="python" names="0:collections 1:namedtuple 2:random 3:randint 4:Color 6:random_colors" %}
from collections import namedtuple
from random import randint

Color = namedtuple('Color', ['red', 'green', 'blue'])

def random_colors():
    while True:
        yield Color(randint(0, 255), randint(0, 255), randint(0, 255))
{% endcode %}

[namedtuple]: https://docs.python.org/3.5/library/collections.html?highlight=namedtuple#collections.namedtuple

Unlike the coordinate generators, this generator is infinite: it will continue generating random colours until the system runs out of entropy (randomness).
That's useful, because we don't know in advance how many colours we might need for a given image — we just have to be careful not to try to store the entire output of this generator, or we'll quickly run out of memory.

But really, we'd like to constrain the colours to a small sample of the RGB space — that's the "low-contrast" part.
For my wallpapers, I typically want a few shades of the same colour, so I like to pick two colours, and have every colour fall somewhere in between.
If you imagine the two colours as being points in 3-dimensional space, let's draw a line between them and just pick colours along that line.
Here's what that looks like:

{% code lang="python" names="0:random_colors 1:color1 2:color2 3:d_red 8:d_green 13:d_blue 18:proportion" %}
def random_colors(color1, color2):
    """
    Generate random colors between ``color1`` and ``color2``.
    Both arguments should be instances of ``Color``.
    """
    # Get the difference along each axis
    d_red   = color1.red - color2.red
    d_green = color1.green - color2.green
    d_blue  = color1.blue - color2.blue

    while True:
        # What proportion of the line to move along
        proportion = random.uniform(0, 1)

        yield Color(
            red=color1.red - int(d_red * proportion),
            green=color1.green - int(d_green * proportion),
            blue=color1.blue - int(d_blue * proportion)
        )
{% endcode %}

So now we have a generator of colours, and a generator of shapes, we need to put them both together on a Pillow canvas.
Python provides the [`zip` function][zip] for combining two iterables, and we can use that to great effect:

{% code lang="python" names="0:shapes 3:colors" %}
shapes = generate_shapes(500, 500, side_length=25)
colors = random_colors(color1, color2)

for shape, color in zip(shapes, colors):
    ...
{% endcode %}

(Here `generate_shapes` is one of the generators we defined in the last post.)

[zip]: https://docs.python.org/3.5/library/functions.html?highlight=zip#zip

Within the body of this for loop, we have a set of coordinates for the shape, and a Color tuple for the fill colour.
The `zip` function runs until one of the iterables is exhausted, so this will run for precisely as many shapes as we need to tile the plane.

Finally, we need to actually use Pillow to draw these shapes!
We can use the `ImageDraw` module, this time passing a `fill` argument to fill in the shapes we're drawing:

{% code lang="python" names="0:PIL 1:Image 2:ImageDraw 3:im 8:shapes 10:colors 14:shape 15:color" %}
from PIL import Image, ImageDraw

# Create a blank 500x500 pixel image
im = Image.new(mode='RGB', size=(500, 500))

# Generate the shapes and colors, and draw them on the canvas
shapes = generate_shapes(500, 500)
colors = random_colors(color1, color2)

for shape, color in zip(shapes, colors):
    ImageDraw.Draw(im).polygon(shape, fill=color)

# Save the image to disk
im.save('wallpaper.png')
{% endcode %}

And voila, we now have a nice, low-contrast wallpaper made from tiling the plane.
And because the colours are generated at random, each wallpaper is unique — not a useful feature per se, but it gives me warm fuzzy feelings.

I've had wallpapers from this tool on all of my devices for a couple of weeks now, and I'll be sticking with it.
This is more effort than anybody should spend on a new desktop background, but I've enjoyed it.
It's been fun to play with a new Python library and to do some graphics work.
Although I'm unlikely to make another wallpaper tool, I have ideas for using my Pillow knowledge elsewhere.

If you'd like to use this yourself, all the code [is in a GitHub repository][github].
I've also made a [web app][webapp] that lets you make these wallpapers within your browser.

[github]: https://github.com/alexwlchan/specktre
[webapp]: https://alexwlchan.net/experiments/specktre/