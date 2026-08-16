"""
Tests for `colormath.color_conversions`.
"""

from typing import Any

from hypothesis import given, strategies as st
import pytest

from mosaic.images.colours import (
    RGBColor,
    LabColor,
    XYZColor,
    RGB_to_Lab,
    Lab_to_RGB,
    XYZ_to_RGB,
    RGB_to_XYZ,
    XYZ_to_Lab,
    Lab_to_XYZ,
    delta_e_cie2000,
)


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

    for part1, part2 in zip(c1.get_value_tuple(), c2.get_value_tuple()):
        assert abs(part1 - part2) <= 1e-3


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
    xyz_rt = Lab_to_XYZ(XYZ_to_Lab(xyz))

    for part1, part2 in zip(xyz.get_value_tuple(), xyz_rt.get_value_tuple()):
        assert abs(part1 - part2) <= 1e-4


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
    rgb_rt = Lab_to_RGB(RGB_to_Lab(rgb))

    for part1, part2 in zip(rgb.get_value_tuple(), rgb_rt.get_value_tuple()):
        assert abs(part1 - part2) <= 1e-4


def test_cie2000_accuracy() -> None:
    """
    Test the accuracy of CIEDE2000 difference.
    """
    c1 = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)
    c2 = LabColor(lab_l=0.7, lab_a=14.2, lab_b=-1.80)
    result = delta_e_cie2000(c1, c2)
    expected = 1.522585
    assert abs(result - expected) <= 1e-5


def test_cie2000_accuracy_2() -> None:
    """
    Follow a different execution path based on variable values.
    """
    # These values are from ticket 8 in regards to a CIE2000 bug.
    c1 = LabColor(lab_l=32.8911, lab_a=-53.0107, lab_b=-43.3182)
    c2 = LabColor(lab_l=77.1797, lab_a=25.5928, lab_b=17.9412)
    result = delta_e_cie2000(c1, c2)
    expected = 78.772
    assert abs(result - expected) <= 1e-3


def test_cie2000_accuracy_3() -> None:
    """
    Test the accuracy of CIEDE2000 difference.

    Reference:
    "The CIEDE2000 Color-Difference Formula: Implementation Notes,
    Supplementary Test Data, and Mathematical Observations,", G. Sharma,
    W. Wu, E. N. Dalal, submitted to Color Research and Application,
    January 2004. http://www.ece.rochester.edu/~gsharma/ciede2000/
    """
    color1 = (
        LabColor(lab_l=50.0000, lab_a=2.6772, lab_b=-79.7751),
        LabColor(lab_l=50.0000, lab_a=3.1571, lab_b=-77.2803),
        LabColor(lab_l=50.0000, lab_a=2.8361, lab_b=-74.0200),
        LabColor(lab_l=50.0000, lab_a=-1.3802, lab_b=-84.2814),
        LabColor(lab_l=50.0000, lab_a=-1.1848, lab_b=-84.8006),
        LabColor(lab_l=50.0000, lab_a=-0.9009, lab_b=-85.5211),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=-1.0000, lab_b=2.0000),
        LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
        LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
        LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
        LabColor(lab_l=50.0000, lab_a=2.4900, lab_b=-0.0010),
        LabColor(lab_l=50.0000, lab_a=-0.0010, lab_b=2.4900),
        LabColor(lab_l=50.0000, lab_a=-0.0010, lab_b=2.4900),
        LabColor(lab_l=50.0000, lab_a=-0.0010, lab_b=2.4900),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=2.5000, lab_b=0.0000),
        LabColor(lab_l=60.2574, lab_a=-34.0099, lab_b=36.2677),
        LabColor(lab_l=63.0109, lab_a=-31.0961, lab_b=-5.8663),
        LabColor(lab_l=61.2901, lab_a=3.7196, lab_b=-5.3901),
        LabColor(lab_l=35.0831, lab_a=-44.1164, lab_b=3.7933),
        LabColor(lab_l=22.7233, lab_a=20.0904, lab_b=-46.6940),
        LabColor(lab_l=36.4612, lab_a=47.8580, lab_b=18.3852),
        LabColor(lab_l=90.8027, lab_a=-2.0831, lab_b=1.4410),
        LabColor(lab_l=90.9257, lab_a=-0.5406, lab_b=-0.9208),
        LabColor(lab_l=6.7747, lab_a=-0.2908, lab_b=-2.4247),
        LabColor(lab_l=2.0776, lab_a=0.0795, lab_b=-1.1350),
    )
    color2 = (
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-82.7485),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-82.7485),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-82.7485),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-82.7485),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-82.7485),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-82.7485),
        LabColor(lab_l=50.0000, lab_a=-1.0000, lab_b=2.0000),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=-2.4900, lab_b=0.0009),
        LabColor(lab_l=50.0000, lab_a=-2.4900, lab_b=0.0010),
        LabColor(lab_l=50.0000, lab_a=-2.4900, lab_b=0.0011),
        LabColor(lab_l=50.0000, lab_a=-2.4900, lab_b=0.0012),
        LabColor(lab_l=50.0000, lab_a=0.0009, lab_b=-2.4900),
        LabColor(lab_l=50.0000, lab_a=0.0010, lab_b=-2.4900),
        LabColor(lab_l=50.0000, lab_a=0.0011, lab_b=-2.4900),
        LabColor(lab_l=50.0000, lab_a=0.0000, lab_b=-2.5000),
        LabColor(lab_l=73.0000, lab_a=25.0000, lab_b=-18.0000),
        LabColor(lab_l=61.0000, lab_a=-5.0000, lab_b=29.0000),
        LabColor(lab_l=56.0000, lab_a=-27.0000, lab_b=-3.0000),
        LabColor(lab_l=58.0000, lab_a=24.0000, lab_b=15.0000),
        LabColor(lab_l=50.0000, lab_a=3.1736, lab_b=0.5854),
        LabColor(lab_l=50.0000, lab_a=3.2972, lab_b=0.0000),
        LabColor(lab_l=50.0000, lab_a=1.8634, lab_b=0.5757),
        LabColor(lab_l=50.0000, lab_a=3.2592, lab_b=0.3350),
        LabColor(lab_l=60.4626, lab_a=-34.1751, lab_b=39.4387),
        LabColor(lab_l=62.8187, lab_a=-29.7946, lab_b=-4.0864),
        LabColor(lab_l=61.4292, lab_a=2.2480, lab_b=-4.9620),
        LabColor(lab_l=35.0232, lab_a=-40.0716, lab_b=1.5901),
        LabColor(lab_l=23.0331, lab_a=14.9730, lab_b=-42.5619),
        LabColor(lab_l=36.2715, lab_a=50.5065, lab_b=21.2231),
        LabColor(lab_l=91.1528, lab_a=-1.6435, lab_b=0.0447),
        LabColor(lab_l=88.6381, lab_a=-0.8985, lab_b=-0.7239),
        LabColor(lab_l=5.8714, lab_a=-0.0985, lab_b=-2.2286),
        LabColor(lab_l=0.9033, lab_a=-0.0636, lab_b=-0.5514),
    )
    diff = (
        2.0424,
        2.8615,
        3.4412,
        1.0000,
        1.0000,
        1.0000,
        2.3669,
        2.3669,
        7.1792,
        7.1792,
        7.2195,
        7.2195,
        4.8045,
        4.8045,
        4.7461,
        4.3065,
        27.1492,
        22.8977,
        31.9030,
        19.4535,
        1.0000,
        1.0000,
        1.0000,
        1.0000,
        1.2644,
        1.2630,
        1.8731,
        1.8645,
        2.0373,
        1.4146,
        1.4441,
        1.5381,
        0.6377,
        0.9082,
    )
    for l_set in zip(color1, color2, diff):
        result = delta_e_cie2000(l_set[0], l_set[1])
        expected = l_set[2]
        assert abs(result - expected) <= 1e-4
