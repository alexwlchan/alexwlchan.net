#!/usr/bin/env python3
"""
Create a new post.
"""

from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from chives.fetch import download_image
from InquirerPy import inquirer
import yaml

sys.path.append(str(Path(__file__).parent.parent))

from mosaic.page_types import BookReview, read_markdown_files
from mosaic.text import coloured


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


def ask_for_choice(message: str, choices: list[str]) -> str:
    """
    Ask the user to select a choice from a predefined list.
    """
    return inquirer.select(message=message, choices=choices).execute()  # type: ignore


def ask_for_text(message: str, **kwargs: Any) -> str:
    """
    Ask the user to enter a free-form text answer.
    """
    return inquirer.text(message=message, **kwargs).execute()  # type: ignore


if __name__ == "__main__":
    post_type = ask_for_choice(
        message="What type of post are you writing?",
        choices=["article", "note", "book review"],
    )

    now = datetime.now(tz=timezone.utc)
    year = str(now.year)

    if post_type == "book review":
        title = ask_for_text(message="Title:".ljust(9, " "))
        slug = ask_for_text(message="URL slug:", default=slugify(title))
        author = ask_for_text(message="Author:".ljust(9, " "))
        isbn13 = ask_for_text(message="ISBN13:".ljust(9, " "))
        publication_year = ask_for_text(message="Publication year:")

        existing_reviews = [
            p
            for p in read_markdown_files(src_dir=Path("src/book-reviews"))
            if isinstance(p, BookReview)
        ]

        all_genres = set()
        for p in existing_reviews:
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
                    [gn.strip() for gn in ask_for_text("New genres:").split(",")]
                )
                return result
            else:
                return result

        genres = inquirer.fuzzy(  # type: ignore
            message="Genres:",
            choices=sorted(all_genres) + [ADD_NEW],
            multiselect=True,
            filter=get_extra_genres,
        ).execute()

        # TODO: If the hour is before a certain time, default to
        # the previous day?
        date_read = ask_for_text(
            "Date read:", default=datetime.now().strftime("%Y-%m-%d (today)")
        )
        date_read = date_read.replace(" (today)", "")

        book_format = ask_for_choice(
            message="Book format:", choices=["paperback", "hardback", "ebook"]
        )

        rating = ask_for_choice(
            message="Rating:", choices=["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆"]
        ).count("★")
        cover_url = ask_for_text("Cover URL:")

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
    elif post_type == "note":
        title = ask_for_text(message="Title:".ljust(9, " "))
        slug = ask_for_text(message="URL slug:", default=slugify(title))
        md_path = Path("src/notes") / year / f"{now.strftime('%Y-%m-%d')}-{slug}.md"
        md_path.parent.mkdir(exist_ok=True)
        with open(md_path, "x") as out_file:
            out_file.write(
                f"---\nlayout: note\ndate: {now.isoformat()}\ntitle: {title}\n---\n"
            )
    else:
        raise NotImplementedError(post_type)
