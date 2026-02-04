"""
Tests for `mosaic.page_types.book_reviews`.
"""

from datetime import date, datetime
from pathlib import Path

import pytest

from mosaic import page_types
from mosaic.page_types.book_reviews import (
    BookContributor,
    BookInfo,
    ReviewInfo,
    attribution_line,
)


def test_book_review_properties(src_dir: Path) -> None:
    """
    Test the `BookReview` page type.
    """
    (src_dir / "_images/2001").mkdir(parents=True)
    (src_dir / "_images/2001/ship-happens.jpg").write_text("JPEG;placeholder")

    review = page_types.BookReview(
        md_path=src_dir / "book_reviews/2001/ship-happens.md",
        src_dir=src_dir,
        date=datetime(2001, 2, 3),
        book=BookInfo(
            title="Ship Happens",
            contributors=[BookContributor(name="James T. Kink")],
            genres=["fiction", "sci-fi"],
            publication_year=1963,
        ),
        review=ReviewInfo(date_read=date(2001, 2, 3), format="paperback", rating=4),
    )

    assert review.title == "Ship Happens, by James T. Kink"
    assert review.attribution_line == "by James T. Kink"
    assert review.template_name == "book_review.html"
    assert review.url == "/book-reviews/ship-happens/"
    assert review.cover_image == src_dir / "_images/2001/ship-happens.jpg"
    assert review.breadcrumb == [
        page_types.BreadcrumbEntry(label="books I've read", href="/book-reviews/")
    ]


@pytest.mark.parametrize(
    "contributors, attribution",
    [
        ([BookContributor(name="Jean-Luc Ficard")], "by Jean-Luc Ficard"),
        (
            [BookContributor(name="Emily Ficinson", role="editor")],
            "edited by Emily Ficinson",
        ),
        (
            [
                BookContributor(name="Faye N. Dom"),
                BookContributor(name="Diana Prints", role="translator"),
            ],
            "by Faye N. Dom",
        ),
        (
            [
                BookContributor(name="Faye N. Dom"),
                BookContributor(name="Diana Prints", role="editor"),
            ],
            "by Faye N. Dom",
        ),
        (
            [
                BookContributor(name="Faye N. Dom"),
                BookContributor(name="Diana Prints", role="narrator"),
            ],
            "by Faye N. Dom",
        ),
        (
            [
                BookContributor(name="Mr Milkshake", role="retold by"),
                BookContributor(name="Anne Onymous", role="illustrator"),
            ],
            "retold by Mr Milkshake",
        ),
    ],
)
def test_attribution_line(
    contributors: list[BookContributor], attribution: str
) -> None:
    """
    Tests for `attribution_line`.
    """
    assert attribution_line(contributors) == attribution
