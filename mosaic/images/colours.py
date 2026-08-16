"""
Code for dealing with RGB and CIELAB colours.

This is based on Greg Taylor's colormath module [1]. I copied out the
parts that were relevant to me, then added type hints and more tests.

[1]: https://github.com/gtaylor/python-colormath
"""

from dataclasses import dataclass
import math


__all__ = [
    "LabColor",
    "RGBColor",
    "RGB_to_Lab",
    "Lab_to_RGB",
    "delta_e_cie2000",
]


# Not sure what these are, they are used in Lab and Luv calculations.
CIE_E = 216.0 / 24389.0
CIE_K = 24389.0 / 27.0

CIE_KE = CIE_E * CIE_K

ILLUMINANT_2_65 = {"X": 0.95047, "Y": 1.00000, "Z": 1.08883}


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
        Return a tuple of the color's values (in order).
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
        Return a tuple of the color's values (in order).
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
        Return a tuple of the color's values (in order).
        """
        return (self.rgb_r, self.rgb_g, self.rgb_b)

    @classmethod
    def new_from_rgb_hex(cls, hex_str: str) -> "RGBColor":
        """
        Convert an RGB hex string like #RRGGBB and assigns the values to
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


def Lab_to_XYZ(lab: LabColor) -> XYZColor:
    """
    Convert from Lab to XYZ.
    """
    fy = (lab.lab_l + 16) / 116
    fx = lab.lab_a / 500.0 + fy
    fz = fy - lab.lab_b / 200.0

    if lab.lab_l > CIE_KE:
        xyz_y = math.pow(fy, 3)
    else:
        xyz_y = lab.lab_l / CIE_K

    if math.pow(fx, 3) > CIE_E:
        xyz_x = math.pow(fx, 3)
    else:
        xyz_x = (116 * fx - 16.0) / CIE_K

    if math.pow(fz, 3) > CIE_E:
        xyz_z = math.pow(fz, 3)
    else:
        xyz_z = (116 * fz - 16) / CIE_K

    xyz_x = ILLUMINANT_2_65["X"] * xyz_x
    xyz_y = ILLUMINANT_2_65["Y"] * xyz_y
    xyz_z = ILLUMINANT_2_65["Z"] * xyz_z

    return XYZColor(xyz_x, xyz_y, xyz_z)


def XYZ_to_Lab(xyz: XYZColor) -> LabColor:
    """
    Convert from XYZ to Lab.
    """
    temp_x = xyz.xyz_x / ILLUMINANT_2_65["X"]
    temp_y = xyz.xyz_y / ILLUMINANT_2_65["Y"]
    temp_z = xyz.xyz_z / ILLUMINANT_2_65["Z"]

    if temp_x > CIE_E:
        temp_x = math.pow(temp_x, (1.0 / 3.0))
    else:
        temp_x = (7.787 * temp_x) + (16.0 / 116.0)

    if temp_y > CIE_E:
        temp_y = math.pow(temp_y, (1.0 / 3.0))
    else:
        temp_y = (7.787 * temp_y) + (16.0 / 116.0)

    if temp_z > CIE_E:
        temp_z = math.pow(temp_z, (1.0 / 3.0))
    else:
        temp_z = (7.787 * temp_z) + (16.0 / 116.0)

    lab_l = (116.0 * temp_y) - 16.0
    lab_a = 500.0 * (temp_x - temp_y)
    lab_b = 200.0 * (temp_y - temp_z)
    return LabColor(lab_l, lab_a, lab_b)


def XYZ_to_RGB(xyz: XYZColor) -> RGBColor:
    """
    XYZ to RGB conversion.
    """
    temp_X = xyz.xyz_x
    temp_Y = xyz.xyz_y
    temp_Z = xyz.xyz_z

    # Apply an RGB working space matrix to the XYZ values.
    # fmt: off
    rgb_r =  3.24071   * temp_X - 1.53726  * temp_Y - 0.498571  * temp_Z
    rgb_g = -0.969258  * temp_X + 1.87599  * temp_Y + 0.0415557 * temp_Z
    rgb_b =  0.0556352 * temp_X - 0.203996 * temp_Y + 1.05707   * temp_Z
    # fmt: on

    # Clamp these values to a valid range.
    rgb_r = max(rgb_r, 0.0)
    rgb_g = max(rgb_g, 0.0)
    rgb_b = max(rgb_b, 0.0)

    # v
    linear_channels = dict(r=rgb_r, g=rgb_g, b=rgb_b)
    # V
    nonlinear_channels = {}

    for channel in ["r", "g", "b"]:
        v = linear_channels[channel]
        if v <= 0.0031308:
            nonlinear_channels[channel] = v * 12.92
        else:
            nonlinear_channels[channel] = 1.055 * math.pow(v, 1 / 2.4) - 0.055

    return RGBColor(
        nonlinear_channels["r"], nonlinear_channels["g"], nonlinear_channels["b"]
    )


def RGB_to_XYZ(rgb: RGBColor) -> XYZColor:
    """
    RGB to XYZ conversion. Expects RGB values between 0 and 1.

    Based off of: http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    """
    # Will contain linearized RGB channels (removed the gamma func).
    linear_channels = {}

    for channel in ["r", "g", "b"]:
        V = getattr(rgb, "rgb_" + channel)
        if V <= 0.04045:
            linear_channels[channel] = V / 12.92
        else:
            linear_channels[channel] = math.pow((V + 0.055) / 1.055, 2.4)

    # Stuff the RGB/XYZ values into a NumPy matrix for conversion.
    temp_r = linear_channels["r"]
    temp_g = linear_channels["g"]
    temp_b = linear_channels["b"]

    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    # fmt: off
    xyz_x = 0.412424  * temp_r + 0.357579 * temp_g + 0.180464  * temp_b
    xyz_y = 0.212656  * temp_r + 0.715158 * temp_g + 0.0721856 * temp_b
    xyz_z = 0.0193324 * temp_r + 0.119193 * temp_g + 0.950444  * temp_b

    # Clamp these values to a valid range.
    xyz_x = max(xyz_x, 0.0)
    xyz_y = max(xyz_y, 0.0)
    xyz_z = max(xyz_z, 0.0)

    return XYZColor(xyz_x, xyz_y, xyz_z)


def RGB_to_Lab(rgb: RGBColor) -> LabColor:
    """
    Convert an RGB colour to CIELAB.
    """
    xyz = RGB_to_XYZ(rgb)
    lab = XYZ_to_Lab(xyz)
    return lab


def Lab_to_RGB(lab: LabColor) -> RGBColor:
    """
    Convert a CIELAB colour to RGB.
    """
    xyz = Lab_to_XYZ(lab)
    rgb = XYZ_to_RGB(xyz)
    return rgb


def delta_e_cie2000(colour1: LabColor, colour2: LabColor) -> float:
    """
    Calculate the Delta E (CIE2000) of two colours.
    """
    # Weighting factors
    Kl = Kc = Kh = 1

    L1, a1, b1 = colour1.lab_l, colour1.lab_a, colour1.lab_b
    L2, a2, b2 = colour2.lab_l, colour2.lab_a, colour2.lab_b

    avg_Lp = (L1 + L2) / 2

    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    avg_C = (C1 + C2) / 2

    C7 = avg_C**7
    G = 0.5 * (1 - math.sqrt(C7 / (C7 + 25**7)))

    a1p = (1.0 + G) * a1
    a2p = (1.0 + G) * a2

    C1p = math.sqrt(a1p**2 + b1**2)
    C2p = math.sqrt(a2p**2 + b2**2)
    avg_C1p_C2p = (C1p + C2p) / 2

    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360

    if abs(h1p - h2p) > 180:
        avg_Hp = (h1p + h2p + 360) / 2
    else:
        avg_Hp = (h1p + h2p) / 2

    T = (
        1
        - 0.17 * math.cos(math.radians(avg_Hp - 30))
        + 0.24 * math.cos(math.radians(2 * avg_Hp))
        + 0.32 * math.cos(math.radians(3 * avg_Hp + 6))
        - 0.2 * math.cos(math.radians(4 * avg_Hp - 63))
    )

    diff_h = h2p - h1p
    if abs(diff_h) <= 180:
        delta_hp_raw = diff_h
    else:
        delta_hp_raw = diff_h + (360 if h2p <= h1p else -360)

    delta_Lp = L2 - L1
    delta_Cp = C2p - C1p
    delta_Hp = 2 * math.sqrt(C2p * C1p) * math.sin(math.radians(delta_hp_raw) / 2)

    S_L = 1 + ((0.015 * (avg_Lp - 50) ** 2) / math.sqrt(20 + (avg_Lp - 50) ** 2))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T

    delta_ro = 30 * math.exp(-(((avg_Hp - 275) / 25) ** 2))
    C7p = avg_C1p_C2p**7
    R_C = 2 * math.sqrt(C7p / (C7p + 25**7))
    R_T = -math.sin(2 * math.radians(delta_ro)) * R_C

    dist_l = delta_Lp / (S_L * Kl)
    dist_c = delta_Cp / (S_C * Kc)
    dist_h = delta_Hp / (S_H * Kh)

    total_de = math.sqrt(dist_l**2 + dist_c**2 + dist_h**2 + R_T * dist_c * dist_h)

    return total_de
