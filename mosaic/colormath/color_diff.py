"""
The functions in this module are used for comparing two LabColor objects
using various Delta E formulas.
"""

import numpy

from .color_objects import LabColor


def delta_e_cie2000(color1: LabColor, color2: LabColor) -> float:
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
    color1_vector = numpy.array([color1.lab_l, color1.lab_a, color1.lab_b])
    color2_matrix = numpy.array([(color2.lab_l, color2.lab_a, color2.lab_b)])

    Kl = Kc = Kh = 1
    L, a, b = color1_vector

    avg_Lp = (L + color2_matrix[:, 0]) / 2.0

    C1 = numpy.sqrt(numpy.sum(numpy.power(color1_vector[1:], 2)))
    C2 = numpy.sqrt(numpy.sum(numpy.power(color2_matrix[:, 1:], 2), axis=1))

    avg_C1_C2 = (C1 + C2) / 2.0

    G = 0.5 * (
        1
        - numpy.sqrt(
            numpy.power(avg_C1_C2, 7.0)
            / (numpy.power(avg_C1_C2, 7.0) + numpy.power(25.0, 7.0))
        )
    )

    a1p = (1.0 + G) * a
    a2p = (1.0 + G) * color2_matrix[:, 1]

    C1p = numpy.sqrt(numpy.power(a1p, 2) + numpy.power(b, 2))
    C2p = numpy.sqrt(numpy.power(a2p, 2) + numpy.power(color2_matrix[:, 2], 2))

    avg_C1p_C2p = (C1p + C2p) / 2.0

    h1p = numpy.degrees(numpy.arctan2(b, a1p))
    h1p += (h1p < 0) * 360

    h2p = numpy.degrees(numpy.arctan2(color2_matrix[:, 2], a2p))
    h2p += (h2p < 0) * 360

    avg_Hp = (((numpy.fabs(h1p - h2p) > 180) * 360) + h1p + h2p) / 2.0

    T = (
        1
        - 0.17 * numpy.cos(numpy.radians(avg_Hp - 30))
        + 0.24 * numpy.cos(numpy.radians(2 * avg_Hp))
        + 0.32 * numpy.cos(numpy.radians(3 * avg_Hp + 6))
        - 0.2 * numpy.cos(numpy.radians(4 * avg_Hp - 63))
    )

    diff_h2p_h1p = h2p - h1p
    delta_hp = diff_h2p_h1p + (numpy.fabs(diff_h2p_h1p) > 180) * 360
    delta_hp -= (h2p > h1p) * 720

    delta_Lp = color2_matrix[:, 0] - L
    delta_Cp = C2p - C1p
    delta_Hp = 2 * numpy.sqrt(C2p * C1p) * numpy.sin(numpy.radians(delta_hp) / 2.0)

    S_L = 1 + (
        (0.015 * numpy.power(avg_Lp - 50, 2))
        / numpy.sqrt(20 + numpy.power(avg_Lp - 50, 2.0))
    )
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T

    delta_ro = 30 * numpy.exp(-(numpy.power(((avg_Hp - 275) / 25), 2.0)))
    R_C = numpy.sqrt(
        (numpy.power(avg_C1p_C2p, 7.0))
        / (numpy.power(avg_C1p_C2p, 7.0) + numpy.power(25.0, 7.0))
    )
    R_T = -2 * R_C * numpy.sin(2 * numpy.radians(delta_ro))

    return float(
        numpy.sqrt(
            numpy.pow(delta_Lp / (S_L * Kl), 2)
            + numpy.pow(delta_Cp / (S_C * Kc), 2)
            + numpy.pow(delta_Hp / (S_H * Kh), 2)
            + R_T * (delta_Cp / (S_C * Kc)) * (delta_Hp / (S_H * Kh))
        )[0].item()
    )
