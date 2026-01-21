"""
The model for an HTML page which is going to be rendered in the site.
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Any, Literal, Self, TypedDict

from pydantic import BaseModel, Field, model_validator
import yaml

from .tint_colours import TintColours


class IndexInfo(BaseModel):
    """
    Toggles for how this page appears in the site-wide indexes.
    """

    exclude: bool = False
    feature: bool = False


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
    src_dir: Path | None = None

    # The path to the Markdown source file.
    md_path: Path | None = None

    # The content of the Markdown source file
    content: str = ""

    # What's the URL of this page?
    url: str = ""

    # The layout template to use
    layout: Literal["page", "post", "til"] | None = None

    # What template should I use?
    template: str = ""

    # The title of the page or post
    title: str

    # A short description of the page or post. Used for <meta> tags
    # and social media previews.
    # TODO(2026-01-20): Make this a required field for all posts.
    summary: str | None = None

    # A list of tags for this page or post
    tags: list[str] = Field(default_factory=lambda: list())

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
    index: IndexInfo = Field(default_factory=lambda: IndexInfo())

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

    # Extra variables which are specific to this page or template.
    extra_variables: dict[str, Any] = Field(default_factory=lambda: dict())

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

    def out_path(self, out_dir: Path) -> Path:
        """
        Returns the path where this HTML file should be written.
        """
        return out_dir / self.url.strip("/") / "index.html"

    @model_validator(mode="after")
    def calculate_url(self) -> Self:
        """
        Calculate the URL of this page, if not set explicitly.
        """
        if self.url != "":
            return self

        assert self.layout is not None
        assert self.src_dir is not None
        assert self.md_path is not None

        if self.layout == "page" and self.md_path == self.src_dir / "index.md":
            self.url = "/"
        elif self.layout == "page":
            relative_path = self.md_path.relative_to(self.src_dir).with_suffix("")
            self.url = f"/{relative_path}/"
        elif self.layout == "post":
            assert self.date is not None
            year = self.date.year

            # Remove the YYYY-MM-DD prefix which is required by Jekyll.
            # TODO(2026-01-20): Get rid of the requirement for this prefix.
            slug = re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)
            self.url = f"/{year}/{slug}/"
        elif self.layout == "til":
            assert self.date is not None
            year = self.date.year

            # Remove the YYYY-MM-DD prefix which is required by Jekyll.
            # TODO(2026-01-20): Get rid of the requirement for this prefix.
            slug = re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)
            self.url = f"/til/{year}/{slug}/"
        else:  # pragma: no cover
            raise ValueError(f"unrecognised layout: {self.layout!r}")

        return self

    @model_validator(mode="after")
    def remove_tags_on_hidden_posts(self) -> Self:
        """
        If a post is hidden from the sitewide index, remove its tags.

        TODO(2026-01-21): Decide if this is still the correct behaviour.
        """
        if self.index.exclude:
            self.tags = []
        return self
