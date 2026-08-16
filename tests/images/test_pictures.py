"""
Tests for `mosaic.images.pictures`.
"""

from pathlib import Path

import pytest

from mosaic.images import pictures as p


class TestChooseTargetWidth:
    """
    Tests for `choose_target_width`.
    """

    fixtures_dir = Path("tests/fixtures")

    @pytest.mark.parametrize("width", [100, 200, 800])
    def test_chooses_based_on_target_width(self, width: int) -> None:
        """
        It chooses the correct width based on target width.
        """
        expected = width
        actual = p.choose_target_width(
            src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
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
        actual = p.choose_target_width(
            src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
            target_width=None,
            target_height=height,
        )

        assert actual == expected

    def test_no_dimensions_is_error(self) -> None:
        """
        Omitting dimensions is a TypeError.
        """
        with pytest.raises(TypeError):
            p.choose_target_width(
                src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
                target_width=None,
                target_height=None,
            )

    def test_both_dimensions_is_error(self) -> None:
        """
        Supplying both dimensions is a TypeError.
        """
        with pytest.raises(TypeError):
            p.choose_target_width(
                src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
                target_width=100,
                target_height=100,
            )

    @pytest.mark.parametrize("width", [801, 1000, 2000])
    def test_too_wide_is_error(self, width: int) -> None:
        """
        A target width larger than the original Image is a ValueError.
        """
        with pytest.raises(ValueError):
            p.choose_target_width(
                src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
                target_width=width,
                target_height=None,
            )

    @pytest.mark.parametrize("height", [401, 800, 1000])
    def test_too_high_is_error(self, height: int) -> None:
        """
        A target height larger than the original Image is a ValueError.
        """
        with pytest.raises(ValueError):
            p.choose_target_width(
                src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
                target_width=None,
                target_height=height,
            )

    def test_rounding_width(self) -> None:
        """
        Rounding is to the nearest integer.
        """
        # The source image is 373 × 480 pixels, so the target width is
        # 373 × 140 / 480 = 108.79, which rounds to 109.
        width = p.choose_target_width(
            src_path=Path("src/images/2021/your-computer-is-on-fire.jpg"),
            target_width=None,
            target_height=140,
        )

        assert width == 109
