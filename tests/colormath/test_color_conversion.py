"""
Tests for `colormath.color_conversions`.
"""

from typing import Any

from hypothesis import given, strategies as st
import numpy as np
import pytest

from mosaic.colormath import RGBColor, LabColor, RGB_to_Lab, Lab_to_RGB
from mosaic.colormath.color_conversions import (
    XYZ_to_RGB,
    RGB_to_XYZ,
    XYZ_to_Lab,
    Lab_to_XYZ,
)
from mosaic.colormath.color_objects import XYZColor


@pytest.mark.parametrize(
    "rgb, xyz, lab",
    [
        pytest.param(
            RGBColor(0, 0, 0), XYZColor(0, 0, 0), LabColor(0, 0, 0), id="black"
        ),
        pytest.param(
            RGBColor(1, 0, 0),
            XYZColor(0.412424, 0.212656, 0.019332),
            LabColor(53.23896, 80.090453, 67.201744),
            id="red",
        ),
        pytest.param(
            RGBColor(0, 1, 0),
            XYZColor(0.357579, 0.715158, 0.119193),
            LabColor(87.735002, -86.182949, 83.179536),
            id="green",
        ),
        pytest.param(
            RGBColor(0, 0, 1),
            XYZColor(0.180464, 0.0721856, 0.950444),
            LabColor(32.299375, 79.191396, -107.865464),
            id="blue",
        ),
    ],
)
@pytest.mark.parametrize(
    "direction",
    [
        "RGB_to_Lab",
        "RGB_to_XYZ",
        "XYZ_to_Lab",
        "Lab_to_RGB",
        "Lab_to_XYZ",
        "XYZ_to_RGB",
    ],
)
def test_colour_conversion(
    rgb: RGBColor, xyz: XYZColor, lab: LabColor, direction: str
) -> None:
    """
    Test the transfer from RGB to Lab and back.
    """
    c1: Any
    c2: Any

    if direction == "RGB_to_Lab":
        c1, c2 = RGB_to_Lab(rgb), lab
    elif direction == "RGB_to_XYZ":
        c1, c2 = RGB_to_XYZ(rgb), xyz
    elif direction == "XYZ_to_Lab":
        c1, c2 = XYZ_to_Lab(xyz), lab
    elif direction == "Lab_to_RGB":
        c1, c2 = Lab_to_RGB(lab), rgb
    elif direction == "Lab_to_XYZ":
        c1, c2 = Lab_to_XYZ(lab), xyz
    elif direction == "XYZ_to_RGB":
        c1, c2 = XYZ_to_RGB(xyz), rgb
    else:  # pragma: no cover
        assert 0, "unreachable!"

    np.testing.assert_allclose(
        c1.get_value_tuple(),
        c2.get_value_tuple(),
        rtol=1e-5,
        atol=1e-5,
    )


@given(
    st.floats(min_value=0.0, max_value=1.0),
    st.floats(min_value=0.0, max_value=1.0),
    st.floats(min_value=0.0, max_value=1.0),
)
def test_xyz_conversions(x: float, y: float, z: float) -> None:
    """
    Test XYZ <-> Lab conversions.
    """
    xyz = XYZColor(x, y, z)
    np.testing.assert_allclose(
        Lab_to_XYZ(XYZ_to_Lab(xyz)).get_value_tuple(),
        xyz.get_value_tuple(),
        rtol=1e-5,
        atol=1e-5,
    )


@given(
    st.floats(min_value=0.0, max_value=1.0),
    st.floats(min_value=0.0, max_value=1.0),
    st.floats(min_value=0.0, max_value=1.0),
)
def test_rgb_conversions(r: float, g: float, b: float) -> None:
    """
    Test RGB <-> Lab conversions.
    """
    rgb = RGBColor(r, g, b)
    np.testing.assert_allclose(
        Lab_to_RGB(RGB_to_Lab(rgb)).get_value_tuple(),
        rgb.get_value_tuple(),
        rtol=1e-4,
        atol=1e-4,
    )
