"""
Create the mosaic-like header images which are a collection of squares
based on the tint colour.
"""

from collections.abc import Iterator
from typing import cast, TypeAlias, TYPE_CHECKING

from PIL import Image, ImageDraw

from .tint_colours import generate_colours_like

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
