"""
The picture tag is for images in posts.

It creates different sizes and formats of image, and returns the
HTML markup for the <picture> tag with the different formats.

Arguments:
    - filename: name of the original image
    - alt: alt text for the image
    - width: the largest size this image will be rendered at

"""

from pathlib import Path
from typing import Any

from jinja2 import pass_context
from jinja2.parser import Parser
from jinja2.runtime import Context
from PIL import Image

from mosaic.models import CardConfig
from mosaic.pictures import create_image_derivatives
from .jinja_extensions import KwargsExtensionBase


class PictureExtension(KwargsExtensionBase):
    tags = {"picture"}

    def parse(self, parser: Parser) -> str:
        return self._parse_kwargs(
            parser, tag_name="picture", render_method="render_picture"
        )

    @pass_context
    def render_picture(self, *args, **kwargs):
        return render_picture(*args, **kwargs)

def render_picture(
        context: Context,
        filename: str,
        width: str | None = None,
        height: str | None = None,
        images_subdir: str | None = None,
        link_to: str | None = None,
        caller: Any | None = None,
        **kwargs,
    ):
        src_dir = context["src_dir"]
        out_dir = context["out_dir"]

        # TODO: Allow passing integer values to the picture tag.
        if width is not None:
            width = int(width)
        if height is not None:
            height = int(height)

        # Work out the source path to the image under `src/images`.
        #
        #   - If a picture tag sets an `images_subdir`, use that
        #   - If the parent page has a date, look in the per-year folder
        #   - Otherwise, look in the `images` folder
        #
        images_dir = src_dir / "_images"

        if images_subdir is not None:
            lt_src_path = images_dir / images_subdir / filename
        else:
            page = context["page"]
            if hasattr(page, "date") and page.date:
                lt_src_path = images_dir / str(page.date.year) / filename
            else:
                lt_src_path = images_dir / filename

        if not lt_src_path.exists():
            raise FileNotFoundError(lt_src_path)

        # Check if there's a dark mode variant of this image, which
        # will have the same name but a .dark suffix.
        #
        # If it exists, check the two images have the same dimensions.
        dk_src_path = lt_src_path.with_suffix(".dark" + lt_src_path.suffix)
        if dk_src_path.exists():
            with Image.open(lt_src_path) as lt_im, Image.open(dk_src_path) as dk_im:
                if lt_im.size != dk_im.size:
                    raise ValueError(
                        "light/dark images have inconsistent dimensions: "
                        f"{lt_src_path} ({lt_im.size}) / {dk_src_path} ({dk_im.size})"
                    )
        else:
            dk_src_path = None

        # Work out how wide we're going to draw the image.
        target_width = get_target_width(
            lt_src_path, target_width=width, target_height=height
        )
        desired_widths = [pixel_density * target_width for pixel_density in (1, 2, 3)]

        lt_derivatives, default_image = create_image_derivatives(
            lt_src_path, src_dir, out_dir, desired_widths, target_width, is_screenshot="screenshot" in kwargs.get("class", "")
        )
        if dk_src_path is not None:
            dk_derivatives, _ = create_image_derivatives(
                dk_src_path, src_dir, out_dir, desired_widths, target_width, is_screenshot="screenshot" in kwargs.get("class", "")
            )
        else:
            dk_derivatives = {}

        # This creates a `sizes` attribute like
        #
        #     (max-width: 450px) 100vw, 450px
        #
        # which tells the browser an image is an exact width (450px) unless
        # the entire viewport is narrower than that, in which case it fills
        # the screen (100vw).
        #
        # This isn't perfect, e.g. it doesn't account for margins or wrapping,
        # but it's good enough and better than relying on screen density alone.
        sizes_attribute = f"(max-width: {target_width}px) 100vw, {target_width}px"

        # Render the <picture> tag.
        env = context.environment
        template = env.get_template("partials/picture.html")

        # Work out where to link to (if any)
        if link_to == "original":
            link_target = "/images/" + str(lt_src_path.relative_to(src_dir / "_images"))
        else:
            link_target = link_to

        return template.render(
            lt_derivatives=lt_derivatives,
            dk_derivatives=dk_derivatives,
            default_image=default_image,
            sizes_attribute=sizes_attribute,
            link_target=link_target,
            extra_attributes=kwargs,
        )

def get_target_width(
    src_path: Path, target_width: int | None, target_height: int | None
) -> int:
    """
    Work out how wide the image should be, based on the target
    dimensions and the image dimensions.
    """
    if target_width is None and target_height is None:
        raise TypeError(f"you forgot to supply a width/height for {src_path}")

    if target_width is not None and target_height is not None:
        raise TypeError(f"only supply one of width/height for {src_path}")

    with Image.open(src_path) as im:
        im_width, im_height = im.size

    if target_width is not None:
        if im_width < target_width:
            raise ValueError(
                f"image is too small: path={src_path}, width={im_width}, target_width={target_width}"
            )
        else:
            return target_width

    elif target_height is not None:
        if im_height < target_height:
            raise ValueError(
                f"image is too small: path={src_path}, height={im_height}, target_height={target_height}"
            )
        else:
            return round(im_width * target_height / im_height)

    assert False, "unreachable"
