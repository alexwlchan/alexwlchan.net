#!/usr/bin/env python3
"""
Get a list of all posts for a month, to include in my newsletter.
"""

from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from mosaic.page_types import Article, BookReview, read_markdown_files


def clean(title: str) -> str:
    """
    Clean a title so it can go in a Buttondown article.
    """
    return title.replace("`", "")


if __name__ == "__main__":
    pages = read_markdown_files(src_dir=Path("src"))

    try:
        year, month = [int(s) for s in sys.argv[1].split("-")]
    except IndexError:
        year, month = datetime.now().year, datetime.now().month

    matching_pages = sorted(
        [
            p
            for p in pages
            if p.date is not None and p.date.year == year and p.date.month == month
        ],
        key=lambda p: p.date,  # type: ignore
    )

    print("Articles:")
    for p in matching_pages:
        if isinstance(p, Article):
            print(f"- [{clean(p.title)}](https://alexwlchan.net{p.url})")

    print("")

    print("Everything else:")
    for p in matching_pages:
        if not isinstance(p, Article) and not isinstance(p, BookReview):
            print(f"- [{clean(p.title)}](https://alexwlchan.net{p.url})")
