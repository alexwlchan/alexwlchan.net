"""
Models for notes.
"""

from datetime import datetime
from pathlib import Path
from typing import Self

from pydantic import model_validator

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

    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        if not self.topics:
            raise ValueError(f"no topics in {self.md_path}")
        return [
            BreadcrumbEntry(label=t.name, href=t.href)
            for t in get_topic_by_name(self.topics[0]).breadcrumb
        ]

    @model_validator(mode="after")
    def check_md_path(self) -> Self:
        """
        Notes should be saved in the per-year subfolder of `notes`.
        """
        expected_filename = self.date.strftime("%Y-%m-%d-") + self.slug + ".md"
        expected_path = self.src_dir / "notes" / str(self.date.year) / expected_filename

        if self.md_path != expected_path:
            raise ValueError(
                f"wrong path: expected {expected_path!r}, got {self.md_path!r}"
            )

        return self
