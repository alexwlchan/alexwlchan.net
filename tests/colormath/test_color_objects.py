"""
Various tests for color objects.
"""

import numpy as np
import pytest

from mosaic.colormath.color_objects import RGBColor


@pytest.mark.parametrize("hex", ["#7bc832", "7bc832"])
def test_set_from_rgb_hex(hex: str) -> None:
    """
    Parse an RGBColor from a hex string.
    """
    actual = RGBColor.new_from_rgb_hex(hex)
    expected = RGBColor(0.482353, 0.784314, 0.196078)
    np.testing.assert_allclose(
        actual.get_value_tuple(),
        expected.get_value_tuple(),
        rtol=1e-5,
        atol=1e-5,
    )


@pytest.mark.parametrize("invalid_hex", ["", "#", "123", "1234567"])
def test_set_from_rgb_hex_invalid(invalid_hex: str) -> None:
    """
    Calling new_from_rgb_hex with an invalid hex string throws a ValueError.
    """
    with pytest.raises(ValueError):
        RGBColor.new_from_rgb_hex(invalid_hex)
