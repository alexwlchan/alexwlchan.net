"""
Create the differnet variants of an image to use with the <picture> tag,
including different formats, sizes, and variants for light/dark mode.
"""

import collections
from fractions import Fraction
from io import BytesIO
from pathlib import Path
from typing import Any, Literal, TypeAlias, TypedDict

from chives.text import coloured
from PIL import Image, ImageCms


__all__ = ["get_picture_template_variables"]


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


# Map of MIME type to srcset strings, for example:
#
#     "image/jpeg": ["/images/example_1x.jpg 1x", "/images/example_2x.jpg 2x"],
#     "image/png":  ["/images/example_1x.png 1x", "/images/example_2x.png 2x"],
#
ImageDerivatives: TypeAlias = dict[MimeType, list[str]]


class PictureTemplateVariables(TypedDict):
    """
    Variables for the picture.html template.
    """

    # Light/dark image derivatives
    lt_derivatives: ImageDerivatives
    dk_derivatives: ImageDerivatives

    # Which image should be used in browsers that don't understand the
    # <picture> and <source> tags?
    default_image: str

    # What sizes attribute should be used in the <picture> tag?
    sizes_attribute: str

    # Where should this image link, if anywhere?
    link_target: str | None

    # Extra HTML attributes to add to the element.
    extra_attributes: dict[str, Any]


def get_picture_template_variables(
    src_dir: Path,
    src_path: Path,
    out_dir: Path,
    width: int | None = None,
    height: int | None = None,
    link_to: str | None = None,
    caller: Any | None = None,
    dst_prefix: str | Path | None = None,
    #
    # In the srcset and sizes attribute, should it be based on the width
    # of the output image or the pixel density?
    size_based_on: Literal["width", "density"] = "width",
    #
    # What's the max pixel density to support?
    max_pixel_density: int = 3,
    **kwargs: Any,
) -> PictureTemplateVariables:
    """
    Create the HTML to display an image.
    """
    if isinstance(dst_prefix, str):
        dst_prefix = Path(dst_prefix)

    # TODO: Allow passing integer values to the picture tag.
    if width is not None:
        target_width = int(width)
    else:
        target_width = None
    if height is not None:
        target_height = int(height)
    else:
        target_height = None

    lt_src_path = src_path
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

    # Check the source images have an sRGB colour profile.
    assert has_srgb_colour_profile(lt_src_path), f"non-sRGB profile in {lt_src_path}"
    assert dk_src_path is None or has_srgb_colour_profile(dk_src_path), (
        f"non-sRGB profile in {dk_src_path}"
    )

    # Work out how wide we're going to draw the image.
    target_width = choose_target_width(
        lt_src_path, target_width=target_width, target_height=target_height
    )

    desired_widths = [d * target_width for d in range(1, max_pixel_density + 1)]

    is_screenshot = "screenshot" in kwargs.get("class", "")

    derivative_args = {
        "src_dir": src_dir,
        "out_dir": out_dir,
        "desired_widths": desired_widths,
        "target_width": target_width,
        "is_screenshot": is_screenshot,
        "dst_prefix": dst_prefix,
        "size_based_on": size_based_on,
    }

    lt_derivatives, default_image = create_image_derivatives(
        lt_src_path, **derivative_args
    )
    if dk_src_path is not None:
        dk_derivatives, _ = create_image_derivatives(dk_src_path, **derivative_args)
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
    if size_based_on == "width":
        sizes_attribute = f"(max-width:{target_width}px)100vw,{target_width}px"
    else:
        sizes_attribute = ""

    # Work out where to link to (if any)
    if link_to == "original":
        link_target: str | None = f"/{lt_src_path.relative_to(src_dir)}"
    else:
        link_target = link_to

    # These two attributes allow the browser to completely determine
    # the space that will be taken up by this image before it actually
    # loads, so it won't have to rearrange the page later.  The fancy
    # term for this is "Cumulative Layout Shift".
    #
    # See https://web.dev/optimize-cls/
    aspect_ratio_style = get_aspect_ratio_style(lt_src_path)
    try:
        kwargs["style"] = f"{aspect_ratio_style}; {kwargs['style']}"
    except KeyError:
        kwargs["style"] = aspect_ratio_style
    kwargs["width"] = target_width

    return {
        "lt_derivatives": lt_derivatives,
        "dk_derivatives": dk_derivatives,
        "default_image": default_image,
        "sizes_attribute": sizes_attribute,
        "link_target": link_target,
        "extra_attributes": kwargs,
    }


def get_aspect_ratio_style(path: Path) -> str:
    """
    Return a CSS `aspect-ratio: X / Y` style for the image at this path.
    """
    with Image.open(path) as im:
        aspect_ratio = Fraction(im.width, im.height)

    return f"aspect-ratio: {str(aspect_ratio)}"


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
    target_width: int | None,
    is_screenshot: bool,
    dst_prefix: Path | None,
    size_based_on: Literal["width", "density"],
) -> tuple[dict[MimeType, list[str]], str]:
    """
    Create all the derivative images for an input image.

    Returns a dict (mime type) -> (srcset strings), and the URL of
    the image you should prefer as the default.
    """
    if dst_prefix is None:
        dst_prefix = src_path.relative_to(src_dir).with_suffix("")

    if src_path.suffix.lower() == ".jpg":
        original_format: ImageFormat = "jpg"
        default_mime_type: MimeType = "image/jpeg"
    elif src_path.suffix.lower() == ".png":
        original_format = "png"
        default_mime_type = "image/png"
    else:  # pragma: no cover
        raise ValueError(f"unrecognised image format: {src_path}")

    # Choose what format we should use for this image, in order of preference.
    # If it's a screenshot or a book review preview, just use the default
    # format; we don't need anything else.
    desired_formats: list[ImageFormat]
    if is_screenshot or dst_prefix.parts[0] == "b":
        desired_formats = [original_format]
    else:
        desired_formats = ["avif", "webp", original_format]

    assert target_width is not None

    created_images = create_image_sizes(
        src_path,
        out_dir,
        dst_prefix,
        desired_formats,
        desired_widths,
        target_width,
        size_based_on,
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
    size_based_on: Literal["width", "density"],
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
            if size_based_on == "density":
                assert out_width % target_width == 0
                out_srcset = (
                    f"/{out_path.relative_to(out_dir)} {out_width // target_width}x"
                )
            else:
                out_srcset = f"/{out_path.relative_to(out_dir)} {out_width}w"
            sources[out_mime_type].append(out_srcset)

    return dict(sources)


def has_srgb_colour_profile(path: Path) -> bool:
    """
    Return True if this image has an sRGB colour profile.

    I block using images with non-standard colour profiles because they
    render inconsistently in web browsers, and I'm not doing anything
    where I'd benefit from the expanded colour gamuts.
    """
    allowed_colour_profiles = [
        None,
        "sRGB",
        "sRGB built-in",
        "sRGB IEC61966-2.1",
        "Generic Gray Gamma 2.2 Profile",
        "Adobe RGB (1998)",
    ]

    with Image.open(path) as im:
        icc = im.info.get("icc_profile")

        if not icc:
            return True

        profile = ImageCms.getOpenProfile(BytesIO(icc))
        profile_name = ImageCms.getProfileDescription(profile).strip()

        if profile_name in allowed_colour_profiles:
            return True
        else:
            print(
                coloured(
                    f"unexpected colour profile on {path!r}: {profile_name!r}", "yellow"
                )
            )
            return False
