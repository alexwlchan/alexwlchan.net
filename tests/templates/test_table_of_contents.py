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
            "Some text under the heading\n"
            "### Subheading 1\n"
            "### Subheading 2\n\n"
            "## My second heading"
        )

        html = env.from_string(md).render(page=StubPage(content=md)).strip()
        assert minify_html.minify(html) == (
            "<link href=css/components/table_of_contents.css rel=stylesheet>"
            "<nav aria-labelledby=toc-heading class=table_of_contents>"
            "<h3 id=toc-heading>Table of contents</h3>"
            "<ul><li>"
            "<a href=#my-first-heading>My first heading</a>"
            "<ul><li><a href=#subheading-1>Subheading 1</a>"
            "<li><a href=#subheading-2>Subheading 2</a></ul>"
            "<li><a href=#my-second-heading>My second heading</a>"
            "</ul></nav> "
            "## My first heading "
            "Some text under the heading "
            "### Subheading 1 "
            "### Subheading 2 "
            "## My second heading"
        )

    def test_render_toc_with_explicit_ids(self, env: Environment) -> None:
        """
        Test a table of contents where each heading has an explicit ID.
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
            "<link href=css/components/table_of_contents.css rel=stylesheet>"
            "<nav aria-labelledby=toc-heading class=table_of_contents>"
            "<h3 id=toc-heading>Table of contents</h3>"
            "<ul><li><a href=#heading1>My first heading</a>"
            "<ul><li><a href=#subheading1a>Subheading 1</a>"
            "<li><a href=#subheading1b>Subheading 2</a></ul>"
            "<li><a href=#heading2>My second heading</a></ul>"
            "</nav>"
            "<h2 id=heading1>My first heading</h2>"
            "<h3 id=subheading1a>Subheading 1</h3>"
            "<h3 id=subheading1b>Subheading 2</h3>"
            "<h2 id=heading2>My second heading</h2>"
        )

    def test_toc_with_inline_tags(self, env: Environment) -> None:
        """
        Test a table of contents where a heading includes markup.
        """
        md = (
            "{% table_of_contents %}\n"
            "\n"
            "## My first heading\n"
            "### This heading has `code` formatting\n"
            "### This heading has *emphasis*\n"
        )

        html = env.from_string(md).render(page=StubPage(content=md)).strip()
        assert minify_html.minify(html) == (
            "<link href=css/components/table_of_contents.css rel=stylesheet>"
            "<nav aria-labelledby=toc-heading class=table_of_contents>"
            "<h3 id=toc-heading>Table of contents</h3>"
            "<ul><li><a href=#my-first-heading>My first heading</a>"
            "<ul>"
            "<li><a href=#this-heading-has-code-code-code-formatting>"
            # "This heading has <code>code</code> formatting</a></ul>"
            "This heading has code formatting</a>"
            "<li><a href=#this-heading-has-em-emphasis-em>"
            # "This heading has <em>emphasis</em></a></ul>"
            "This heading has emphasis</a></ul></ul>"
            "</nav> "
            "## My first heading "
            "### This heading has `code` formatting "
            "### This heading has *emphasis*"
        )
