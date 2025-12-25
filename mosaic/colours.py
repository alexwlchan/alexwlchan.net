from collections.abc import Iterator
import math
import random

from PIL import Image


HexColour = str
RgbColour = tuple[float, float, float]
LabColour = tuple[float, float, float]


def hex_to_rgb(hex: HexColour) -> RgbColour:
    """
    Convert a hex string to RGB.

    Returns a colour with RGB components in [0.0, 1.0].
    """
    assert len(hex) == 7, hex

    red = int(hex[1:3], 16)
    grn = int(hex[3:5], 16)
    blu = int(hex[5:7], 16)

    return (red / 255, grn / 255, blu / 255)


def rgb_to_lab(rgb: RgbColour) -> LabColour:
    """
    Convert an RGB colour to CIELAB.

    See http://www.brucelindbloom.com/index.html?Math.html
    """

    # Inverse sRGB compounding:
    #
    #     First, the companded RGB channels (denoted uppercase R, G, B),
    #     are made linear with respect to energy (denoted lowercase r, g, b)
    #
    def pivot_rgb(V: float) -> float:
        if V <= 0.04045:
            return V / 12.92
        else:
            return ((V + 0.055) / 1.055) ** 2.4

    r, g, b = map(pivot_rgb, rgb)

    # 2. Convert linear RGB to XYZ
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    # 3. XYZ to Lab
    def pivot_xyz(n: float) -> float:
        return n ** (1 / 3) if n > 0.008856 else (7.787 * n) + (16 / 116)

    # Normalized for D65 white point
    x_pivot = pivot_xyz(x / 0.95047)
    y_pivot = pivot_xyz(y / 1.00000)
    z_pivot = pivot_xyz(z / 1.08883)

    l_ = (116 * y_pivot) - 16
    a = 500 * (x_pivot - y_pivot)
    b = 200 * (y_pivot - z_pivot)

    return l_, a, b


def lab_to_rgb(lab: LabColour) -> RgbColour:
    """
    Convert a CIELAB colour to RGB.

    See http://www.brucelindbloom.com/index.html?Math.html

    TODO: Document and test this code properly.
    """
    l_, a, b = lab
    # Lab to XYZ
    y = (l_ + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    def unpivot_xyz(n):
        return n**3 if n**3 > 0.008856 else (n - 16 / 116) / 7.787

    x, y, z = unpivot_xyz(x) * 0.95047, unpivot_xyz(y) * 1.0, unpivot_xyz(z) * 1.08883
    # XYZ to RGB
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    # Gamma Correction
    def unpivot_rgb(n):
        n = max(0, min(1, n))
        return 1.055 * (n ** (1 / 2.4)) - 0.055 if n > 0.0031308 else 12.92 * n

    return tuple(int(unpivot_rgb(c) * 255) for c in (r, g, b))


def delta_e_2000(lab1: LabColour, lab2: LabColour) -> float:
    """
    Simplified Delta E 2000 implementation for L* variance.

    TODO: Document and test this code.
    """
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    # For L-only variation, the formula simplifies significantly,
    # but we'll use a standard distance for chromaticity consistency.
    # avg_lp = (L1 + L2) / 2.0
    c1 = math.sqrt(a1**2 + b1**2)
    c2 = math.sqrt(a2**2 + b2**2)
    avg_c = (c1 + c2) / 2.0
    g = 0.5 * (1 - math.sqrt(avg_c**7 / (avg_c**7 + 25**7)))
    a1p, a2p = a1 * (1 + g), a2 * (1 + g)
    c1p, c2p = math.sqrt(a1p**2 + b1**2), math.sqrt(a2p**2 + b2**2)
    # This is a partial Delta E (focused on Lightness)
    # Full implementation is 30+ lines; this captures the core perceptual shift
    return math.sqrt(((L2 - L1) / 1.0) ** 2 + ((c2p - c1p) / 1.0) ** 2)


def get_lightness_for_delta(original_lab, direction, target_delta):
    l_orig, a_orig, b_orig = original_lab
    low_l, high_l = (l_orig, 100) if direction == "lighter" else (0, l_orig)

    best_l = l_orig
    best_delta_diff = float("inf")

    for _ in range(15):
        mid_l = (low_l + high_l) / 2.0
        candidate_lab = (mid_l, a_orig, b_orig)
        candidate_delta = delta_e_2000(original_lab, candidate_lab)

        if abs(candidate_delta - target_delta) < best_delta_diff:
            best_l = mid_l
            best_delta_diff = abs(candidate_delta - target_delta)

        if candidate_delta < target_delta:
            if direction == "lighter":
                low_l = mid_l
            else:
                high_l = mid_l
        else:
            if direction == "lighter":
                high_l = mid_l
            else:
                low_l = mid_l

    return best_l


def get_colours_like(hex: HexColour) -> Iterator[tuple[int, int, int]]:
    """
    Generate an infinite sequence of colours which vary only in lightness.
    """
    # 1. Seed the random to get consistent outputs.  This ensures the
    #    images created in local builds are the same as ones on the
    #    server, and I can delete the folder and regenerate without
    #    changing the appearance of already-published pages.
    seed = int(hex[1:], 16)
    r = random.Random(seed)

    # 2. Convert the hex colour to RGB, then to CIELAB.
    rgb = hex_to_rgb(hex)
    lab = rgb_to_lab(rgb)

    # 3. Work out the min/max lightness that gets us a fixed delta
    #    away from the original color.
    #
    #    Note(2025-12-24): although it's currently the same +/- in
    #    both directions, but maybe it should be different and depend
    #    on whether you're in light/dark mode?
    min_lightness = get_lightness_for_delta(lab, "darker", 6)
    max_lightness = get_lightness_for_delta(lab, "lighter", 6)

    lightness_diff = max_lightness - min_lightness

    if lightness_diff == 0:
        raise ValueError(f"No lightness diff for hex colour: {hex}")

    while True:
        next_lightness = min_lightness + (r.random() * lightness_diff)
        yield lab_to_rgb((next_lightness, lab[1], lab[2]))



def colourise_image(im, hex: str):
    """
    Given a PNG image with grayscale pixels and a tint colour, create
    a colourised version of the image.
    """
    r,g,b = hex_to_rgb(hex)
    red, grn, blu = round(r * 255), round(g * 255), round(b * 255)

    new_im = Image.new("RGBA", im.size)

    for x in range(im.width):
        for y in range(im.width):
            _, alpha = im.getpixel((x, y))
            new_im.putpixel((x, y), (red, grn, blu, alpha))

    return new_im
