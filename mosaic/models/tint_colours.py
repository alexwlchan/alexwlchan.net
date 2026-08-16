"""
Models for tint colours on a page. A page can declare light/dark modes
to use for its CSS or index page cards.
"""

from pathlib import Path
import re
from typing import Self

from pydantic import BaseModel, field_validator, model_validator


__all__ = ["TintColours", "get_default_tint_colours"]


class TintColours(BaseModel):
    """
    A set of tint colours for a page.
    """

    css_light: str | None
    css_dark: str | None
    index_light: str | None
    index_dark: str | None

    def __init__(
        self,
        css_light: str | None = None,
        css_dark: str | None = None,
        index_light: str | None = None,
        index_dark: str | None = None,
    ):
        """
        Create a new instance of TintColours.

        If only CSS colours are set, copy them to the index colours.
        """
        if index_light is None:
            index_light = css_light
        if index_dark is None:
            index_dark = css_dark

        super().__init__(
            css_light=css_light,
            css_dark=css_dark,
            index_light=index_light,
            index_dark=index_dark,
        )

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


def get_default_tint_colours(variables_path: Path) -> TintColours:
    """
    Return the default tint colours used by pages that don't set their own.
    """
    variables_css = variables_path.read_text()

    m = re.search(
        "--default-primary-color-light:[ ]+(?P<colour>#[0-9a-f]{6});", variables_css
    )
    assert m is not None
    css_light = m.group("colour")

    m = re.search(
        "--default-primary-color-dark:[ ]+(?P<colour>#[0-9a-f]{6});", variables_css
    )
    assert m is not None
    css_dark = m.group("colour")

    return TintColours(css_light=css_light, css_dark=css_dark)


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
