"""
Models for different types of page that appear on the site.
"""

import glob
import os
from pathlib import Path

import yaml

from mosaic.text import coloured

from ._base import BreadcrumbEntry, BaseHtmlPage, IndexInfo
from .articles import Article
from .book_reviews import BookContributor, BookReview, BookInfo, ReviewInfo
from .generic_pages import Page
from .notes import Note
from .posts import Post
from .projects import (
    ProjectCommit,
    ProjectHomepage,
    ProjectLog,
    ProjectSingleFile,
    ProjectTags,
    ProjectTree,
)
from .topic_pages import TopicPage


def read_page_from_markdown(src_dir: Path, md_path: str | Path) -> BaseHtmlPage:
    """
    Read a Markdown file and parse the YAML front matter.
    """
    with open(md_path) as in_file:
        raw = in_file.read()

    # The YAML front matter is delimited by `---\n` at the start
    # and `\n---\n` at the end. Extract the front matter string
    # from the body.
    #
    # TODO: Use TOML; it's in the standard library and is slightly
    # faster than parsing YAML.
    try:
        _, front_matter_str, content = raw.split("---\n", 2)
        front_matter = yaml.load(front_matter_str, Loader=yaml.CSafeLoader)
    except Exception as exc:
        raise RuntimeError(f"error reading md file {md_path!r}: {exc}")

    layout = front_matter.pop("layout")

    if (
        "topic" in front_matter
        and "topics" not in front_matter
        and isinstance(front_matter["topic"], str)
    ):
        front_matter["topics"] = [front_matter.pop("topic")]

    kwargs = {
        "src_dir": src_dir,
        "md_path": md_path,
        "content": content,
        **front_matter,
    }

    match layout:
        case "article":
            return Article(**kwargs)
        case "book_review":
            return BookReview(**kwargs)
        case "note":
            return Note(**kwargs)
        case "page":
            return Page(**kwargs)
        case "topic":
            return TopicPage(**kwargs)
        case _:
            raise ValueError(f"unrecognised layout in {md_path}: {layout!r}")


def read_markdown_files(src_dir: Path) -> list[BaseHtmlPage]:
    """
    Read all the Markdown source files.
    """
    # Search for all the cards in the card directory and build a lookup,
    # so we can efficiently assign cards to posts when reading the Markdown.
    card_lookup = {}
    for img_path in glob.glob(f"{src_dir}/images/cards/**/*", recursive=True):
        if not os.path.isfile(img_path) or not img_path.endswith((".jpg", ".png")):
            continue

        year = int(os.path.basename(os.path.dirname(img_path)))
        slug, _ = os.path.splitext(os.path.basename(img_path))
        assert (year, slug) not in card_lookup, (
            f"duplicate card found for year={year}, slug={slug}"
        )
        card_lookup[(year, slug)] = Path(img_path).relative_to(src_dir)

    result = []

    for md_path in glob.glob(f"{src_dir}/**/*.md", recursive=True):
        try:
            page = read_page_from_markdown(src_dir, md_path)
        except Exception as exc:  # pragma: no cover
            print(coloured(f"error reading {md_path}: {exc}", "red"))
            raise

        if isinstance(page, Post):
            try:
                page.card_path = card_lookup[(page.date.year, page.slug)]
            except KeyError:
                pass

        result.append(page)

    return result


__all__ = [
    "Article",
    "BaseHtmlPage",
    "BookContributor",
    "BookInfo",
    "BookReview",
    "BreadcrumbEntry",
    "IndexInfo",
    "Note",
    "Page",
    "Post",
    "ProjectCommit",
    "ProjectHomepage",
    "ProjectLog",
    "ProjectSingleFile",
    "ProjectTags",
    "ProjectTree",
    "ReviewInfo",
    "TopicPage",
    "read_markdown_files",
]
