"""
Code for computing the contrast between two colours.
"""

__all__ = ["get_contrast_ratio"]


def get_relative_luminance(hex_colour: str) -> float:
    """
    Get the relative luminance of a hexadecimal colour.
    """
    r = int(hex_colour[1:3], 16) / 255
    g = int(hex_colour[3:5], 16) / 255
    b = int(hex_colour[5:7], 16) / 255
    rgb = [r, g, b]

    # sRGB gamma correction
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_contrast_ratio(colour1: str, colour2: str) -> float:
    """
    Return the WCAG contrast ratio of two colours as hex strings.
    """
    l1 = get_relative_luminance(colour1)
    l2 = get_relative_luminance(colour2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
