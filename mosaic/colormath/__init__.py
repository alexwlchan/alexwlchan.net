"""
Code for dealing with RGB and CIELAB colours.

This is based on Greg Taylor's colormath module [1]. I copied out the
parts that were relevant to me, then added type hints and more tests.

[1]: https://github.com/gtaylor/python-colormath
"""

from .color_diff import delta_e_cie2000
from .color_objects import RGBColor, LabColor
from .color_conversions import RGB_to_Lab, Lab_to_RGB

__all__ = [
    "delta_e_cie2000",
    "RGBColor",
    "LabColor",
    "RGB_to_Lab",
    "Lab_to_RGB",
]
