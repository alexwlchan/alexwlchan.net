"""
Tests for `mosaic.templates.downloads`.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from jinja2 import Environment
import minify_html
import pytest

from mosaic import templates as t


@dataclass
class StubPage:
    """Stub entry for a page."""

    date: datetime | None


class TestDownloadExtension:
    """
    Tests for DownloadExtension.
    """

    def test_render_download(self, out_dir: Path) -> None:
        """
        Test the basic usage of the {% download %} tag.
        """
        env = t.get_jinja_environment(src_dir=Path("src"), out_dir=out_dir)

        page = StubPage(date=datetime(2026, 1, 1))

        md = '{% download filename="example.zip" %}'

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            '<style type=x-text/scss>@use "components/download";</style>'
            "<a class=download href=/files/2026/example.zip>"
            "<picture>"
            '<source sizes="(max-width: 64px) 100vw, 64px" '
            'srcset="/images/icons/download_zip_1x.avif 64w,'
            "/images/icons/download_zip_2x.avif 128w,"
            '/images/icons/download_zip_3x.avif 192w" type=image/avif>'
            '<source sizes="(max-width: 64px) 100vw, 64px" '
            'srcset="/images/icons/download_zip_1x.webp 64w,'
            "/images/icons/download_zip_2x.webp 128w,"
            '/images/icons/download_zip_3x.webp 192w" type=image/webp>'
            '<source sizes="(max-width: 64px) 100vw, 64px" '
            'srcset="/images/icons/download_zip_1x.png 64w,'
            "/images/icons/download_zip_2x.png 128w,"
            '/images/icons/download_zip_3x.png 192w" type=image/png>'
            '<img style="aspect-ratio: 1" alt data-proofer-ignore '
            "src=/images/icons/download_zip_1x.png width=64>"
            "</picture> example.zip</a>"
        )

    @pytest.mark.parametrize(
        "filename", ["example.zip", "example.py", "example.rb", "example.js"]
    )
    def test_render_different_file_types(self, out_dir: Path, filename: str) -> None:
        """
        Test different file extensions with the {% download %} tag.
        """
        env = t.get_jinja_environment(src_dir=Path("src"), out_dir=out_dir)

        page = StubPage(date=datetime(2026, 1, 1))

        md = '{% download filename="' + filename + '" %}'

        html = env.from_string(md).render(page=page).strip()
        assert filename in html

    def test_unrecognised_file_type_is_error(self, env: Environment) -> None:
        """
        You can't use download with an unrecognised file extension.
        """
        md = '{% download filename="mystery.xyz" %}'

        with pytest.raises(ValueError):
            env.from_string(md).render().strip()
