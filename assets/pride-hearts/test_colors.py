# -*- encoding: utf-8

import pytest

from colors import RGBColor


@pytest.mark.parametrize("hex_str, expected_colors", [
    ("#aaa", (170, 170, 170)),
    ("aaa", (170, 170, 170)),

    ("#faa", (255, 170, 170)),
    ("faa", (255, 170, 170)),

    ("#afa", (170, 255, 170)),
    ("afa", (170, 255, 170)),

    ("#aaf", (170, 170, 255)),
    ("aaf", (170, 170, 255)),

    ("#a0b0f0", (160, 176, 240)),
])
def test_from_hex_str(hex_str, expected_colors):
    assert RGBColor.from_hex_string(hex_str) == RGBColor(*expected_colors)
