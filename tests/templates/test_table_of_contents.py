"""
Tests for `mosaic.templates.table_of_contents`.
"""

from dataclasses import dataclass

import minify_html
from jinja2 import Environment


@dataclass
class StubPage:
    """Stub entry for a page."""

    content: str


class TestTableOfContentsExtension:
    """
    Tests for TableOfContentsExtension.
    """

    def test_render_toc(self, env: Environment) -> None:
        """
        Test the basic usage of the {% table_of_contents %} tag.
        """
        md = (
            "{% table_of_contents %}\n"
            "\n"
            "## My first heading\n"
            "### Subheading 1\n"
            "### Subheading 2\n\n"
            "## My second heading"
        )

        html = env.from_string(md).render(page=StubPage(content=md)).strip()
        assert minify_html.minify(html) == (
            '<style type=x-text/scss>@use "components/table_of_contents";</style>'
            "<blockquote class=table_of_contents>"
            "<h3>Table of contents</h3>"
            "<ul><li>"
            "<a href=#my-first-heading>My first heading</a> "
            "<ul><li><a href=#subheading-1>Subheading 1</a>"
            "<li><a href=#subheading-2>Subheading 2</a></ul>"
            "<li><a href=#my-second-heading>My second heading</a>"
            "</ul></blockquote> "
            "## My first heading "
            "### Subheading 1 "
            "### Subheading 2 "
            "## My second heading"
        )

    def test_render_toc_with_explicit_ids(self, env: Environment) -> None:
        """
        Test the basic usage of the {% table_of_contents %} tag.
        """
        md = (
            "{% table_of_contents %}\n"
            "\n"
            '<h2 id="heading1">My first heading</h2>\n'
            '<h3 id="subheading1a">Subheading 1</h3>\n'
            '<h3 id="subheading1b">Subheading 2</h3>\n\n'
            '<h2 id="heading2">My second heading</h2>'
        )

        html = env.from_string(md).render(page=StubPage(content=md)).strip()
        assert minify_html.minify(html) == (
            '<style type=x-text/scss>@use "components/table_of_contents";</style>'
            "<blockquote class=table_of_contents>"
            "<h3>Table of contents</h3>"
            "<ul><li><a href=#heading1>My first heading</a> "
            "<ul><li><a href=#subheading1a>Subheading 1</a>"
            "<li><a href=#subheading1b>Subheading 2</a></ul>"
            "<li><a href=#heading2>My second heading</a></ul>"
            "</blockquote>"
            "<h2 id=heading1>My first heading</h2>"
            "<h3 id=subheading1a>Subheading 1</h3>"
            "<h3 id=subheading1b>Subheading 2</h3>"
            "<h2 id=heading2>My second heading</h2>"
        )
