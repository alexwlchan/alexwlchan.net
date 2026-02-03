"""
Models for different types of page that appear on the site.
"""

from pathlib import Path

import termcolor
import yaml

from mosaic.fs import find_paths_under

from ._base import BreadcrumbEntry, BaseHtmlPage
from .articles import Article
from .book_reviews import BookReview
from .generic_pages import Page
from .notes import Note, TodayILearned
from .topic_pages import TopicPage


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

    layout = front_matter.pop("layout")

    match layout:
        case "post":
            return Article(
                src_dir=src_dir, md_path=md_path, content=content, **front_matter
            )
        case "book_review":
            return BookReview(
                src_dir=src_dir, md_path=md_path, content=content, **front_matter
            )
        case "note":
            return Note(
                src_dir=src_dir, md_path=md_path, content=content, **front_matter
            )
        case "til":
            return TodayILearned(
                src_dir=src_dir, md_path=md_path, content=content, **front_matter
            )
        case "page":
            return Page(
                src_dir=src_dir,
                md_path=md_path,
                content=content,
                **front_matter,
            )
        case "topic":
            return TopicPage(
                src_dir=src_dir,
                md_path=md_path,
                content=content,
                **front_matter,
            )
        case _:
            raise ValueError(f"unrecognised layout in {md_path}: {layout!r}")


def read_markdown_files(src_dir: Path) -> list[BaseHtmlPage]:
    """
    Read all the Markdown source files.
    """
    result = []

    for md_path in find_paths_under(src_dir, suffix=".md"):
        try:
            result.append(read_page_from_markdown(src_dir, md_path))
        except Exception:
            print(termcolor.colored("error reading {md_path}: {exc}", "red"))
            raise

    return result


__all__ = [
    "Article",
    "BaseHtmlPage",
    "BookReview",
    "BreadcrumbEntry",
    "Note",
    "Page",
    "TodayILearned",
    "TopicPage",
    "read_markdown_files",
]
