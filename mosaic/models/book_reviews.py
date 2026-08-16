"""
Models for books and book reviews.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel


__all__ = ["BookContributor", "BookInfo", "BookReview", "book_attribution"]


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


class BookReview(BaseModel):
    """
    Information about the review; when I read the book.
    """

    date_read: date
    format: Literal["audiobook", "paperback", "hardback", "ebook", "pamphlet", "zine"]
    rating: int = 0
    summary: str = ""
    did_not_finish: bool = False
    from_the_library: bool = False


def book_attribution(contributors: list[BookContributor]) -> str:
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
    if len(contributors) == 1 and contributors[0].role == "compiled by":
        compiler = contributors[0]
        return f"compiled by {compiler.name}"
    if len(contributors) == 1 and contributors[0].role == "editor":
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
