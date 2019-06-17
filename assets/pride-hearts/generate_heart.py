#!/usr/bin/env python
# -*- encoding: utf-8

import pathlib

from PIL import Image, ImageDraw

from colors import RGBColor, random_colors_near
from heart_coords import get_heart_rows, scale, HEART_10, HEART_12


def create_heart(stripes, threshold=100, scale_factor=25):
    if len(stripes) in {1, 2, 3, 4, 6}:
        heart_defn = HEART_12

        dimensions = (12, 12)

        if len(stripes) == 1:
            row_colors = stripes * 12
        elif len(stripes) == 2:
            row_colors = [stripes[0]] * 6 + [stripes[1]] * 6
        elif len(stripes) == 3:
            row_colors = [stripes[0]] * 4 + [stripes[1]] * 4 + [stripes[2]] * 4
        elif len(stripes) == 4:
            row_colors = (
                [stripes[0]] * 3 + [stripes[1]] * 3 + [stripes[2]] * 3 +
                [stripes[3]] * 3
            )
        elif len(stripes) == 6:
            row_colors = (
                [stripes[0]] * 2 + [stripes[1]] * 2 + [stripes[2]] * 2 +
                [stripes[3]] * 2 + [stripes[4]] * 2 + [stripes[5]] * 2
            )

    elif len(stripes) == 5:
        heart_defn = HEART_10

        dimensions = (10, 10)

        row_colors = (
            [stripes[0]] * 2 + [stripes[1]] * 2 + [stripes[2]] * 2 +
            [stripes[3]] * 2 + [stripes[4]] * 2
        )

    else:
        raise ValueError(f"Unsupported stripe count: {stripes!r} ({len(stripes)})")

    scaled_dimensions = tuple(dim * scale_factor for dim in dimensions)

    im = Image.new("RGBA", size=scaled_dimensions)
    draw = ImageDraw.Draw(im)

    for row_coords, row_color_hex in zip(get_heart_rows(heart_defn), row_colors):
        row_color_seed = RGBColor.from_hex_string(row_color_hex)
        random_colors = random_colors_near(row_color_seed, threshold=threshold)
        for rect, color in zip(row_coords, random_colors):
            draw.polygon(
                scale(rect, factor=scale_factor),
                fill=(color.red, color.green, color.blue, 255)
            )

    return im


if __name__ == "__main__":
    out_dir = pathlib.Path("hearts")
    out_dir.mkdir(exist_ok=True)

    im = create_heart(stripes=["#d01c11"], threshold=30)
    im.save(out_dir / "red_heart.png")

    im = create_heart(stripes=["#d01c11", "#11d01c"], threshold=30)
    im.save(out_dir / "red_green_heart.png")

    im = create_heart(stripes=["#b57edc", "#efefef", "#4A8123"], threshold=20)
    im.save(out_dir / "genderqueer.png")

    im = create_heart(
        stripes=["#5bcefa", "#f5a9b8", "#ffffff", "#f5a9b8", "#5bcefa"], threshold=20
    )
    im.save(out_dir / "trans.png")

    im = create_heart(
        stripes=["#000000", "#a3a3a3", "#ffffff", "#810082"], threshold=20
    )
    im.save(out_dir / "asexual.png")

    im = create_heart(
        stripes=["#ff0080", "#ff0080", "#a349a4", "#0000ff", "#0000ff"], threshold=35
    )
    im.save(out_dir / "bisexual.png")

    im = create_heart(
        stripes=["#e70000", "#ff8c00", "#ffef00", "#00811f", "#0044ff", "#760089"], threshold=35
    )
    im.save(out_dir / "rainbow.png")

    im = create_heart(
        stripes=["#ff218e", "#fcd800", "#0194fc"], threshold=35
    )
    im.save(out_dir / "pansexual.png")

    im = create_heart(
        stripes=["#fff433", "#ffffff", "#9b59d0", "#000000"], threshold=35
    )
    im.save(out_dir / "nonbinary.png")
