"""
Conversion between color spaces.
"""

import math

import numpy

from .color_objects import XYZColor, RGBColor, LabColor


# Not sure what these are, they are used in Lab and Luv calculations.
CIE_E = 216.0 / 24389.0
CIE_K = 24389.0 / 27.0

CIE_KE = CIE_E * CIE_K

ILLUMINANT_2_65 = {"X": 0.95047, "Y": 1.00000, "Z": 1.08883}


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
    Converts XYZ to Lab.
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

    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    rgb_matrix = numpy.array(
        (
            (3.24071, -1.53726, -0.498571),
            (-0.969258, 1.87599, 0.0415557),
            (0.0556352, -0.203996, 1.05707),
        )
    )

    # Stuff the RGB/XYZ values into a NumPy matrix for conversion.
    var_matrix = numpy.array((temp_X, temp_Y, temp_Z))
    # Perform the adaptation via matrix multiplication.
    rgb_r, rgb_g, rgb_b = numpy.dot(rgb_matrix, var_matrix)
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

    # Apply an RGB working space matrix to the XYZ values (matrix mul).
    rgb_matrix = numpy.array(
        (
            (0.412424, 0.357579, 0.180464),
            (0.212656, 0.715158, 0.0721856),
            (0.0193324, 0.119193, 0.950444),
        )
    )

    # Stuff the RGB/XYZ values into a NumPy matrix for conversion.
    var_matrix = numpy.array(
        (linear_channels["r"], linear_channels["g"], linear_channels["b"])
    )
    # Perform the adaptation via matrix multiplication.
    xyz_x, xyz_y, xyz_z = numpy.dot(rgb_matrix, var_matrix)
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
