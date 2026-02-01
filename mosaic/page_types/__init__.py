"""
Models for different types of page that appear on the site.
"""

from pathlib import Path

import yaml

from mosaic.fs import find_paths_under

from ._base import BreadcrumbEntry, BaseHtmlPage
from .articles import Article
from .book_reviews import BookReview
from .generic_pages import Page
from .notes import Note, TodayILearned


def read_page_from_markdown(src_dir: Path, md_path: Path) -> BaseHtmlPage:
    """
    Read a Markdown file and parse the YAML front matter.
    """
    try:
        raw = md_path.read_text()
        _, front_matter_str, content = raw.split("---\n", 2)
        front_matter = yaml.safe_load(front_matter_str)
    except Exception as exc:
        raise RuntimeError(f"error reading md file {md_path!r}: {exc}")

    if front_matter["layout"] == "post":
        return Article(
            src_dir=src_dir, md_path=md_path, content=content, **front_matter
        )
    elif front_matter["layout"] == "book_review":
        return BookReview(
            src_dir=src_dir, md_path=md_path, content=content, **front_matter
        )
    elif front_matter["layout"] == "note":
        return Note(src_dir=src_dir, md_path=md_path, content=content, **front_matter)
    elif front_matter["layout"] == "til":
        return TodayILearned(
            src_dir=src_dir, md_path=md_path, content=content, **front_matter
        )
    else:
        return Page(
            src_dir=src_dir,
            md_path=md_path,
            content=content,
            **front_matter,
        )


def read_markdown_files(src_dir: Path) -> list[BaseHtmlPage]:
    """
    Read all the Markdown source files.
    """
    return [
        read_page_from_markdown(src_dir, md_path)
        for md_path in find_paths_under(src_dir, suffix=".md")
    ]


__all__ = [
    "Article",
    "BaseHtmlPage",
    "BookReview",
    "BreadcrumbEntry",
    "Note",
    "Page",
    "TodayILearned",
    "read_markdown_files",
]
