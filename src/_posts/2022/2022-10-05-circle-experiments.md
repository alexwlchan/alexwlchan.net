---
layout: post
date: 2022-10-05 22:35:11 +00:00
title: Some experiments with circle-based art
summary: Casually covering a canvas with coloured circles.
tags:
  - python:pillow
  - drawing things
  - generative art
colors:
  index_light: "#ae0000"
  index_dark:  "#ea0000"
---

<style>
  /*
    By default, this is a grid that's four columns wide, but on narrow screens
    (i.e. mobile), I shrink it to two columns so it remains readable.

    I think I might do a checkerboard pattern on the 4-wide layout, and I want
    to retain that on the 2-wide layout, so I need to swap the 3rd/4th in every row.

    e.g. if I have

        X1 .2 X3 .4
        .5 X6 .7 X8

    then on the mobile layout I want

        X1 .2
        .4 X3
        X6 .5
        .7 X8

    I swap the orders with `grid-column` properties, then the `grid-auto-flow`
    stops there being gaps in the grid.
  */
  .grid_4up {
    display: grid;
    grid-gap: var(--grid-gap);
    grid-template-columns: auto auto auto auto;
  }

  @media screen and (max-width: 500px) {
    .grid_4up {
      grid-template-columns: auto auto;
    }
  }
</style>

The header of this site is made of tiling squares in slightly varying shades of red.
It's meant to be subtle, but I think it still gives the site a unique look:

{%
  picture
  filename="header_image.png"
  width="750"
  alt="The site header, which is made of small tiling squares in slightly varying shades of red."
%}

I think of this as the "new" header, even though my [screenshot library] tells me I added it in 2016 (!), as does [the blog post] I wrote about how I make these images.

It has a lot of straight edges, and for a while I've been pondering alternatives.
A lot of my current designs have swapped right angles for rounded corners; I'm a heavy user of the [border-radius property].
Could I do something with circles instead of squares?

I made a few prototypes tonight, and for now the squares are staying -- but I thought I'd share my experiments.
These graphics don't work for me, but they might work for somebody else.

I started by refamiliarising myself with [Pillow], the Python library I use for doing simple graphics.
The API has changed since my post in 2016 -- I don't remember what I was using back then, but today I'm using Pillow&nbsp;9.2.0.

I started with a single red circle, to get the hang of [the new `ImageDraw` API][ImageDraw]:

{% code lang="python" names="0:PIL 1:Image 2:ImageDraw 3:im 7:draw" %}
from PIL import Image, ImageDraw

im = Image.new('RGB', size=(500, 500))
draw = ImageDraw.Draw(im)

draw.ellipse([(100, 100), (200, 200)], fill=(255, 0, 0))

im.save('red_circle.png')
{% endcode %}

Not especially exciting:

<img src="/images/2022/circle-experiments/red_circle_1x.png" srcset="/images/2022/circle-experiments/red_circle_1x.png 1x, /images/2022/circle-experiments/red_circle_2x.png 2x" alt="A red circle in the middle of a black background.">

I'm passing two arguments to the `ellipse()` method: an xy-bounding box, and a fill colour as an RGB tuple.
Because the bounding box is a square, the ellipse becomes a circle -- this took me a few moments to figure out, because the word "circle" doesn't appear anywhere in the ImageDraw docs.

I extended this code to draw circles in a grid, with a random shade of red in each circle:

{% code lang="python" names="0:random 1:PIL 2:Image 3:ImageDraw 4:im 8:draw 12:x 14:y" %}
import random
from PIL import Image, ImageDraw

im = Image.new('RGB', size=(500, 500))
draw = ImageDraw.Draw(im)

for x in range(-100, 600, 70):
    for y in range(-100, 600, 70):
        draw.ellipse(
            [(x, y), (x + 100, y + 100)],
            fill=(random.randint(128, 255), 0, 0)
        )

im.save('grid_of_circles.png')
{% endcode %}

The circles are drawn left-to-right, top-to-bottom.
In one prototype, I accidentally saved an image on every iteration of the xy loop, so you can see how it's created:

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/grid_of_partial_circles_1.png" alt="A black background with red circles stacked on top of it. There's one complete column of circles down the left-hand side, then three more circles at the top starting the first column.">
  <img src="/images/2022/circle-experiments/grid_of_partial_circles_2.png" alt="Now with two more columns filled in.">
  <img src="/images/2022/circle-experiments/grid_of_partial_circles_3.png" alt="Another two columns from the left are filled, more than halfway across.">
  <img src="/images/2022/circle-experiments/grid_of_partial_circles_4.png" alt="Almost all of the image is circles, with just a bit of empty space in the bottom right.">
</div>

Each circle is 100 points in diameter, so I spaced their centres 70 points apart -- this is as far as you can space them before some of the background starts poking through in the gaps.
(You can work out the exact value with Pythagoras' theorem, or just tweak the numbers until it looks right.)

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/grid_of_circles1.png" alt="An image made entirely of overlapping red circles, arranged in a grid. Each circle is overlapped by the circles below and to the right of it.">
  <img src="/images/2022/circle-experiments/grid_of_circles2.png" alt="The same shapes, but with different shades.">
  <img src="/images/2022/circle-experiments/grid_of_circles3.png" alt="The same shapes, but with different shades.">
  <img src="/images/2022/circle-experiments/grid_of_circles4.png" alt="The same shapes, but with different shades.">
</div>

The colour and the overlapping shape vaguely remind me of roof tiles -- and when I googled, I learnt that this shape is called "fish scale" roof tiles.
Yeah, I can see that.

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/fish_scales_1.png" alt="The same shapes as the overlapping red circles, but now in shades of blue.">
  <img src="/images/2022/circle-experiments/fish_scales_2.png" alt="The same shapes, but with different shades.">
  <img src="/images/2022/circle-experiments/fish_scales_3.png" alt="The same shapes, but with different shades.">
  <img src="/images/2022/circle-experiments/fish_scales_4.png" alt="The same shapes, but with different shades.">
</div>

But these shapes have a sense of direction -- because the circles always overlap on the same two sides, you can see the order in which they were laid down.

I tried shuffling the order in which the circles were drawn:

{% code lang="python" names="0:random 1:PIL 2:Image 3:ImageDraw 4:coords 7:x 9:y 14:im 18:draw 23:x 24:y" %}
import random
from PIL import Image, ImageDraw

coords = [
    (x, y)
    for x in range(-100, 600, 70)
    for y in range(-100, 600, 70)
]

random.shuffle(coords)

im = Image.new('RGB', size=(500, 500))
draw = ImageDraw.Draw(im)

for (x, y) in coords:
    draw.ellipse(
        [(x, y), (x + 100, y + 100)],
        fill=(random.randint(128, 255), 0, 0)
    )

im.save('grid_of_random_circles.png')
{% endcode %}

These images don't have a sense of direction, but they're a bit busy to my eye.
Although there's no pattern, I can feel my brain trying to find one in the various curves:

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/grid_of_random_circles_1.png" alt="A collection of red circles, still arranged in a grid, but now the overlap is in different directions. Some circles don't have anything on top of them, other circles have circles on top of them in any of the four directions.">
  <img src="/images/2022/circle-experiments/grid_of_random_circles_2.png" alt="The same shapes, but with different shades.">
  <img src="/images/2022/circle-experiments/grid_of_random_circles_3.png" alt="The same shapes, but with different shades.">
  <img src="/images/2022/circle-experiments/grid_of_random_circles_4.png" alt="The same shapes, but with different shades.">
</div>

I tried one more variation, with more randomness.
Rather than drawing equal-sized circles on a fixed grid, what if I drew circles of varying sizes at random points on the grid?

This is what I came up with:

{% code lang="python" names="0:random 1:PIL 2:Image 3:ImageDraw 4:im 8:draw 12:circle_count 16:x 19:y 22:r" %}
import random
from PIL import Image, ImageDraw

im = Image.new('RGB', size=(500, 500))
draw = ImageDraw.Draw(im)

circle_count = 0

while (0, 0, 0) in im.getdata():
    x = random.randint(-100, 600)
    y = random.randint(-100, 600)
    r = random.randint(50, 100)

    draw.ellipse(
        [(x, y), (x + r, y + r)],
        fill=(random.randint(128, 255), 0, 0)
    )

    circle_count += 1
    if circle_count >= 100:
        break

print(circle_count)

im.save('random_circles.png')
{% endcode %}

This draws circles of different radii, centred anywhere on the grid.
It will stop after there are no more black pixels (which means circles cover the entire image), or after 100 circles (I wasn't sure if it this would cover the image in a sensible amount of time).
The results are quite nice, and feel vaguely art-like:

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/random_circles1.png" alt="A collection of red circles of various sizes, placed randomly on a black background.">
  <img src="/images/2022/circle-experiments/random_circles2.png" alt="A collection of red circles of various sizes, placed randomly on a black background.">
  <img src="/images/2022/circle-experiments/random_circles3.png" alt="A collection of red circles of various sizes, placed randomly on a black background.">
  <img src="/images/2022/circle-experiments/random_circles4.png" alt="A collection of red circles of various sizes, placed randomly on a black background.">
</div>

I did a batch where I let it pick arbitrary bright colours, and that's fun too:

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/polka_dot5.png" alt="A collection of brightly coloured circles of various sizes, placed randomly on a black background.">
  <img src="/images/2022/circle-experiments/polka_dot6.png" alt="A different set of circles and colours.">
  <img src="/images/2022/circle-experiments/polka_dot7.png" alt="A different set of circles and colours.">
  <img src="/images/2022/circle-experiments/polka_dot8.png" alt="A different set of circles and colours.">
</div>

I decided to let it run to completion, and keep drawing circles until the whole image was covered.
It does eventually complete -- the exact number of circles varies, with an average of ~850.

<div class="grid_4up">
  <img src="/images/2022/circle-experiments/complete_circles1.png" alt="An image which is covered in red circles of varying sizes.">
  <img src="/images/2022/circle-experiments/complete_circles2.png" alt="A different set of circles.">
  <img src="/images/2022/circle-experiments/complete_circles3.png" alt="A different set of circles.">
  <img src="/images/2022/circle-experiments/complete_circles4.png" alt="A different set of circles.">
</div>

This still feels quite busy and loud, and not really what I want in the site header, so I decided to stop here.
I still like these images, they're just not right for this purpose.

One of the things I enjoy about Python and its drawing libraries is how fast I can go from idea to pretty picture.
I thought about this on the walk home from the station, and within ten minutes of walking through my door I had the final set of images.
It's a fun creative outlet -- and unlike other forms of computer-based art, my randomly generated graphics don't have any ethical quagmires.

[screenshot library]: /2022/screenshots/
[border-radius property]: https://developer.mozilla.org/en-US/docs/Web/CSS/border-radius
[the blog post]: /2016/wallpapers-with-pillow/
[Pillow]: https://python-pillow.org/
[ImageDraw]: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
[kirsten]: https://twitter.com/Kirsten3531/status/1575789943565131776
