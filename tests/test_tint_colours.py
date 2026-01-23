"""
Tests for `mosaic.tint_colours`.
"""

from pathlib import Path

from PIL import Image
from pydantic import ValidationError
import pytest

from mosaic.tint_colours import TintColours, get_default_tint_colours


def test_get_default_tint_colours() -> None:
    """
    Test for get_default_tint_colours.
    """
    c = get_default_tint_colours(css_dir=Path("css"))
    assert c.css_light == "#d01c11"
    assert c.css_dark == "#ff4a4a"


class TestTintColours:
    """
    Tests for TintColours, especially validation.
    """

    def test_valid_hex_string_is_allowed(self) -> None:
        """
        Creating a TintColours with valid hex strings is fine.
        """
        TintColours(
            css_light="#000000", css_dark="#ffffff", index_light=None, index_dark=None
        )

    @pytest.mark.parametrize("hex_string", ["", "#", "#12345", "#1234567", "zzz"])
    def test_invalid_hex_string_is_error(self, hex_string: str) -> None:
        """
        Creating an instance of TintColours with an invalid hex string
        is an error.
        """
        with pytest.raises(ValidationError, match="invalid hex colour"):
            TintColours(css_light=hex_string, css_dark=hex_string)

        with pytest.raises(ValidationError, match="invalid hex colour"):
            TintColours(index_light=hex_string, index_dark=hex_string)

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"css_light": "#dddddd", "css_dark": "#dddddd"},
            {"css_light": "#222222", "css_dark": "#222222"},
            # TODO(2026-01-20): Add contrast checks for index colours.
            # {"index_light": "#dddddd", "index_dark": "#dddddd"},
            # {"index_light": "#222222", "index_dark": "#222222"},
        ],
    )
    def test_insufficient_contrast_is_error(self, kwargs: dict[str, str]) -> None:
        """
        Creating a TintColours with insufficient contrast is an erorr.
        """
        with pytest.raises(ValidationError, match="contrast ratio"):
            TintColours(**kwargs)

    def test_colours_must_be_pairs(self) -> None:
        """
        Colours must be supplied in pairs; both or neither.
        """
        with pytest.raises(ValidationError):
            TintColours(css_dark="#dddddd", index_dark="#dddddd", index_light="#222222")

    def test_creates_asset_images(self, out_dir: Path) -> None:
        """
        Create all the asset images for a tint colour.
        """
        c = TintColours(css_light="#220000", css_dark="#00ff00")

        # Run the process multiple times to check that calling it repeatedly
        # is a no-op.
        for _ in range(2):
            c.create_assets(out_dir)

            for name, width, height in [
                ("h/220000.png", 2500, 250),
                ("h/00ff00.png", 2500, 250),
                ("f/220000.ico", 16, 16),
                ("f/00ff00.ico", 16, 16),
            ]:
                assert (out_dir / name).exists()

                with Image.open(out_dir / name) as im:
                    assert im.size == (width, height)

    def test_no_asset_images_if_only_index_colours(self, out_dir: Path) -> None:
        """
        If the tint colours are only for the index, no asset images are
        created.
        """
        c = TintColours(index_light="#220000", index_dark="#00ff00")
        c.create_assets(out_dir)
        assert not out_dir.exists()
