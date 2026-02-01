#!/usr/bin/env python3
# type: ignore
"""
Create a new post.
"""

from datetime import datetime, timezone
import os
from pathlib import Path
import re
import subprocess
import sys

import httpx
from InquirerPy import inquirer
import termcolor
from unidecode import unidecode
import yaml

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site
from mosaic.html_page import BookReview


def slugify(u: str) -> str:
    """
    Convert Unicode string into blog slug.

    From https://leancrew.com/all-this/2014/10/asciifying/
    """
    # fmt: off
    u = re.sub(u'[–—/:;,.]', '-', u)  # replace separating punctuation
    a = unidecode(u).lower()          # best ASCII substitutions, lowercased
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
    post_type = inquirer.select(
        message="What type of post are you writing?",
        choices=["article", "note", "book review"],
    ).execute()

    now = datetime.now(tz=timezone.utc)
    year = str(now.year)

    if post_type == "book review":
        title = inquirer.text(message="Title:".ljust(9, " ")).execute()
        slug = inquirer.text(message="URL slug:", default=slugify(title)).execute()
        author = inquirer.text(message="Author:".ljust(9, " ")).execute()
        isbn13 = inquirer.text(message="ISBN13:".ljust(9, " ")).execute()
        publication_year = inquirer.text(message="Publication year:").execute()

        site = Site()
        existing_reviews = [
            p for p in site.read_markdown_source_files() if isinstance(p, BookReview)
        ]

        all_genres = set()
        for p in site.read_markdown_source_files():
            if isinstance(p, BookReview):
                for g in p.book.genres:
                    all_genres.add(g)

        ADD_NEW = "[add new…]"

        def get_extra_genres(result: list[str]) -> list[str]:
            """
            Misuse the filter mechanism to define new genres if there isn't
            one that matches what I already have.

            The output is a bit clumsy, but I won't hit this path very often.
            """
            if ADD_NEW in result:
                result.remove(ADD_NEW)
                result.extend(
                    [
                        gn.strip()
                        for gn in inquirer.text(message="New genres:")
                        .execute()
                        .split(",")
                    ]
                )
                return result
            else:
                return result

        genres = inquirer.fuzzy(
            message="Genres:",
            choices=sorted(all_genres) + [ADD_NEW],
            multiselect=True,
            filter=get_extra_genres,
        ).execute()

        # TODO: If the hour is before a certain time, default to
        # the previous day?
        date_read = inquirer.text(
            "Date read:", default=datetime.now().strftime("%Y-%m-%d (today)")
        ).execute()
        date_read = date_read.replace(" (today)", "")

        book_format = inquirer.select(
            message="Book format:", choices=["paperback", "hardback", "ebook"]
        ).execute()

        rating = (
            inquirer.select(
                message="Rating:", choices=["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆"]
            )
            .execute()
            .count("★")
        )
        cover_url = inquirer.text("Cover URL:").execute()

        cover_path = (Path("src/_images") / year / slug).with_suffix(
            os.path.splitext(cover_url)[-1]
        )
        cover_path.parent.mkdir(exist_ok=True)

        try:
            resp = httpx.get(cover_url)
            resp.raise_for_status()
            with open(cover_path, "xb") as out_file:
                out_file.write(resp.content)

            css_light = get_tint_colour(cover_path, background="white")
            css_dark = get_tint_colour(cover_path, background="black")
        except Exception as exc:
            print(
                termcolor.colored(
                    f"could not download cover to {cover_path}: {exc}", "red"
                )
            )
            css_light = "#000000"
            css_dark = "#ffffff"

        book = {"title": title, "contributors": [{"name": author}]}
        book["genres"] = genres
        if publication_year:
            book["publication_year"] = publication_year
        if isbn13:
            book["isbn13"] = isbn13

        md_path = Path("src/book-reviews") / year / f"{slug}.md"
        md_path.parent.mkdir(exist_ok=True)
        with open(md_path, "w") as out_file:
            out_file.write(
                "---\n"
                "layout: book_review\n"
                f"date: {now.isoformat()}\n"
                "\n"
                + yaml.dump({"book": book})
                + "\n"
                + yaml.dump(
                    {
                        "review": {
                            "date_read": date_read,
                            "format": book_format,
                            "rating": rating,
                            "summary": "TODO Write a summary",
                        }
                    }
                )
                + "\n"
                + yaml.dump({"colors": {"css_light": css_light, "css_dark": css_dark}})
                + "\n---\n"
            )

        subprocess.check_call(["open", str(md_path)])
    else:
        raise NotImplementedError(post_type)
