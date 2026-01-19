"""
Tests for mosaic.header_images.
"""

from mosaic.header_images import draw_header_image


def test_draw_header_image() -> None:
    """
    The draw_header_image function completes and returns an appropriate image.
    """
    im = draw_header_image("#008800")
    assert im.width == 2500
    assert im.height == 250
