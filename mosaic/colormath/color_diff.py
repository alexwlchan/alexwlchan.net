"""
The Delta E (CIE2000) difference for comparing the perceptual difference
between two colours.
"""

import math

from .color_objects import LabColor


def delta_e_cie2000(colour1: LabColor, colour2: LabColor) -> float:
    """
    Calculates the Delta E (CIE2000) of two colours.
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
