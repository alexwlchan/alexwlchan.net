"""
Tests for `mosaic.templates`.
"""

from jinja2 import Environment
import pytest

from mosaic.page_types import Page


@pytest.mark.parametrize(
    "title_md, title_html",
    [
        ("", "alexwlchan"),
        ("alexwlchan", "alexwlchan"),
        ("Hello world", "Hello world – alexwlchan"),
        ("Hello *world*", "Hello world – alexwlchan"),
        ("Hello <em>world</em>", "Hello world – alexwlchan"),
    ],
)
def test_title_element(env: Environment, title_md: str, title_html: str) -> None:
    """
    Check the <title> element renders correctly.

    This means:

    *   A suffix `– alexwlchan` is added if the title is non-trivial
    *   Markdown or HTML tags are stripped out

    """
    p = Page(url="/example/", title=title_md, content="This is my page")

    html = p.render_full_html(env)

    assert f"<title>{title_html}</title>" in html
