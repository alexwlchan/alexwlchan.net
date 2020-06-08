---
layout: post
date: 2020-03-08 10:13:19 +0000
title: Creating striped flag wallpapers with Pillow
category: Python
tags: python images
---

<style>
  img {
    max-height: 250px;
    display: inline-block;
  }

  figure img {
    margin-left:  0.5em;
    margin-right: 0.5em;
  }

  figure {
    text-align: center;
  }
</style>

One of the builtin wallpapers that ships with iOS is a black wallpaper with slanted rainbow stripes, based on the [old rainbow Apple logo](https://commons.wikimedia.org/wiki/File:Apple_Computer_Logo_rainbow.svg).

<figure>
  <img src="/images/2020/rainbow_apple_wallpaper.jpg" class="wallpaper" alt="A black wallpaper with six coloured diagonal stripes. From top to bottom: green, yellow, orange, red, purple, blue.">
  <img src="/images/2020/rainbow_apple_logo.svg" alt="The rainbow Apple logo.">
</figure>

This sort of simple, geometric design is exactly the type of thing you can create in code, not an image editor.
I've used Pillow, the Python imaging library, to do this sort of thing in the past -- first [tiling the plane](/2016/10/tiling-the-plane-with-pillow/), then adding colour to [create low contrast wallpapers](/2016/10/wallpapers-with-pillow/).

This design is simpler and involves less geometry: I measured the dimensions of the stripes from a JPEG, then used the ImageDraw class in Pillow to create the stripes on the background.
My metrics are based on the dimensions of an iPhone X-sized phone, but you can adapt the idea to any size of phone.

I'm not going to walk through the code in detail, but you can read it below.

You can choose the background colour and the colours of the different stripes.
It always draws the stripes are roughly the same height and position on the screen, and you can double or triple a stripe colour if you want extra thickness.

{% details %}
  <summary>create_stripey_wallpapers.py</summary>
```python
from PIL import Image, ImageDraw


def create_wallpaper(stripes, background_color="#000000"):
    """
    Create a ``PIL.Image`` instance with a striped wallpaper.

    :param stripes: A list of colours to draw as stripes.  Stripes are
        drawn from stop to bottom.
    :param background_color: The background colour of the wallpaper,
        default black.

    """
    # The dimensions of an iPhone X wallpaper are 1440 x 2560.
    im = Image.new("RGB", size=(1440, 2560), color=background_color)

    draw = ImageDraw.Draw(im)

    # When measuring the stripes on a JPEG of the iPhone X wallpaper:
    #
    #   - Each stripe was 110 pixels high
    #   - The midpoint of the stripes (between orange/red) on the left-hand
    #     side was 1754 pixels down
    #   - The midpoint of the stripes (between orange/red) on the left-hand
    #     side was 1202 pixels down
    #
    stripe_height = 110
    left_hand_midpoint = 1754
    right_hand_midpoint = 1202

    total_stripe_height = stripe_height * len(stripes)
    left_hand_top = 1754 - (total_stripe_height / 2)
    right_hand_top = 1202 - (total_stripe_height / 2)

    # Each stripe is a parallelogram.
    #
    # The points start in the top left-hand corner, and work clockwise
    # around the shape.
    #
    #         +
    #        /|
    #       / |
    #      /  |
    #     +   +
    #     |  /
    #     | /
    #     |/
    #     +
    #
    for i, color in enumerate(stripes):
        draw.polygon(
            [
                (0,    left_hand_top  + stripe_height * i),
                (1440, right_hand_top + stripe_height * i),
                (1440, right_hand_top + stripe_height * (i + 1)),
                (0,    left_hand_top  + stripe_height * (i + 1)),
            ],
            fill=color
        )

    return im


if __name__ == '__main__':
    for name, stripes in [
        ("mystery_1", ["#F996B9", "#FFFFFF", "#CA28E3", "#333333", "#5861CD"]),
        ("mystery_2", ["#D90012", "#D90012", "#0033A0", "#0033A0", "#F2A802", "#F2A802"]),
        ("mystery_3", ["#5BBD60", "#BAD897", "#ffffff", "#BABABA", "#333333"]),
        ("mystery_4", ["#FCD827", "#0423D2", "#0423D2", "#0423D2", "#FCD827"])
    ]:
        im = create_wallpaper(stripes=stripes)
        im.save(f"wallpaper_{name}.jpg")
```
{% enddetails %}

I've used it to create four mystery wallpapers, based on different flags with horizontal stripes:

<figure>
  <img src="/images/2020/wallpaper_mystery_1.jpg" class="wallpaper" alt="A black wallpaper with pink, white, hot pink, black and purple stripes.">
  <img src="/images/2020/wallpaper_mystery_2.jpg" class="wallpaper" alt="A black wallpaper with red, blue and gold stripes.">
  <img src="/images/2020/wallpaper_mystery_3.jpg" class="wallpaper" alt="A black wallpaper with dark green, light green, white, grey and black stripes.">
  <img src="/images/2020/wallpaper_mystery_4.jpg" class="wallpaper" alt="A black wallpaper with yellow, blue, yellow stripes. The blue stripe is three times the width of the yellow.">
</figure>

There are no prizes, but I'll be suitably impressed if anybody can work out what these four wallpapers are.
Tell me your answers [on Twitter](https://twitter.com/alexwlchan).

In the meantime, feel free to use this code to create your wallpapers, and please send me pictures of your homescreen if you do!
