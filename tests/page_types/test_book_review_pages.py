"""
Tests for `mosaic.page_types.book_reviews`.
"""

from datetime import date, datetime
from pathlib import Path


from mosaic import page_types
from mosaic.models import (
    BookContributor,
    BookInfo,
    BookReview as ReviewInfo,
    BreadcrumbEntry,
)


def test_book_review_properties(src_dir: Path) -> None:
    """
    Test the `BookReview` page type.
    """
    (src_dir / "images/2001").mkdir(parents=True)
    (src_dir / "images/2001/ship-happens.jpg").write_text("JPEG;placeholder")

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
    assert review.cover_image == src_dir / "images/2001/ship-happens.jpg"
    assert review.breadcrumb == [
        BreadcrumbEntry(label="books I've read", href="/book-reviews/")
    ]
