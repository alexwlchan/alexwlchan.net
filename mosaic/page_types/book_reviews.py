"""
Models for book reviews.
"""

from pathlib import Path
from typing import Self

from pydantic import model_validator

from mosaic.models import (
    BookInfo,
    BookReview as ReviewInfo,
    BreadcrumbEntry,
    book_attribution,
)
from .posts import Post


class BookReview(Post):
    """
    A book review is my notes on a book I've read.
    """

    template_name: str = "book_review.html"

    # Information about the book itself
    book: BookInfo

    # Information about my review and opinions
    review: ReviewInfo

    @property
    def attribution_line(self) -> str:
        """
        Returns the one-line attribution based on the contributor.
        """
        return book_attribution(contributors=self.book.contributors)

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/book-reviews/{self.slug}/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="books I've read", href="/book-reviews/"),
        ]

    @model_validator(mode="after")
    def set_title(self) -> Self:
        """
        Set a title for this review, of the form "[title], [attribution]".

        For example: "Dethroned in Knightsbridge, by Silvia Lemos"
        """
        self.title = f"{self.book.title}, {self.attribution_line}"
        return self

    @property
    def cover_image(self) -> Path:
        """
        The cover image of this book.
        """
        matching_paths = [
            p
            for p in (
                self.src_dir / "images" / str(self.review.date_read.year)
            ).iterdir()
            if p.stem == self.md_path.stem
        ]

        assert len(matching_paths) == 1, matching_paths

        return matching_paths[0]
