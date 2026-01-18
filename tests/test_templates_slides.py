"""
Tests for `mosaic.templates.slides`.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil

import minify_html
from jinja2 import Environment


@dataclass
class StubPage:
    """Stub entry for a page."""

    date: datetime | None
    slug: str


class TestSlideExtension:
    """
    Tests for SlideExtension.
    """

    def test_render_slide(self, src_dir: Path, out_dir: Path, env: Environment) -> None:
        """
        Test the basic usage of the {% slide %} tag.
        """
        (src_dir / "_images/2026/truchet-tiles").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles/slide1-800x400.png",
        )
        page = StubPage(date=datetime(2026, 1, 1), slug="truchet-tiles")

        md = '{% slide filename="slide1-800x400.png" alt="Title slide" %}'

        html = env.from_string(md).render(page=page).strip()
        assert minify_html.minify(html) == (
            '<style type=x-text/scss>@use "components/slides";</style>'
            "<figure class=slide>"
            "<a href=/images/2026/truchet-tiles/slide1-800x400.png>"
            "<picture>"
            '<source sizes="(max-width: 450px) 100vw, 450px" '
            'srcset="/images/2026/truchet-tiles/slide1-800x400_1x.avif 450w" '
            "type=image/avif>"
            '<source sizes="(max-width: 450px) 100vw, 450px" '
            'srcset="/images/2026/truchet-tiles/slide1-800x400_1x.webp 450w" '
            "type=image/webp>"
            '<source sizes="(max-width: 450px) 100vw, 450px" '
            'srcset="/images/2026/truchet-tiles/slide1-800x400_1x.png 450w" '
            "type=image/png>"
            '<img alt="Title slide" style="aspect-ratio: 2" loading=lazy '
            "src=/images/2026/truchet-tiles/slide1-800x400_1x.png width=450>"
            "</picture></a></figure>"
        )

    def test_slide_with_caption(
        self, src_dir: Path, out_dir: Path, env: Environment
    ) -> None:
        """
        Test a slide which includes a caption.
        """
        (src_dir / "_images/2026/truchet-tiles").mkdir(parents=True)
        shutil.copyfile(
            "tests/fixtures/truchet-tiles-800x400.png",
            src_dir / "_images/2026/truchet-tiles/slide1-800x400.png",
        )
        page = StubPage(date=datetime(2026, 1, 1), slug="truchet-tiles")

        md = (
            '{% slide filename="slide1-800x400.png" alt="Title slide" '
            'caption="This caption has **bold** text" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        figcaption_html = (
            "<figcaption>"
            "<p>This caption has <strong>bold</strong> text</p>"
            "</figcaption>"
        )
        assert figcaption_html in html
