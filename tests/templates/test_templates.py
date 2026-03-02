"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic.page_types import BaseHtmlPage, Page
from mosaic.templates import absolute_url, filter_for_topic


@pytest.mark.parametrize(
    "path, url",
    [("/", "https://alexwlchan.net/"), ("example", "https://alexwlchan.net/example")],
)
def test_absolute_url(path: str, url: str) -> None:
    """
    Tests for `absolute_url`.
    """
    assert absolute_url(path) == url


def test_filter_for_topic() -> None:
    """
    Filtering by topic looks at the topic on a page, and all parent topics.
    """
    page1 = Page(url="/page1/")
    page2 = Page(url="/page2/", topics=["Python"])
    page3 = Page(url="/page3/", topics=["Systems and software"])
    page4 = Page(url="/page4/", topics=["Art and creativity", "Python"])
    page5 = Page(url="/page5/", topics=["Generative art", "Interesting words"])

    pages: list[BaseHtmlPage] = [page1, page2, page3, page4, page5]

    assert filter_for_topic(pages, topic_name="Python") == [page2, page4]
    assert filter_for_topic(pages, topic_name="Systems and software") == [
        page2,
        page3,
        page4,
    ]
    assert filter_for_topic(pages, topic_name="Art and creativity") == [page4, page5]
