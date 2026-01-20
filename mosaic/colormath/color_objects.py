"""
Classes to represent various color spaces.
"""

from dataclasses import dataclass


@dataclass
class LabColor:
    """
    Represents a CIE Lab color. For more information on CIE Lab,
    see `Lab color space <http://en.wikipedia.org/wiki/Lab_color_space>`_ on
    Wikipedia.
    """

    lab_l: float
    lab_a: float
    lab_b: float

    def get_value_tuple(self) -> tuple[float, float, float]:
        """
        Returns a tuple of the color's values (in order).
        """
        return (self.lab_l, self.lab_a, self.lab_b)


@dataclass
class XYZColor:
    """
    Represents an XYZ color.
    """

    xyz_x: float
    xyz_y: float
    xyz_z: float

    def get_value_tuple(self) -> tuple[float, float, float]:
        """
        Returns a tuple of the color's values (in order).
        """
        return (self.xyz_x, self.xyz_y, self.xyz_z)


@dataclass
class RGBColor:
    """
    Represents an sRGB color.
    """

    rgb_r: float
    rgb_g: float
    rgb_b: float

    def get_value_tuple(self) -> tuple[float, float, float]:
        """
        Returns a tuple of the color's values (in order).
        """
        return (self.rgb_r, self.rgb_g, self.rgb_b)

    @classmethod
    def new_from_rgb_hex(cls, hex_str: str) -> "RGBColor":
        """
        Converts an RGB hex string like #RRGGBB and assigns the values to
        this RGBColor object.
        """
        colorstring = hex_str.strip()
        if colorstring and colorstring[0] == "#":
            colorstring = colorstring[1:]
        if len(colorstring) != 6:
            raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
        rs, gs, bs = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) / 255.0 for n in (rs, gs, bs)]
        return cls(r, g, b)
