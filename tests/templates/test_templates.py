"""
Tests for `mosaic.templates`.
"""

from jinja2 import Environment
import pytest

from mosaic.page_types import BaseHtmlPage, Page
from mosaic.templates import filter_for_topic


def test_filter_for_topic() -> None:
    """
    Filtering by topic looks at the topic on a page, and all parent topics.
    """
    page1 = Page(url="/page1/")
    page2 = Page(url="/page2/", topics=["Python"])
    page3 = Page(url="/page3/", topics=["Computers and code"])
    page4 = Page(url="/page4/", topics=["Art and creativity", "Python"])
    page5 = Page(url="/page5/", topics=["Generative art", "Interesting words"])

    pages: list[BaseHtmlPage] = [page1, page2, page3, page4, page5]

    assert filter_for_topic(pages, topic_name="Python") == [page2, page4]
    assert filter_for_topic(pages, topic_name="Computers and code") == [
        page2,
        page3,
        page4,
    ]
    assert filter_for_topic(pages, topic_name="Art and creativity") == [page4, page5]


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
