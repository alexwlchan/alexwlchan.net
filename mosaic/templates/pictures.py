"""
Beginning of tools to deal with pictures.
"""

from pathlib import Path

from PIL import Image


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
