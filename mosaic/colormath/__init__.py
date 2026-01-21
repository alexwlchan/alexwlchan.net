"""
Code for dealing with RGB and CIELAB colours.

This is based on Greg Taylor's colormath module [1]. I copied out the
parts that were relevant to me, then added type hints and more tests.

[1]: https://github.com/gtaylor/python-colormath
"""

from .color_diff import delta_e_cie2000
from .color_objects import RGBColor, LabColor
from .color_conversions import RGB_to_Lab, Lab_to_RGB
from .contrast import get_contrast_ratio

__all__ = [
    "delta_e_cie2000",
    "get_contrast_ratio",
    "RGBColor",
    "LabColor",
    "RGB_to_Lab",
    "Lab_to_RGB",
]
