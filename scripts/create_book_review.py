#!/usr/bin/env python3
"""
Create a new post.
"""

from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
from urllib.parse import quote_plus
import webbrowser

from chives.fetch import download_image
from chives.text import coloured
import yaml


def slugify(u: str) -> str:
    """
    Convert Unicode string into blog slug.

    Based on https://leancrew.com/all-this/2014/10/asciifying/
    """
    # fmt: off
    u = re.sub(u'[–—/:;,.]', '-', u)  # replace separating punctuation
    a = u.lower()
    a = re.sub(r'[^a-z0-9 -]', '', a) # delete any other characters
    a = a.replace(' ', '-')           # spaces to hyphens
    a = re.sub(r'-+', '-', a)         # condense repeated hyphens
    # fmt: on
    return a


def get_tint_colour(path: str | Path, *, background: str) -> str:
    """
    Get the tint colour for an image.
    """
    if background == "white":
        background = "#ffffff"
    elif background == "black":
        background = "#000000"

    result = subprocess.check_output(
        ["dominant_colours", str(path), "--best-against-bg", background], text=True
    )
    return result.strip()


if __name__ == "__main__":
    now = datetime.now(tz=timezone.utc)
    year = str(now.year)

    title = input("Title: ")
    slug = slugify(title)
    author = input("Author: ")
    isbn13 = input("ISBN13: ")
    publication_year = input("Publication year: ")

    genres = [g.strip() for g in input("Genres: ").split(",")]

    # TODO: If the hour is before a certain time, default to
    # the previous day?
    date_read = input("Date read: ")

    book_format = input("Book format (paperback, hardback, ebook): ")

    is_library = input("Is this a library book (y/n): ") == "y"

    rating = int(input("Star rating: "))

    cover_query = quote_plus(f"cover {title} {author}")
    webbrowser.open(
        f"https://next.duckduckgo.com/?q={cover_query}&ia=images&iax=images"
    )

    cover_url = input("Cover URL: ")

    try:
        cover_path = download_image(
            url=cover_url, out_prefix=Path("src/images") / year / slug
        )

        css_light = get_tint_colour(cover_path, background="white")
        css_dark = get_tint_colour(cover_path, background="black")
    except Exception as exc:
        print(coloured(f"could not download cover from {cover_url}: {exc}", "red"))
        css_light = "#000000"
        css_dark = "#ffffff"

    book = {"title": title, "contributors": [{"name": author}]}
    book["genres"] = genres
    if publication_year:
        book["publication_year"] = publication_year
    if isbn13:
        book["isbn13"] = isbn13

    review = {
        "date_read": date_read,
        "format": book_format,
        "rating": rating,
        "summary": "TODO Write a summary",
    }
    if is_library:
        review["from_the_library"] = True

    md_path = Path("src/book-reviews") / year / f"{slug}.md"
    md_path.parent.mkdir(exist_ok=True)
    with open(md_path, "x") as out_file:
        out_file.write(
            "---\n"
            "layout: book_review\n"
            f"date: {now.isoformat()}\n"
            "\n"
            + yaml.dump({"book": book})
            + "\n"
            + yaml.dump({"review": review})
            + "\n"
            + yaml.dump(
                {"colours": {"css_light": css_light, "css_dark": css_dark}},
                sort_keys=False,
            )
            + "\n---\n"
        )

    subprocess.check_call(["open", str(md_path)])
