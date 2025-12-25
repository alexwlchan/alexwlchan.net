"""
Data structures used to build the site.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
import os
from pathlib import Path
from typing import Literal


@dataclass
class SiteConfig:
    url: str
    title: str
    description: str
    email: str


@dataclass
class Colours:
    css_light: str | None = None
    css_dark: str | None = None
    index_light: str | None = None
    index_dark: str | None = None

    def __post_init__(self):
        # TODO: Validate that a card always has matching light/dark pairs.
        # TODO: Validate that colours have sufficient contrast

        # If CSS colours are set but not index colours, copy the CSS colours
        # to the index colours.
        if self.css_light is not None and self.index_light is None:
            self.index_light = self.css_light
        if self.css_dark is not None and self.index_dark is None:
            self.index_dark = self.css_dark


@dataclass
class IndexConfig:
    """
    Whether this post is featured or excluded from the sitewide index.
    """

    feature: bool = False
    exclude: bool = False


@dataclass
class CardConfig:
    """
    Information about the sharing card on this post.
    """

    # TODO: Do something more useful with this info
    attribution: str

    # Year when this post was published
    year: int

    # Path to the card image on disk
    path: Path

    # Prefix to the card image in the output directory.
    #
    # This depends on the names of all other cards, and is calculated
    # in the "prepare" step of the build.
    out_prefix: str | None = None


@dataclass
class Article:
    path: Path
    layout: Literal["article"]
    title: str
    date: datetime
    content: str
    index: IndexConfig | None = None
    date_updated: datetime | None = None

    # TODO: Implement article cards
    card: None = None

    # TODO: Do I still need `link_direct`? What does it do?
    canonical_url: str | None = None
    link: str | None = None
    link_direct: bool = False

    # TODO: Add a way to surface articles which are untagged, and/or
    # require that every article has tags.
    tags: list[str] = field(default_factory=list)

    # TODO: Require a summary for all articles
    summary: str | None = None

    # TODO: Rename "colors" to "colours"
    colors: Colours | None = None

    # TODO: Show the card attribution as a comment in the <head>
    card_attribution: str | None = None

    # TODO: This is a fix for Jekyll warnings; remove it once I get
    # rid of Jekyll
    excerpt_separator: str | None = None

    # TODO: Is there a neater way to get this?
    order: int = -1

    def __post_init__(self):
        # TODO: Update all my dates so they automatically get parsed
        # as dates.
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S %z")
        if isinstance(self.date_updated, str):
            self.date_updated = datetime.strptime(
                self.date_updated, "%Y-%m-%d %H:%M:%S %z"
            )

        if isinstance(self.colors, dict):
            self.colors = Colours(**self.colors)

        if isinstance(self.index, dict):
            self.index = IndexConfig(**self.index)

    @property
    def slug(self) -> str:
        """
        Returns the slug of the article.

        Articles are named using the Jekyll convention YYYY-MM-DD-{slug}.md,
        so strip off the date prefix and return the slug.
        """
        stem = self.path.stem
        date_prefix = self.date.strftime("%Y-%m-%d-")

        if not stem.startswith(date_prefix):
            raise ValueError(
                f"Article path does not match date: path={self.path}, date={self.date}"
            )

        return stem[len(date_prefix) :]

    @property
    def url(self) -> str:
        """
        Returns the URL of the article, relative to the root of the site.
        """
        return f"/{self.date.year}/{self.slug}/"

    @property
    def nav_section(self) -> str:
        """
        Returns the nav section for this page.
        """
        return "articles"

    @property
    def is_excluded_from_index(self) -> bool:
        """
        Returns True if this article is excluded from the index, False otherwise.
        """
        if self.index is None:
            return False
        else:
            return self.index.exclude

    @property
    def is_featured(self) -> bool:
        if self.index is None:
            return False
        else:
            return self.index.feature

    @property
    def is_new(self) -> bool:
        """
        A new article is any published in the last few weeks.
        """
        now = datetime.now(tz=timezone.utc)
        return (now - self.date).total_seconds() < 21 * 24 * 60 * 60

    @property
    def visible_tags(self) -> list[str]:
        """
        An article only has visible tags if it's visible.
        """
        if self.is_excluded_from_index:
            return []
        else:
            return self.tags



@dataclass
class TodayILearned:
    path: Path
    layout: Literal["til"]
    title: str
    date: datetime
    content: str
    index: IndexConfig | None = None
    date_updated: datetime | None = None

    # TODO: Add a way to surface TILs which are untagged, and/or require
    # that every TIL has tags.
    tags: list[str] = field(default_factory=list)

    # TODO: Require a summary for all TILs
    summary: str | None = None

    # TODO: Rename "colors" to "colours"
    colors: Colours | None = None

    # TODO: This is a fix for Jekyll warnings; remove it once I get
    # rid of Jekyll
    excerpt_separator: str | None = None

    # TODO: Implement article cards
    card: None = None

    def __post_init__(self):
        # TODO: Update all my dates so they automatically get parsed
        # as dates.
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S %z")
        if isinstance(self.date_updated, str):
            self.date_updated = datetime.strptime(
                self.date_updated, "%Y-%m-%d %H:%M:%S %z"
            )

        if isinstance(self.colors, dict):
            self.colors = Colours(**self.colors)

        if isinstance(self.index, dict):
            self.index = IndexConfig(**self.index)

    @property
    def slug(self) -> str:
        """
        Returns the slug of the TIL.

        TILs are named using the Jekyll convention YYYY-MM-DD-{slug}.md,
        so strip off the date prefix and return the slug.
        """
        stem = self.path.stem
        date_prefix = self.date.strftime("%Y-%m-%d-")

        if not stem.startswith(date_prefix):
            raise ValueError(
                f"TIL path does not match date: path={self.path}, date={self.date}"
            )

        return stem[len(date_prefix) :]

    @property
    def url(self) -> str:
        """
        Returns the URL of the article, relative to the root of the site.
        """
        return f"/til/{self.date.year}/{self.slug}/"

    @property
    def nav_section(self) -> str:
        """
        Returns the nav section for this page.
        """
        return "til"

    @property
    def is_excluded_from_index(self) -> bool:
        """
        Returns True if this article is excluded from the index, False otherwise.
        """
        if self.index is None:
            return False
        else:
            return self.index.exclude

    @property
    def is_featured(self) -> bool:
        if self.index is None:
            return False
        else:
            return self.index.feature

    @property
    def link_direct(self) -> bool:
        return False

    @property
    def visible_tags(self) -> list[str]:
        """
        An article only has visible tags if it's visible.
        """
        if self.is_excluded_from_index:
            return []
        else:
            return self.tags


@dataclass
class TagPage:
    namespace: str
    tag_name: str
    tag_description: str | None
    featured_posts: list[Article | TodayILearned]
    remaining_posts: list[Article | TodayILearned]
    content: str = ""

    @property
    def title(self):
        return f"Tagged with “{self.tag_name}”"

    @property
    def url(self) -> str:
        return "/" + os.path.join("tags", self.namespace, self.tag_name.replace(" ", "-")) + "/"

    @property
    def nav_section(self) -> str:
        return "tags"

    @property
    def colors(self) -> Literal[None]:
        return None

    @property
    def card(self) -> Literal[None]:
        return None


@dataclass
class Page:
    path: Path
    layout: Literal["page"]
    title: str
    content: str
    summary: str | None = None
    date_updated: datetime | None = None
    nav_section: str | None = None

    # TODO: Replace this field with something more structured
    meta: list[str] = field(default_factory=list)

    # TODO: Rename "colors" to "colours"
    colors: Colours | None = None

    # TODO: Implement article cards
    card: None = None

    def __post_init__(self):
        # TODO: Update all my dates so they automatically get parsed
        # as dates.
        if isinstance(self.date_updated, str):
            self.date_updated = datetime.strptime(
                self.date_updated, "%Y-%m-%d %H:%M:%S %z"
            )

        if isinstance(self.colors, dict):
            self.colors = Colours(**self.colors)

    @property
    def url(self) -> str:
        """
        Returns the URL of the page, relative to the root of the site.
        """
        if self.path.name == "index.md":
            return "/" + str(self.path.parent) + "/"
        else:
            return "/" + str(self.path.with_suffix("")) + "/"


@dataclass
class RSSFeed:
    path: Path
    layout: Literal["rss_feed"]
    content: str


@dataclass
class StaticFile:
    path: Path


@dataclass
class SiteInput:
    src_dir: Path
    config: SiteConfig
    articles: list[Article] = field(default_factory=list)
    tils: list[TodayILearned] = field(default_factory=list)
    pages: list[Page] = field(default_factory=list)
    feeds: list[RSSFeed] = field(default_factory=list)
    static_files: dict[Path, StaticFile] = field(default_factory=dict)
    visible_tags: dict[str, int] = field(default_factory=dict)

    @property
    def url(self) -> str:
        return self.config.url

    @property
    def email(self) -> str:
        return self.config.email

    @property
    def description(self) -> str:
        return self.config.description

    @property
    def title(self) -> str:
        return self.config.title

    @property
    def posts(self) -> list[Article | TodayILearned]:
        return self.articles + self.tils
