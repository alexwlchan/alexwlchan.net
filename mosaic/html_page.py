"""
The model for an HTML page which is going to be rendered in the site.
"""

from datetime import datetime
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from pydantic import BaseModel
import yaml


class TintColours(TypedDict):
    """
    A set of tint colours for a page.
    """

    css_light: NotRequired[str]
    css_dark: NotRequired[str]
    index_light: NotRequired[str]
    index_dark: NotRequired[str]


class IndexInfo(TypedDict):
    """
    Toggles for how this page appears in the site-wide indexes.
    """

    exclude: NotRequired[Literal[True]]
    feature: NotRequired[Literal[True]]


class PartOf(TypedDict):
    """
    Which section this page is part of.
    """

    url: str
    label: str


class HtmlPage(BaseModel):
    """
    An HTML page which is going to be rendered in the site.
    """

    # The source directory to the Markdown source file.
    src_dir: Path

    # The path to the Markdown source file.
    md_path: Path

    # The content of the Markdown source file
    content: str

    # The layout template to use
    layout: Literal["page", "post", "til"]

    # The title of the page or post
    title: str

    # A short description of the page or post. Used for <meta> tags
    # and social media previews.
    # TODO(2026-01-20): Make this a required field for all posts.
    summary: str | None = None

    # A list of tags for this page or post
    tags: list[str] | None = None

    # When this page or post was created
    date: datetime | None = None

    # When this page or post was last updated
    date_updated: datetime | None = None

    # An external URL that this page should like to, like a link blog.
    # This is used on the HTML version of the page, and where clicking
    # on the RSS feed entry will take the reader.
    link: str | None = None

    # Whether the articles index should link directly to the external page.
    link_direct: bool | None = None

    # An external URL that is the canonical copy of this page, used
    # for external posts I've copied to this site
    canonical_url: str | None = None

    # Tint colours for this page.
    # TODO(2026-01-20): Rename this field to "colours".
    colors: TintColours | None = None

    # Toggles for how this page appears in the site-wide indexes.
    # TODO(2026-01-20): Decompose this into individual booleans.
    index: IndexInfo | None = None

    # Which section is this page part of?
    part_of: PartOf | None = None

    # Which section of the site this page/post belongs to
    nav_section: Literal["articles", "til", "contact", "subscribe", "tags"] | None = (
        None
    )

    # Attribution information about the photo used for the card.
    # TODO(2026-01-20): Actually use this information.
    card_attribution: str | None = None

    # Unused except to suppress a Jekyll warning
    # TODO(2026-01-20): Remove this once I've gotten rid of Jekyll.
    excerpt_separator: str | None = None

    @classmethod
    def from_path(cls, src_dir: Path, md_path: Path) -> "HtmlPage":
        """
        Read a Markdown file and parse the YAML front matter.
        """
        try:
            raw = md_path.read_text()
            _, front_matter, content = raw.split("---\n", 2)
            return HtmlPage(
                src_dir=src_dir,
                md_path=md_path,
                content=content,
                **yaml.safe_load(front_matter),
            )
        except Exception as exc:
            raise RuntimeError(f"error reading md file {md_path!r}: {exc}")
