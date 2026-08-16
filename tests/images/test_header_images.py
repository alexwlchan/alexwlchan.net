"""
Tests for mosaic.images.header_images.
"""

from pathlib import Path

from PIL import Image

from mosaic.images import create_header_image


def test_draw_header_image(tmp_path: Path) -> None:
    """
    The draw_header_image function completes and returns an appropriate image.
    """
    path = create_header_image(headers_dir=tmp_path / "out/h", tint_colour="#008800")
    assert path.exists()
    assert path == tmp_path / "out/h/008800.png"

    with Image.open(path) as im:
        assert im.width == 2500
        assert im.height == 250
