#!/usr/bin/env python3

import colorsys
import hashlib
import random

from PIL import Image, ImageDraw  # pip install pillow==11.1.0


def pick_color(title):
    h = hashlib.md5(title.encode("utf8")).hexdigest()
    seed = int(h, 16)
    r = random.Random()
    r.seed(seed)

    hue = r.randint(0, 360) / 360

    r, g, b = colorsys.hls_to_rgb(hue, 0.25, 1.0)

    return int(r * 255), int(g * 255), int(b * 255)


if __name__ == "__main__":
    width = 672
    height = 1004

    title = "The Kudos of Monte Cristo"
    author = "Ann Thology"

    color = pick_color(title)

    im = Image.new("RGB", size=(width, height), color=color)
    d = ImageDraw.Draw(im)

    d.text(
        (width / 2, height / 2), title, fill=(255, 255, 255), anchor="mm", font_size=80
    )
    d.text(
        (width / 2, height / 2 + height / 13),
        author,
        fill=(255, 255, 255),
        anchor="mm",
        font_size=80,
    )

    im.save(f"{title}.png")
