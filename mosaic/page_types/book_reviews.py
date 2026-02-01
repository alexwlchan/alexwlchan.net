"""
Models for book reviews.
"""

from datetime import date
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator

from ._base import BaseHtmlPage, BreadcrumbEntry


class BookContributor(BaseModel):
    """
    Somebody who contributed to a book.
    """

    name: str
    role: str = "author"


class BookInfo(BaseModel):
    """
    Information about a book. This describes the book in the abstract,
    and doesn't tell you anything about how I read it.
    """

    title: str
    contributors: list[BookContributor]
    genres: list[str]
    publication_year: int
    isbn13: str = ""


class ReviewInfo(BaseModel):
    """
    Information about the review; when I read the book.
    """

    date_read: date
    format: Literal["audiobook", "paperback", "hardback", "ebook", "pamphlet", "zine"]
    rating: int = 0
    summary: str = ""
    did_not_finish: bool = False


class BookReview(BaseHtmlPage):
    """
    A book review is my notes on a book I've read.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a BookReview.
    md_path: Path
    src_dir: Path

    # Information about the book itself
    book: BookInfo

    # Information about my review and opinions
    review: ReviewInfo

    @property
    def attribution_line(self) -> str:
        """
        Returns the one-line attribution based on the contributor.
        """
        return attribution_line(contributors=self.book.contributors)

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        return "book_review.html"

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
                self.src_dir / "_images" / str(self.review.date_read.year)
            ).iterdir()
            if p.stem == self.md_path.stem
        ]

        assert len(matching_paths) == 1, matching_paths

        return matching_paths[0]


def attribution_line(contributors: list[BookContributor]) -> str:
    """
    Choose the one-line attribution for this book, used in the list of reviews.
    """
    contributors = [
        c
        for c in contributors
        if c.role not in {"illustrator", "narrator", "translator"}
    ]

    if len(contributors) == 1 and contributors[0].role == "author":
        author = contributors[0]
        return f"by {author.name}"
    if len(contributors) == 1 and contributors[0].role == "retold by":
        author = contributors[0]
        return f"retold by {author.name}"
    elif len(contributors) == 1 and contributors[0].role == "editor":
        editor = contributors[0]
        return f"edited by {editor.name}"
    elif (
        len(contributors) == 2
        and contributors[0].role == "author"
        and contributors[1].role == "editor"
    ):
        author = contributors[0]
        return f"by {author.name}"
    else:  # pragma: no cover
        raise ValueError(f"unable to choose attribution for book: {contributors}")
