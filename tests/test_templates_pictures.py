"""
Tests for `mosaic.templates.pictures`.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil

from jinja2 import Environment
import minify_html
from PIL import UnidentifiedImageError
import pytest

from mosaic.templates import pictures as tp


@dataclass
class StubPage:
    """Stub entry for a page."""

    date: datetime | None


class TestPictureExtension:
    """
    Tests for PictureExtension.
    """

    def test_render_picture(
        self, src_dir: Path, out_dir: Path, env: Environment
    ) -> None:
        """
        Test the basic usage of the {% picture %} tag.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles-800x400.png",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% picture filename="truchet-tiles-800x400.png" '
            'width="400" alt="Geometrically-drawn tiles in red and black" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            "<picture>"
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400_1x.avif 400w,'
            '/images/2026/truchet-tiles-800x400_2x.avif 800w" '
            "type=image/avif>"
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400_1x.webp 400w,'
            '/images/2026/truchet-tiles-800x400_2x.webp 800w" '
            'type=image/webp><source sizes="(max-width: 400px) 100vw, '
            '400px" srcset="/images/2026/truchet-tiles-800x400_1x.png 400w,'
            '/images/2026/truchet-tiles-800x400_2x.png 800w" type=image/png>'
            '<img alt="Geometrically-drawn tiles in red and black" '
            'style="aspect-ratio: 2" '
            "src=/images/2026/truchet-tiles-800x400_1x.png width=400></picture>"
        )

        for name in (
            "truchet-tiles-800x400_1x.avif",
            "truchet-tiles-800x400_2x.avif",
            "truchet-tiles-800x400_1x.webp",
            "truchet-tiles-800x400_2x.webp",
            "truchet-tiles-800x400_1x.png",
            "truchet-tiles-800x400_2x.png",
        ):
            assert (out_dir / "images/2026" / name).exists()

    def test_render_picture_based_on_height(
        self, src_dir: Path, env: Environment
    ) -> None:
        """
        Picking an equivalent target width/height returns the same HTML.
        """
        (src_dir / "_images").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/truchet-tiles-800x400.png",
        )

        md_width = (
            '{% picture filename="truchet-tiles-800x400.png" width="400" '
            'parent="/images/" %}'
        )
        md_height = (
            '{% picture filename="truchet-tiles-800x400.png" height="200" '
            'parent="/images/" %}'
        )

        html_width = env.from_string(md_width).render()
        html_height = env.from_string(md_height).render()
        assert html_width == html_height

    def test_render_picture_for_page_without_date(
        self, src_dir: Path, out_dir: Path, env: Environment
    ) -> None:
        """
        Test a picture on a page without a date.
        """
        (src_dir / "_images").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/truchet-tiles-800x400.png",
        )
        page = StubPage(date=None)

        md = '{% picture filename="truchet-tiles-800x400.png" width="400" %}'

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            "<picture>"
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/truchet-tiles-800x400_1x.avif 400w,'
            '/images/truchet-tiles-800x400_2x.avif 800w" '
            "type=image/avif>"
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/truchet-tiles-800x400_1x.webp 400w,'
            '/images/truchet-tiles-800x400_2x.webp 800w" '
            'type=image/webp><source sizes="(max-width: 400px) 100vw, '
            '400px" srcset="/images/truchet-tiles-800x400_1x.png 400w,'
            '/images/truchet-tiles-800x400_2x.png 800w" type=image/png>'
            '<img style="aspect-ratio: 2" '
            "src=/images/truchet-tiles-800x400_1x.png width=400></picture>"
        )

        for name in (
            "truchet-tiles-800x400_1x.avif",
            "truchet-tiles-800x400_2x.avif",
            "truchet-tiles-800x400_1x.webp",
            "truchet-tiles-800x400_2x.webp",
            "truchet-tiles-800x400_1x.png",
            "truchet-tiles-800x400_2x.png",
        ):
            assert (out_dir / "images" / name).exists()

    def test_render_not_found_picture(self, env: Environment) -> None:
        """
        Rendering a picture that doesn't exist throws a FileNotFoundError.
        """
        page = StubPage(date=datetime.now())
        md = '{% picture filename="doesnotexist.png" width="100" %}'

        with pytest.raises(FileNotFoundError):
            env.from_string(md).render(page=page)

    def test_unregcognised_image_format(self, src_dir: Path, env: Environment) -> None:
        """
        Rendering a picture with an unrecognised format is an error.
        """
        (src_dir / "_images").mkdir(parents=True)
        (src_dir / "_images/greeting.txt").write_text("hello world")

        page = StubPage(date=None)
        md = '{% picture filename="greeting.txt" width="100" %}'

        with pytest.raises(UnidentifiedImageError):
            env.from_string(md).render(page=page)

    def test_only_original_for_png_screenshot(
        self, src_dir: Path, env: Environment
    ) -> None:
        """
        If the image is a PNG screenshot, there's only a PNG derivative.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles-800x400.png",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% picture filename="truchet-tiles-800x400.png" width="400" '
            'class="screenshot" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            "<picture>"
            '<source sizes="(max-width: 400px) 100vw, '
            '400px" srcset="/images/2026/truchet-tiles-800x400_1x.png 400w,'
            '/images/2026/truchet-tiles-800x400_2x.png 800w" type=image/png>'
            '<img style="aspect-ratio: 2" class=screenshot '
            "src=/images/2026/truchet-tiles-800x400_1x.png width=400></picture>"
        )

    def test_only_original_for_jpg_screenshot(
        self, src_dir: Path, env: Environment
    ) -> None:
        """
        If the image is a JPEG screenshot, there's only a JPEG derivative.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/palymyra-500x525.jpg",
            src_dir / "_images/2026/palymyra-500x525.jpg",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% picture filename="palymyra-500x525.jpg" '
            'width="250" class="screenshot" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            "<picture>"
            '<source sizes="(max-width: 250px) 100vw, 250px" '
            'srcset="/images/2026/palymyra-500x525_1x.jpg 250w,'
            '/images/2026/palymyra-500x525_2x.jpg 500w" type=image/jpeg>'
            '<img style="aspect-ratio: 20/21" class=screenshot '
            "src=/images/2026/palymyra-500x525_1x.jpg width=250></picture>"
        )

    def test_link_to_original(self, src_dir: Path, env: Environment) -> None:
        """
        An image can link to the original version.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles-800x400.png",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% picture filename="truchet-tiles-800x400.png" width="400" '
            'link_to="original" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        assert html.startswith('<a href="/images/2026/truchet-tiles-800x400.png">')
        assert html.endswith("</a>")

    def test_link_to_other_page(self, src_dir: Path, env: Environment) -> None:
        """
        An image can link to a different page.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles-800x400.png",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% picture filename="truchet-tiles-800x400.png" width="400" '
            'link_to="https://example.com" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        assert html.startswith('<a href="https://example.com"')
        assert html.endswith("</a>")

    def test_render_jpeg(self, src_dir: Path, out_dir: Path, env: Environment) -> None:
        """
        Test when the source image is a JPEG.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/palymyra-500x525.jpg",
            src_dir / "_images/2026/palymyra-500x525.jpg",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = '{% picture filename="palymyra-500x525.jpg" width="250" %}'

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            "<picture>"
            '<source sizes="(max-width: 250px) 100vw, 250px" '
            'srcset="/images/2026/palymyra-500x525_1x.avif 250w,'
            '/images/2026/palymyra-500x525_2x.avif 500w" '
            "type=image/avif>"
            '<source sizes="(max-width: 250px) 100vw, 250px" '
            'srcset="/images/2026/palymyra-500x525_1x.webp 250w,'
            '/images/2026/palymyra-500x525_2x.webp 500w" '
            'type=image/webp><source sizes="(max-width: 250px) 100vw, 250px" '
            'srcset="/images/2026/palymyra-500x525_1x.jpg 250w,'
            '/images/2026/palymyra-500x525_2x.jpg 500w" type=image/jpeg>'
            '<img style="aspect-ratio: 20/21" '
            "src=/images/2026/palymyra-500x525_1x.jpg width=250></picture>"
        )

    def test_dark_mode(self, src_dir: Path, out_dir: Path, env: Environment) -> None:
        """
        Test a picture with light and dark variants.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles-800x400.png",
        )
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.dark.png",
            src_dir / "_images/2026/truchet-tiles-800x400.dark.png",
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = '{% picture filename="truchet-tiles-800x400.png" width="400" %}'

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            "<picture>"
            '<source media="(prefers-color-scheme: dark)" '
            'sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400.dark_1x.avif 400w,'
            '/images/2026/truchet-tiles-800x400.dark_2x.avif 800w" type=image/avif>'
            '<source media="(prefers-color-scheme: dark)" '
            'sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400.dark_1x.webp 400w,'
            '/images/2026/truchet-tiles-800x400.dark_2x.webp 800w" type=image/webp>'
            '<source media="(prefers-color-scheme: dark)" '
            'sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400.dark_1x.png 400w,'
            '/images/2026/truchet-tiles-800x400.dark_2x.png 800w" type=image/png>'
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400_1x.avif 400w,'
            '/images/2026/truchet-tiles-800x400_2x.avif 800w" type=image/avif>'
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400_1x.webp 400w,'
            '/images/2026/truchet-tiles-800x400_2x.webp 800w" type=image/webp>'
            '<source sizes="(max-width: 400px) 100vw, 400px" '
            'srcset="/images/2026/truchet-tiles-800x400_1x.png 400w,'
            '/images/2026/truchet-tiles-800x400_2x.png 800w" type=image/png>'
            '<img style="aspect-ratio: 2" class=dark_aware '
            "src=/images/2026/truchet-tiles-800x400_1x.png width=400></picture>"
        )

        for name in (
            "truchet-tiles-800x400_1x.avif",
            "truchet-tiles-800x400_2x.avif",
            "truchet-tiles-800x400_1x.webp",
            "truchet-tiles-800x400_2x.webp",
            "truchet-tiles-800x400_1x.png",
            "truchet-tiles-800x400_2x.png",
            "truchet-tiles-800x400.dark_1x.avif",
            "truchet-tiles-800x400.dark_2x.avif",
            "truchet-tiles-800x400.dark_1x.webp",
            "truchet-tiles-800x400.dark_2x.webp",
            "truchet-tiles-800x400.dark_1x.png",
            "truchet-tiles-800x400.dark_2x.png",
        ):
            assert (out_dir / "images/2026" / name).exists()


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
        actual = tp.choose_target_width(
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
        actual = tp.choose_target_width(
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
            tp.choose_target_width(
                src_path=self.fixtures_dir / "truchet-tiles-800x400.png",
                target_width=None,
                target_height=None,
            )

    def test_both_dimensions_is_error(self) -> None:
        """
        Supplying both dimensions is a TypeError.
        """
        with pytest.raises(TypeError):
            tp.choose_target_width(
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
            tp.choose_target_width(
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
            tp.choose_target_width(
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
        width = tp.choose_target_width(
            src_path=Path("src/_images/2021/your-computer-is-on-fire.jpg"),
            target_width=None,
            target_height=140,
        )

        assert width == 109
