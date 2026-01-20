"""
Code for dealing with tint colours.
"""

from collections.abc import Iterator
import random
import re
from typing import Literal, Self, TypeAlias

from pydantic import BaseModel, field_validator, model_validator

from .colormath import (
    LabColor,
    RGBColor,
    RGB_to_Lab,
    Lab_to_RGB,
    delta_e_cie2000,
    get_contrast_ratio,
)


__all__ = ["generate_colours_like", "TintColours"]


class TintColours(BaseModel):
    """
    A set of tint colours for a page.
    """

    css_light: str | None = None
    css_dark: str | None = None
    index_light: str | None = None
    index_dark: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def validate_hex_format(cls, v: str | None) -> str | None:
        """
        Validate that every colour is a hexadecimal string.
        """
        if v is None:
            return None
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
            raise ValueError(f"invalid hex colour: {v}")
        return v.lower()

    @model_validator(mode="after")
    def check_contrast(self) -> Self:
        """
        Ensure every colour has sufficient contrast with the background.
        """
        # TODO(2026-01-20): Add contrast checks for index colours.
        # TODO(2026-01-20): Switch to newer contrast algorithms.
        checks = [
            ("css_light", "#ffffff"),
            # ("index_light", "#ffffff"),
            ("css_dark", "#000000"),
            # ("index_dark", "#000000"),
        ]

        for field_name, bg_hex in checks:
            fg_hex = getattr(self, field_name)
            if fg_hex:
                ratio = get_contrast_ratio(fg_hex, bg_hex)
                if ratio < 4.5:
                    raise ValueError(
                        f"contrast ratio for {field_name} ({fg_hex}) is too low: "
                        f"{ratio:.2f}:1 against {bg_hex} (min 4.5:1)"
                    )
        return self

    @model_validator(mode="after")
    def validate_pairs(self) -> Self:
        """
        Validate that CSS and index colours are specified as pairs.
        """
        # Define the pairs to check
        pairs = [
            ("css_light", "css_dark"),
            ("index_light", "index_dark"),
        ]

        for light_field, dark_field in pairs:
            light_val = getattr(self, light_field)
            dark_val = getattr(self, dark_field)

            # If exactly one is set, raise an error
            if (light_val is None) != (dark_val is None):
                missing = light_field if light_val is None else dark_field
                present = dark_field if light_val is None else light_field
                raise ValueError(
                    f"incomplete colour pair: {present!r} is set, "
                    f"so {missing!r} must also be defined."
                )

        return self


# An RGB colour whose components are in the range [0, 255].
ColourRGB_255: TypeAlias = tuple[int, int, int]


def generate_colours_like(hex_colour: str) -> Iterator[ColourRGB_255]:
    """
    Generate an infinite sequence of colours varying only in lightness.

    Returns a sequence of RGB colours, where each component is in the
    range [0, 255].
    """
    # Seed from the hex integer value. This ensures the random lightness
    # is consistent across builds and devices.
    seed = int(hex_colour.lstrip("#"), 16)
    rand = random.Random(seed)

    # Convert to CIELAB.
    rgb = RGBColor.new_from_rgb_hex(hex_colour)
    lab = RGB_to_Lab(rgb)

    # Find the bounds for random values of L*
    min_l: float = get_lightness_for_delta(lab, "darker", 6.0)
    max_l: float = get_lightness_for_delta(lab, "lighter", 6.0)
    l_range: float = max_l - min_l

    # Generate infinite colours in this range
    while True:
        new_l = min_l + (rand.random() * l_range)
        new_lab = LabColor(new_l, lab.lab_a, lab.lab_b)

        # Discard colours which don't map cleanly from CIELAB to sRGB.
        round_trip_lab = RGB_to_Lab(Lab_to_RGB(new_lab))
        if delta_e_cie2000(new_lab, round_trip_lab) > 1.0:
            continue

        rgb = Lab_to_RGB(new_lab)
        yield (round(rgb.rgb_r * 255), round(rgb.rgb_g * 255), round(rgb.rgb_b * 255))


def get_lightness_for_delta(
    original_lab: LabColor,
    direction: Literal["lighter", "darker"],
    target_delta: float,
) -> float:
    """
    Find the lightness of a CIELAB colour that gets the target CIELAB ΔE* 2000
    perceptual distance from the original colour, while preserving the
    original chromacity.
    """
    l_orig = original_lab.lab_l

    # Define the search range for L*
    low_l = l_orig if direction == "lighter" else 0.0
    high_l = 100.0 if direction == "lighter" else l_orig

    # Run a binary search on L*
    best_l: float = l_orig

    for _ in range(15):
        mid_l = (low_l + high_l) / 2.0
        candidate_lab = LabColor(mid_l, original_lab.lab_a, original_lab.lab_b)

        # Calculate the perceptual difference
        candidate_delta = delta_e_cie2000(original_lab, candidate_lab)

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
        best_l = mid_l

    return best_l
