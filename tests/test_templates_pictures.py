"""
Tests for `mosaic.templates.pictures`.
"""

from pathlib import Path

import pytest

from mosaic.templates import pictures as tp


class TestChooseTargetWidth:
    """
    Tests for `choose_target_width`.
    """

    @pytest.mark.parametrize("width", [100, 200, 800])
    def test_chooses_based_on_target_width(self, width: int) -> None:
        """
        It chooses the correct width based on target width.
        """
        expected = width
        actual = tp.choose_target_width(
            src_path=Path("tests/fixtures/truchet-tiles-800x400.png"),
            target_width=width,
            target_height=None,
        )

        assert actual == expected

    @pytest.mark.parametrize("height", [100, 200, 400])
    def test_chooses_based_on_target_height(self, height: int) -> None:
        """
        It chooses the correct width based on target height.
        """
        expected = height * 2
        actual = tp.choose_target_width(
            src_path=Path("tests/fixtures/truchet-tiles-800x400.png"),
            target_width=None,
            target_height=height,
        )

        assert actual == expected

    def test_no_dimensions_is_error(self) -> None:
        """
        Omitting dimensions is a TypeError.
        """
        with pytest.raises(TypeError):
            tp.choose_target_width(
                src_path=Path("tests/fixtures/truchet-tiles-800x400.png"),
                target_width=None,
                target_height=None,
            )

    def test_both_dimensions_is_error(self) -> None:
        """
        Supplying both dimensions is a TypeError.
        """
        with pytest.raises(TypeError):
            tp.choose_target_width(
                src_path=Path("tests/fixtures/truchet-tiles-800x400.png"),
                target_width=100,
                target_height=100,
            )

    @pytest.mark.parametrize("width", [801, 1000, 2000])
    def test_too_wide_is_error(self, width: int) -> None:
        """
        A target width larger than the original Image is a ValueError.
        """
        with pytest.raises(ValueError):
            tp.choose_target_width(
                src_path=Path("tests/fixtures/truchet-tiles-800x400.png"),
                target_width=width,
                target_height=None,
            )

    @pytest.mark.parametrize("height", [401, 800, 1000])
    def test_too_high_is_error(self, height: int) -> None:
        """
        A target height larger than the original Image is a ValueError.
        """
        with pytest.raises(ValueError):
            tp.choose_target_width(
                src_path=Path("tests/fixtures/truchet-tiles-800x400.png"),
                target_width=None,
                target_height=height,
            )
