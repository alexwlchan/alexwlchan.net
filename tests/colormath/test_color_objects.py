"""
Various tests for color objects.
"""

import pytest

from mosaic.colormath.color_objects import RGBColor


@pytest.mark.parametrize("hex", ["#7bc832", "7bc832"])
def test_set_from_rgb_hex(hex: str) -> None:
    """
    Parse an RGBColor from a hex string.
    """
    actual = RGBColor.new_from_rgb_hex(hex)
    expected = RGBColor(0.482353, 0.784314, 0.196078)

    assert abs(actual.rgb_r - expected.rgb_r) <= 1e-5
    assert abs(actual.rgb_g - expected.rgb_g) <= 1e-5
    assert abs(actual.rgb_b - expected.rgb_b) <= 1e-5


@pytest.mark.parametrize("invalid_hex", ["", "#", "123", "1234567"])
def test_set_from_rgb_hex_invalid(invalid_hex: str) -> None:
    """
    Calling new_from_rgb_hex with an invalid hex string throws a ValueError.
    """
    with pytest.raises(ValueError):
        RGBColor.new_from_rgb_hex(invalid_hex)
