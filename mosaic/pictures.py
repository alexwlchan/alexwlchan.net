import collections
from collections.abc import Iterator
from pathlib import Path

from PIL import Image


def create_image_derivatives(
    src_path: Path,
    src_dir: Path,
    out_dir: Path,
    desired_widths: list[int],
    target_width: int | None = None,
    out_path: Path | None = None,
    is_screenshot: bool = False,
) -> tuple[dict[str, list[str]], str]:
    """
    Create all the derivative images for an input image.

    Returns a dict (mime type) -> (srcset strings), and the URL of
    the image you should prefer as the default.
    """
    if out_path is None:
        out_path = Path("images") / src_path.relative_to(src_dir / "_images")

    # Choose what format we should use for this image, in order of preference.
    if is_screenshot:
        # TODO: I'm excluding screenshots from WebP and AVIF because
        # they looked bad with VIPS, but they might look better in Pillow.
        desired_formats = [
            ("image/png", "png"),
        ]
        default_mime_type = "image/png"
    elif src_path.suffix.lower() == ".jpg":
        desired_formats = [
            ("image/avif", "avif"),
            ("image/webp", "webp"),
            ("image/jpeg", "jpg"),
        ]
        default_mime_type = "image/jpeg"
    elif src_path.suffix.lower() == ".png":
        desired_formats = [
            ("image/avif", "avif"),
            ("image/webp", "webp"),
            ("image/png", "png"),
        ]
        default_mime_type = "image/png"
    else:
        raise ValueError(f"unrecognised image format: {src_path}")

    # Work out what images we want to create.
    #
    # This is keyed by target width, and the values are a list of MIME types
    # and paths to write at that width.
    images_to_create: dict[int, list[tuple[str, Path]]] = collections.defaultdict(list)

    for w in desired_widths:
        for mime_type, ext in desired_formats:
            # The suffix is:
            #  - _1x, _2x, _3x if the width is an exact multiple
            #  - _840w, _260w otherwise
            #
            if target_width is not None and w % target_width == 0:
                suffix = f"{w // target_width}x"
            else:
                suffix = f"{w}w"

            name = out_path.with_stem(f"{out_path.stem}_{suffix}").with_suffix(
                f".{ext}"
            )
            images_to_create[w].append((mime_type, out_dir / name))

    # The result is a map (mime type) -> (srcset strings)
    result: dict[str, list[str]] = collections.OrderedDict(
        [(mime_type, []) for mime_type, _ in desired_formats]
    )

    # Actually create the images.
    #
    # There are lots of images, so we try to avoid creating images
    # unnecessarily. In particular, if we see an image with the correct
    # output filename, we assume it's correct without inspecting it.
    #
    # (Maybe that should be a post-build test?)
    for width, images in images_to_create.items():
        # Only open and resize the image once for each width we want
        # to create.
        if not all(p.exists() for _, p in images):
            with Image.open(src_path) as im:
                if width > im.width:
                    continue

                resized_im = im.resize((w, round(im.height * w / im.width)))

                for _, p in images:
                    p.parent.mkdir(exist_ok=True, parents=True)
                    resized_im.save(p)

        for mime_type, p in images:
            result[mime_type].append(f"/{p.relative_to(out_dir)} {width}w")

    default_image = result[default_mime_type][0].split()[0]

    return result, default_image


def generate_unit_squares(
    width: int, height: int
) -> Iterator[tuple[int, int, int, int]]:
    """
    Generate coordinates for a tiling of unit squares.
    """
    for x in range(width):
        for y in range(height):
            yield [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def generate_squares(width: int, height: int, sq_size: int = 1):
    """
    Generate coordinates for a tiling of squares.
    """
    assert width % sq_size == 0
    assert height % sq_size == 0

    scaled_width = int(width / sq_size) + 2
    scaled_height = int(height / sq_size) + 2

    for coords in generate_unit_squares(scaled_width, scaled_height):
        yield [(x * sq_size, y * sq_size) for (x, y) in coords]
