"""
Create favicons based on tint colours.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    import PIL


def colourise_image(template: "PIL.Image.Image", tint_colour: str) -> "PIL.Image.Image":
    """
    Takes a greyscale image with an alpha channel and applies a tint colour.
    """
    # Create solid colour images for each of the RGB components of
    # the tint colour.
    rd = int(tint_colour[1:3], 16)
    gr = int(tint_colour[3:5], 16)
    bl = int(tint_colour[5:7], 16)

    solid_rd = Image.new("L", size=template.size, color=rd)
    solid_gr = Image.new("L", size=template.size, color=gr)
    solid_bl = Image.new("L", size=template.size, color=bl)

    # Use the original image's alpha channel as a mask
    _, _, _, alpha = template.convert("RGBA").split()

    # Create the final image: solid colour plus alpha
    colourised = Image.merge("RGBA", (solid_rd, solid_gr, solid_bl, alpha))
    return colourised


def create_favicon(favicon_dir: Path, tint_colour: str) -> None:
    """
    Create the favicon assets for a tint colour.
    """
    hex_string = tint_colour.strip("#")
    ico_path = favicon_dir / f"{hex_string}.ico"

    # The ICO favicon is the last to be created, so if it already exists,
    # we assume the whole process is complete.
    if ico_path.exists():
        return

    favicon_dir.mkdir(exist_ok=True, parents=True)

    # TODO(2026-01-21): Move the favicon templates out of `src` and into
    # the `templates` dir

    # 1. SVG variants
    for size in [16, 32]:
        svg_template_path = Path(f"templates/favicons/favicon-{size}x{size}.svg")
        svg_data = svg_template_path.read_text().replace("#000000", tint_colour)
        (favicon_dir / f"{hex_string}-{size}x{size}.svg").write_text(svg_data)

    # 2. PNG variants
    png_images = []
    for size in [16, 32]:
        template_path = Path(f"templates/favicons/favicon-{size}x{size}.png")
        with Image.open(template_path) as template:
            colourised = colourise_image(template, tint_colour)
        png_path = favicon_dir / f"{hex_string}-{size}x{size}.png"
        colourised.save(png_path, optimize=True)
        png_images.append(colourised)

    # 3. ICO file
    png_images[0].save(ico_path, append_images=png_images[1:])
