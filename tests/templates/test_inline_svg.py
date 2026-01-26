"""
Tests for `mosaic.templates.inline_svg`.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from jinja2 import Environment
import pytest


@dataclass
class StubPage:
    """Stub entry for a page."""

    date: datetime | None = None


class TestInlineSvgExtension:
    """
    Tests for InlineSvgExtension.
    """

    def test_render_inline_svg(self, src_dir: Path, env: Environment) -> None:
        """
        Test the basic usage of the {% inline_svg %} tag.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        (src_dir / "_images/2026/example.svg").write_text(
            '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            '  <rect width="200" height="200" fill="yellow"/>\n'
            "</svg>"
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = '{% inline_svg filename="example.svg" alt="A yellow rectangle" %}'

        html = env.from_string(md).render(page=page).strip()
        assert html == (
            '<svg aria-labelledby="svg_example" role="img" '
            'viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">'
            '<title id="svg_example">A yellow rectangle</title>\n'
            '<rect fill="yellow" height="200" width="200"/>\n</svg>'
        )

    def test_link_multiple_svgs_in_same_page(
        self, src_dir: Path, out_dir: Path, env: Environment
    ) -> None:
        """
        You can have multiple SVGs in a page which all link to the original.
        """
        (src_dir / "_images/2026").mkdir(parents=True)

        for colour in ("red", "green", "blue"):
            (src_dir / f"_images/2026/rect_{colour}.svg").write_text(
                f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
                f'  <rect width="200" height="200" fill="{colour}"/>\n'
                f"</svg>"
            )

        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% inline_svg filename="rect_red.svg"   link_to="original" %}\n'
            '{% inline_svg filename="rect_green.svg" link_to="original" %}\n'
            '{% inline_svg filename="rect_blue.svg"  link_to="original" %}\n'
        )

        html = env.from_string(md).render(page=page).strip()
        assert html == (
            '<a href="/images/2026/rect_red.svg">'
            '<svg role="img" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            '<rect fill="red" height="200" width="200"/>\n</svg></a>'
            '<a href="/images/2026/rect_green.svg">'
            '<svg role="img" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            '<rect fill="green" height="200" width="200"/>\n</svg></a>'
            '<a href="/images/2026/rect_blue.svg">'
            '<svg role="img" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            '<rect fill="blue" height="200" width="200"/>\n</svg></a>'
        )

        for f in ("rect_red.svg", "rect_green.svg", "rect_blue.svg"):
            assert (out_dir / "images/2026" / f).exists()

    def test_adds_extra_attributes(self, src_dir: Path, env: Environment) -> None:
        """
        Extra attributes are added dirctly to the <svg>.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        (src_dir / "_images/2026/example.svg").write_text(
            '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            '  <rect width="200" height="200" fill="yellow"/>\n'
            "</svg>"
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = (
            '{% inline_svg filename="example.svg" alt="A yellow rectangle" '
            'class="dark_aware" data_colour="yellow" %}'
        )

        html = env.from_string(md).render(page=page).strip()
        assert html == (
            '<svg aria-labelledby="svg_example" class="dark_aware" '
            'data_colour="yellow" role="img" viewBox="0 0 200 200" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<title id="svg_example">A yellow rectangle</title>\n'
            '<rect fill="yellow" height="200" width="200"/>\n</svg>'
        )

    def test_comments_are_removed(self, src_dir: Path, env: Environment) -> None:
        """
        Comments in the original SVG are removed.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        (src_dir / "_images/2026/example.svg").write_text(
            '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            '  <rect width="200" height="200" fill="blue"/>\n'
            "  <!-- This is a comment -->"
            '  <rect width="200" height="200" fill="yellow"/>\n'
            "</svg>"
        )
        page = StubPage(date=datetime(2026, 1, 1))

        md = '{% inline_svg filename="example.svg" alt="A yellow rectangle" %}'

        html = env.from_string(md).render(page=page).strip()
        assert html == (
            '<svg aria-labelledby="svg_example" role="img" '
            'viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">'
            '<title id="svg_example">A yellow rectangle</title>\n'
            '<rect fill="blue" height="200" width="200"/>'
            '<rect fill="yellow" height="200" width="200"/>\n</svg>'
        )

    def test_non_svg_is_error(self, env: Environment) -> None:
        """
        Using a non-SVG filename is an error.
        """
        page = StubPage()
        md = '{% inline_svg filename="rect_red.png" %}\n'

        with pytest.raises(ValueError):
            env.from_string(md).render(page=page)

    def test_missing_svg_tag_is_error(self, src_dir: Path, env: Environment) -> None:
        """
        Using an SVG file which doesn't contain an <svg> is an error.
        """
        (src_dir / "_images/2026").mkdir(parents=True)
        (src_dir / "_images/2026/example.svg").write_text("Hello world!")

        page = StubPage(date=datetime(2026, 1, 1))
        md = '{% inline_svg filename="example.svg" %}\n'

        with pytest.raises(ValueError, match="No <svg> tag found"):
            env.from_string(md).render(page=page)
