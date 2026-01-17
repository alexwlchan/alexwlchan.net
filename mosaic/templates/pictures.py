"""
Creates a <picture> tag for images in blog posts.

This is more than a simple <img> tag; it also handles creating
multiple formats and resolutions, to minimise the amount of data
transfer for images in posts.

This includes:

    * Creating copies at different widths from the original, which are
      used with the `srcset` attribute to send copies appropriate for
      different screen resolutions.

    * Creating copies in different formats, including WebP, which have
      better compression and can further reduce data transfer in browsers
      with appropriate support.

    * Creating the HTML markup with the <picture> and <source> tags which
      allows browsers to select an appropriate image.

See:
https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset
https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types

== Example ==

This is a minimal example:

    {%
      picture
      filename="IMG_5744.jpg"
      alt="A black steam engine with a boxy shape."
      width="622"
    %}

It includes the following mandatory parameters:

    * `filename` is the name of the oriignal image.  This should be in
      the same per-year directory as the post.
    * `alt` is the alt text for the image, which must be supplied on
      all posts (which is checked by the linter plugin).
    * `width` or `height`, which is used to pick the sizes for the
      different resolutions.  This is a rough guide.

It will look for the image in `/images/[year]/[filename]`, so if this
was a post from 2022, it will look in `/images/2022/IMG_5744.jpg`.

Other Parameters
----------------
    * `link_to="original"` -- if added, the final <picture> tag will be
      wrapped in an <a> that links to the full-sized image.  Useful for
      gallery-type posts.

    * `link_to="https://example.com/some/page"` -- causes the <a> to link
      to somewhere other than the full-sized image.

    * `parent="/images"` -- looks for an image in somewhere other than
      the per-year directory.

Any other attribute (e.g. `style`, `class`) will be passed directly to
the  underlying <img> tag, which allows you to apply styles or behaviours
not covered by this plugin.

== How it works ==

The code in this file will create the different variants of each image,
based on:

    * dimensions, e.g. if the image is going to be shown at 300px wide,
      it might resize to 300px, 600px and 900px wide versions, to be
      shown on screens with 1x, 2x, 3px pixel density, respectively
    * light/dark mode -- if I have an image "cat.jpg" and a second file
      "cat.dark.jpg", then the latter is used for dark mode

Then it passes all of those variants into my `picture.html` component,
which actually renders the <picture> tag.

"""

import collections
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from PIL import Image


from jinja2 import pass_context
from jinja2.runtime import Context


from .jinja_extensions import KwargsExtensionBase


ImageFormat = Literal["avif", "webp", "jpg", "png"]

MimeType = Literal["image/avif", "image/jpeg", "image/png", "image/webp"]

FORMAT_TO_FILE_EXTENSION: dict[ImageFormat, str] = {
    "avif": ".avif",
    "webp": ".webp",
    "jpg": ".jpg",
    "png": ".png",
}

FORMAT_TO_MIME_TYPE: dict[ImageFormat, MimeType] = {
    "avif": "image/avif",
    "webp": "image/webp",
    "jpg": "image/jpeg",
    "png": "image/png",
}


class PictureExtension(KwargsExtensionBase):
    """
    Allow me to use the {% picture %} tag to render images with Jekyll.
    """

    tags = {"picture"}

    @pass_context
    def render_html(self, *args: Any, **kwargs: dict[str, Any]) -> str:
        """
        Render the picture tag.
        """
        return render_picture(*args, **kwargs)  # type: ignore


def render_picture(
    context: Context,
    filename: str,
    width: str | None = None,
    height: str | None = None,
    parent: str | None = None,
    link_to: str | None = None,
    caller: Any | None = None,
    **kwargs: Any,
) -> str:
    """
    Create the HTML to display an image.
    """
    src_dir = context["src_dir"]
    out_dir = context["out_dir"]

    # TODO: Allow passing integer values to the picture tag.
    if width is not None:
        target_width = int(width)
    else:
        target_width = None
    if height is not None:
        target_height = int(height)
    else:
        target_height = None

    # Work out the source path to the image under `src/images`.
    #
    #   - If a picture tag sets an `parent`, use that
    #   - If the parent page has a date, look in the per-year folder
    #   - Otherwise, look in the `images` folder
    #
    images_dir = src_dir / "_images"

    # TODO: Tidy up some of the `parent` handling logic?
    if parent is not None:
        lt_src_path = src_dir / str(parent).replace("/images", "_images") / filename
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
            if lt_im.size != dk_im.size:  # pragma: no cover
                raise ValueError(
                    "light/dark images have inconsistent dimensions: "
                    f"{lt_src_path} ({lt_im.size}) / {dk_src_path} ({dk_im.size})"
                )
    else:
        dk_src_path = None

    # Work out how wide we're going to draw the image.
    target_width = choose_target_width(
        lt_src_path, target_width=target_width, target_height=target_height
    )
    desired_widths = [pixel_density * target_width for pixel_density in (1, 2, 3)]

    lt_derivatives, default_image = create_image_derivatives(
        lt_src_path,
        src_dir,
        out_dir,
        desired_widths,
        target_width,
        is_screenshot="screenshot" in kwargs.get("class", ""),
    )
    if dk_src_path is not None:
        dk_derivatives, _ = create_image_derivatives(
            dk_src_path,
            src_dir,
            out_dir,
            desired_widths,
            target_width,
            is_screenshot="screenshot" in kwargs.get("class", ""),
        )
    else:
        dk_derivatives = {}

    # I have a CSS rule that adds a white background behind any
    # images shown in dark mode, so e.g. diagrams in transparent PNGs
    # will appear properly.
    #
    # We don't need to this this if there's a dark-mode variant of
    # the image.
    if dk_derivatives:
        kwargs["class"] = f"{kwargs.get('class', '')} dark_aware".strip()

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

    # Work out where to link to (if any)
    if link_to == "original":
        link_target: str | None = "/images/" + str(
            lt_src_path.relative_to(src_dir / "_images")
        )
    else:
        link_target = link_to

    # These two attributes allow the browser to completely determine
    # the space that will be taken up by this image before it actually
    # loads, so it won't have to rearrange the page later.  The fancy
    # term for this is "Cumulative Layout Shift".
    #
    # See https://web.dev/optimize-cls/
    with Image.open(lt_src_path) as im:
        aspect_ratio = Fraction(im.width, im.height)

    if aspect_ratio.is_integer():
        aspect_ratio_style = f"aspect-ratio: {aspect_ratio.numerator}"
    else:
        aspect_ratio_style = "aspect-ratio: " + "/".join(
            str(s) for s in aspect_ratio.as_integer_ratio()
        )

    try:
        kwargs["style"] = f"{aspect_ratio_style}; {kwargs['style']}"
    except KeyError:
        kwargs["style"] = aspect_ratio_style
    kwargs["width"] = target_width

    # Render the <picture> tag.
    env = context.environment
    template = env.get_template("partials/picture.html")

    html: str = template.render(
        lt_derivatives=lt_derivatives,
        dk_derivatives=dk_derivatives,
        default_image=default_image,
        sizes_attribute=sizes_attribute,
        link_target=link_target,
        extra_attributes=kwargs,
    )

    # Remove an empty attribute which tells html-proofer to ignore it.
    # TODO: Remove all instances of this attribute.
    html = html.replace('data-proofer-ignore="None"', "data-proofer-ignore")

    return html


def choose_target_width(
    src_path: Path, target_width: int | None, target_height: int | None
) -> int:
    """
    Choose how wide an image should be displayed.
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
                f"image is too small: "
                f"path={src_path}, width={im_width}, target_width={target_width}"
            )
        else:
            return target_width

    elif target_height is not None:
        if im_height < target_height:
            raise ValueError(
                f"image is too small: "
                f"path={src_path}, height={im_height}, target_height={target_height}"
            )
        else:
            return round(im_width * target_height / im_height)

    assert False, "unreachable"  # pragma: no cover


def create_image_derivatives(
    src_path: Path,
    src_dir: Path,
    out_dir: Path,
    desired_widths: list[int],
    target_width: int | None = None,
    is_screenshot: bool = False,
) -> tuple[dict[MimeType, list[str]], str]:
    """
    Create all the derivative images for an input image.

    Returns a dict (mime type) -> (srcset strings), and the URL of
    the image you should prefer as the default.
    """
    out_path = Path("images") / src_path.relative_to(src_dir / "_images")

    # Choose what format we should use for this image, in order of preference.
    if is_screenshot and src_path.suffix.lower() == ".jpg":
        # TODO: I'm excluding screenshots from WebP and AVIF because
        # they looked bad with VIPS, but they might look better in Pillow.
        desired_formats: list[ImageFormat] = ["jpg"]
        default_mime_type: MimeType = "image/jpeg"
    elif is_screenshot and src_path.suffix.lower() == ".png":
        desired_formats = ["png"]
        default_mime_type = "image/png"
    elif src_path.suffix.lower() == ".jpg":
        desired_formats = ["avif", "webp", "jpg"]
        default_mime_type = "image/jpeg"
    elif src_path.suffix.lower() == ".png":
        desired_formats = ["avif", "webp", "png"]
        default_mime_type = "image/png"
    else:  # pragma: no cover
        raise ValueError(f"unrecognised image format: {src_path}")

    assert target_width is not None

    dst_prefix = out_path.with_suffix("")

    created_images = create_image_sizes(
        src_path,
        out_dir,
        dst_prefix,
        desired_formats,
        desired_widths,
        target_width,
    )

    default_image = created_images[default_mime_type][0].split()[0]
    return created_images, default_image


def create_image_sizes(
    src_path: Path,
    out_dir: Path,
    dst_prefix: Path,
    desired_formats: list[ImageFormat],
    desired_widths: list[int],
    target_width: int,
) -> dict[MimeType, list[str]]:
    """
    Create all the different sizes of an image.

    Returns a map (mime type) -> (srcset values).

    For example:

        {
          "image/avif": "/im/example_100.avif 100w, /im/example_50.avif 50w,",
          "image/webp": "/im/example_100.webp 100w, /im/example_50.webp 50w",
          "image/jpeg": "/im/example_100.jpg 100w,  /im/example_50.jpg 50w"
        }

    """
    sources: dict[MimeType, list[str]] = collections.defaultdict(list)

    for out_width in desired_widths:
        for out_format in desired_formats:
            # I already have lots of images cut with the _1x, _2x, _3x names,
            # so I retain those when picking names to avoid breaking links or
            # losing Google juice, then switch to _500w, _640w, and so on
            # for larger sizes.
            #
            # This is also used downstream to choose the default image --
            # the 1x image is the default.
            if out_width % target_width == 0:
                suffix = f"{out_width // target_width}x"
            else:  # pragma: no cover
                suffix = "{out_width}w"

            ext = FORMAT_TO_FILE_EXTENSION[out_format]

            out_path = (
                (out_dir / dst_prefix)
                .with_stem(f"{dst_prefix.stem + dst_prefix.suffix}_{suffix}")
                .with_suffix(ext)
            )

            # Assume that if the image already exists, it's correct.
            if not out_path.exists():
                with Image.open(src_path) as im:
                    if out_width > im.width:
                        continue

                    out_height = round(im.height * out_width / im.width)
                    resized = im.resize((out_width, out_height))
                    out_path.parent.mkdir(exist_ok=True, parents=True)
                    resized.save(out_path)

            # Construct the srcset entry for this image, for example
            # /images/example.jpg 100w
            out_mime_type = FORMAT_TO_MIME_TYPE[out_format]
            out_srcset = f"/{out_path.relative_to(out_dir)} {out_width}w"
            sources[out_mime_type].append(out_srcset)

    return dict(sources)
