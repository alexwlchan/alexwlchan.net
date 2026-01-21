"""
Create the mosaic-like header images which are a collection of squares
based on the tint colour.
"""

from collections.abc import Iterator
import random
from typing import cast, Literal, TypeAlias, TYPE_CHECKING

from PIL import Image, ImageDraw

from .colormath import (
    LabColor,
    RGBColor,
    RGB_to_Lab,
    Lab_to_RGB,
    delta_e_cie2000,
)

if TYPE_CHECKING:
    import PIL


__all__ = ["draw_header_image"]


# An x-y Cartesian coordinate
Coordinate = tuple[int, int]

# Coordinates which define the four corners of a square
Square: TypeAlias = tuple[Coordinate, Coordinate, Coordinate, Coordinate]


def draw_header_image(tint_colour: str) -> "PIL.Image.Image":
    """
    Create a header image.
    """
    im = Image.new(mode="RGB", size=(2500, 250))
    draw = ImageDraw.Draw(im)

    squares = generate_squares(im.width, im.height, side_length=50)
    colours = generate_colours_like(tint_colour)

    for sq, col in zip(squares, colours):
        draw.polygon(sq, fill=col)

    return im


def generate_unit_squares(image_width: int, image_height: int) -> Iterator[Square]:
    """
    Generate coordinates for a tiling of unit squares.
    """
    for x in range(image_width):
        for y in range(image_height):
            yield (x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)


def generate_squares(
    image_width: int, image_height: int, *, side_length: int = 1
) -> Iterator[Square]:
    """
    Generate coordinates for a tiling of squares.
    """
    assert image_width % side_length == 0
    assert image_height % side_length == 0

    scaled_width = int(image_width / side_length) + 2
    scaled_height = int(image_height / side_length) + 2
    for coords in generate_unit_squares(scaled_width, scaled_height):
        yield cast(
            Square, tuple((x * side_length, y * side_length) for (x, y) in coords)
        )


# An RGB colour whose components are in the range [0, 255].
ColourRGB_255: TypeAlias = tuple[int, int, int]


def generate_colours_like(hex_colour: str) -> Iterator[ColourRGB_255]:
    """
    Generate an infinite sequence of colours varying only in lightness.

    Returns a sequence of RGB colours, where each component is in the
    range [0, 255].
    """
    # Seed from the hex integer value. This ensures the random lightness
    # is consistent across builds and devices.
    seed = int(hex_colour.lstrip("#"), 16)
    rand = random.Random(seed)

    # Convert to CIELAB.
    rgb = RGBColor.new_from_rgb_hex(hex_colour)
    lab = RGB_to_Lab(rgb)

    # Find the bounds for random values of L*
    min_l: float = get_lightness_for_delta(lab, "darker", 6.0)
    max_l: float = get_lightness_for_delta(lab, "lighter", 6.0)
    l_range: float = max_l - min_l

    # Generate infinite colours in this range
    while True:
        new_l = min_l + (rand.random() * l_range)
        new_lab = LabColor(new_l, lab.lab_a, lab.lab_b)

        # Discard colours which don't map cleanly from CIELAB to sRGB.
        round_trip_lab = RGB_to_Lab(Lab_to_RGB(new_lab))
        if delta_e_cie2000(new_lab, round_trip_lab) > 1.0:
            continue

        rgb = Lab_to_RGB(new_lab)
        yield (round(rgb.rgb_r * 255), round(rgb.rgb_g * 255), round(rgb.rgb_b * 255))


def get_lightness_for_delta(
    original_lab: LabColor,
    direction: Literal["lighter", "darker"],
    target_delta: float,
) -> float:
    """
    Find the lightness of a CIELAB colour that gets the target CIELAB ΔE* 2000
    perceptual distance from the original colour, while preserving the
    original chromacity.
    """
    l_orig = original_lab.lab_l

    # Define the search range for L*
    low_l = l_orig if direction == "lighter" else 0.0
    high_l = 100.0 if direction == "lighter" else l_orig

    # Run a binary search on L*
    best_l: float = l_orig

    for _ in range(15):
        mid_l = (low_l + high_l) / 2.0
        candidate_lab = LabColor(mid_l, original_lab.lab_a, original_lab.lab_b)

        # Calculate the perceptual difference
        candidate_delta = delta_e_cie2000(original_lab, candidate_lab)

        if candidate_delta < target_delta:
            if direction == "lighter":
                low_l = mid_l
            else:
                high_l = mid_l
        else:
            if direction == "lighter":
                high_l = mid_l
            else:
                low_l = mid_l
        best_l = mid_l

    return best_l
