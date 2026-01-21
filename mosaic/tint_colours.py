"""
Code for dealing with tint colours.
"""

from pathlib import Path
import re
from typing import Self

from pydantic import BaseModel, field_validator, model_validator

from .colormath import get_contrast_ratio
from .favicons import create_favicon
from .header_images import draw_header_image


__all__ = ["get_default_tint_colours", "TintColours"]


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

    def create_assets(self, out_dir: Path) -> None:
        """
        Create all of the assets based on this tint colour.
        """
        self._create_header_image(out_dir, tint_colour=self.css_light)
        self._create_header_image(out_dir, tint_colour=self.css_dark)
        self._create_favicon(out_dir, tint_colour=self.css_light)
        self._create_favicon(out_dir, tint_colour=self.css_dark)

    def _create_favicon(self, out_dir: Path, tint_colour: str | None) -> None:
        """
        Create the favicon for this tint colour.
        """
        if tint_colour is None:
            return

        create_favicon(favicon_dir=out_dir / "f", tint_colour=tint_colour)

    def _create_header_image(self, out_dir: Path, tint_colour: str | None) -> None:
        """
        Create the header image for this tint colour.
        """
        if tint_colour is None:
            return

        hex_string = tint_colour.strip("#")
        out_path = out_dir / "h" / f"{hex_string}.png"
        out_path.parent.mkdir(exist_ok=True, parents=True)

        if out_path.exists():
            return

        im = draw_header_image(tint_colour)
        im.save(out_path)


def get_default_tint_colours(css_dir: Path) -> TintColours:
    """
    Return the default tint colours used by pages that don't set their own.
    """
    variables_css = (css_dir / "base/variables.css").read_text()

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
