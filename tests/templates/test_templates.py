"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic.page_types import BaseHtmlPage, Page
from mosaic.templates import absolute_url, filter_for_topic, naturalsize


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
    "size, expected",
    [
        (1, "1 byte"),
        (999, "999 bytes"),
        (1024, "1.0 kB"),
        (1234567, "1.2 MB"),
        (1234567890, "1.2 GB"),
        (123456789012345678901234567890, "123456.8 YB"),
    ],
)
def test_naturalsize(size: int, expected: str) -> None:
    """
    Tests for `naturalsize`.
    """
    assert naturalsize(size) == expected
