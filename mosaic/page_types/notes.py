"""
Models for notes.
"""

from datetime import datetime
from pathlib import Path

from mosaic.topics import get_topic_by_name

from ._base import BaseHtmlPage, BreadcrumbEntry


class Note(BaseHtmlPage):
    """
    A note is a short-form piece of writing, something often without
    original thought, just meant as a reference.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a BookReview.
    md_path: Path
    src_dir: Path
    date: datetime
    topic: str

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        return "note.html"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        assert self.md_path.name != "index.md"
        relative_dir = self.md_path.parent.relative_to(self.src_dir)
        return f"/{relative_dir}/{self.slug}/".replace("./", "")

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label=t.name, href=t.href)
            for t in get_topic_by_name(self.topic).breadcrumb
        ]


class TodayILearned(BaseHtmlPage):
    """
    A TIL is a short-form piece of writing, something often without
    original thought, just meant as a reference.

    TODO: Replace these with notes.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a BookReview.
    md_path: Path
    src_dir: Path
    date: datetime

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        return "til.html"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/til/{self.date.year}/{self.slug}/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [BreadcrumbEntry(label="today I learned", href="/til/")]
