"""
Models for articles.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Self

from pydantic import model_validator

from mosaic.topics import get_topic_by_name

from ._base import BaseHtmlPage, BreadcrumbEntry


class Article(BaseHtmlPage):
    """
    An article is a long-form piece of writing, usually with original thought.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a BookReview.
    md_path: Path
    src_dir: Path
    date: datetime

    # What order is this in the list of all articles?
    order: int = -1

    # The short filename for this card, used on /articles/ to reduce page
    # weight. For example, "dominant-colours" might become "do".
    card_short_name: str | None = None

    def __hash__(self) -> int:
        """
        Return a hash; this is so I can use articles as dict keys when
        working out the short names for cards.
        """
        return hash(repr(self))

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        return "article.html"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/{self.date.year}/{self.slug}/"

    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        if self.topics:
            return [
                BreadcrumbEntry(label=t.name, href=t.href)
                for t in get_topic_by_name(self.topics[0]).breadcrumb
            ]
        else:
            return [BreadcrumbEntry(label="articles", href="/articles/")]

    @property
    def is_new(self) -> bool:
        """
        Returns True if this page was published recently, False otherwise.
        """
        return (datetime.now(tz=timezone.utc) - self.date).days <= 21

    @model_validator(mode="after")
    def check_md_path(self) -> Self:
        """
        Articles should be saved in the per-year subfolder of `_articles`.
        """
        expected_filename = self.date.strftime("%Y-%m-%d-") + self.slug + ".md"
        expected_path = (
            self.src_dir / "_articles" / str(self.date.year) / expected_filename
        )

        if self.md_path != expected_path:
            raise ValueError(
                f"wrong path: expected {expected_path!r}, got {self.md_path!r}"
            )

        return self
