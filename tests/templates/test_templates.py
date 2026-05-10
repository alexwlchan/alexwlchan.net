"""
Tests for `mosaic.templates`.
"""

from datetime import datetime
from pathlib import Path
import uuid

import pytest

from mosaic.page_types import BaseHtmlPage, BreadcrumbEntry, Page, Post
from mosaic.templates import (
    absolute_url,
    filter_for_topic,
    group_list_of_posts,
    naturalsize,
)


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


class TestGroupListOfPosts:
    """
    Tests for `group_list_of_posts`.
    """

    @staticmethod
    def create_post(is_featured: bool = False, is_excluded: bool = False) -> Post:
        """
        Create a post.
        """

        class PostStub(Post):
            @property
            def url(self) -> str:  # pragma: no cover
                raise NotImplementedError

            @property
            def breadcrumb(self) -> list[BreadcrumbEntry]:  # pragma: no cover
                raise NotImplementedError

        return PostStub(
            md_path=Path(f"{uuid.uuid4()}.md"),
            src_dir=Path("src"),
            date=datetime.now(),
            template_name="stub.html",
            is_featured=is_featured,
            is_excluded=is_excluded,
        )

    @pytest.mark.parametrize(
        "featured",
        [
            [True, True, True],
            [True, True, True, True],
            [False, False, False, True, True, False],
        ],
    )
    def test_groups_remaining_posts(self, featured: list[bool]) -> None:
        """
        After doing the first pass, if all the leftover posts are remaining,
        they get merged with the final group.
        """
        # This is a regression test for a bug on the /images-and-videos/
        # page, where two 'remaining' posts were leftover and separated
        # from the rest of the group.
        posts = [self.create_post(is_featured=f) for f in featured]

        groups = list(group_list_of_posts(posts))

        for i in range(len(groups) - 1):
            assert groups[i]["type"] != groups[i + 1]["type"], featured
