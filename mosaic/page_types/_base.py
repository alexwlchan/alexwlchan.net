"""
The model for an HTML page which is going to be rendered in the site.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from jinja2 import Environment
from pydantic import BaseModel, Field

from mosaic import cache
from mosaic.tint_colours import TintColours
from mosaic.text import markdownify, md5, minify_html
from mosaic.topics import get_topic_by_name


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


class BreadcrumbEntry(BaseModel):
    """
    A breadcrumb entry that helps you see this page in my broader site.
    """

    label: str
    href: str


class BaseHtmlPage(ABC, BaseModel):
    """
    BaseHtmlPage is the base class for all types of HTML page. It should
    never be constructed directly, but instead used to create pages
    as needed.
    """

    @property
    @abstractmethod
    def url(self) -> str:
        """
        The output URL of this page.
        """

    @property
    @abstractmethod
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """

    def belongs_to_topic(self, topic_name: str) -> bool:
        """
        Check whether this post is part of a topic.
        """
        if not self.topics:
            return False
        elif topic_name in self.topics:
            return True
        else:
            return any(
                self.belongs_to_topic(topic_name=c.name)
                for c in get_topic_by_name(topic_name).children
            )

    # The name of the HTML file used as a template for this page.
    template_name: str

    # The source directory to the Markdown source file.
    src_dir: Path | None = None

    # The path to the Markdown source file.
    md_path: Path | None = None

    # The content of the Markdown source file
    content: str = ""

    # The title of the page or post
    title: str = ""

    # A short description of the page or post. Used for <meta> tags
    # and social media previews.
    # TODO(2026-01-20): Make this a required field for all posts.
    summary: str | None = None

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

    # Attribution information about the photo used for the card.
    # TODO(2026-01-20): Actually use this information.
    card_attribution: str | None = None

    card_path: Path | None = None

    # The single topic where this page is saved, which will be used
    # to construct the breadcrumb.
    topics: list[str] = Field(default_factory=lambda: list())

    # A place for me to put topics that don't exist yet, but where
    # this post might be filed in future.
    hidden_topics: list[str] = Field(default_factory=lambda: list())

    def __repr__(self) -> str:  # pragma: no cover
        """
        Return a debugging representation of this page.
        """
        if self.md_path is not None:
            return f"<{type(self).__name__} md_path={self.md_path!r}>"
        else:
            return f"<{type(self).__name__} url={self.url!r}>"

    @property
    def sort_date(self) -> datetime:
        """
        Return the sort date for this item.
        """
        d = self.date_updated or self.date
        assert d is not None
        return d

    def out_path(self, out_dir: Path) -> Path:
        """
        Return the path where this HTML file should be written.
        """
        return out_dir / self.url.strip("/") / "index.html"

    def render_body_html(self, env: Environment) -> str:
        """
        Return the HTML-ified content from the page.

        This is the content unique to the page; it doesn't include any
        of the shared template code.
        """
        cache_ns = "render_body_html"
        cache_key = f"{self.url}:{md5(self.content)}"

        if body := cache.get(cache_ns, cache_key):
            return body

        # Expanding any Jinja2 plugins and templates, then convert
        # the Markdown to HTML. The Jinja2 expansion has to come first
        # so anything in the Jinja2 elements doesn't get Markdown-ified.
        body = markdownify(env.from_string(self.content).render(page=self))

        cache.set(cache_ns, cache_key, body)

        return body

    def render_full_html(self, env: Environment) -> str:
        """
        Return the HTML to be written to disk.
        """
        html_body = self.render_body_html(env)
        template = env.get_template(self.template_name)
        html = template.render(page=self, content=html_body)
        html = minify_html(html)

        return html

    def write(self, env: Environment, out_dir: Path) -> Path:
        """
        Write this HTML file to disk, and return the path of the
        newly-written file.
        """
        out_path = self.out_path(out_dir)

        # The cache key includes the path and modified time of the template.
        # This means the cache could contain stale data if a template partial
        # has changed but the main template didn't; I'll see if that becomes
        # an issue in practice.
        cache_ns = "render_full_html"
        template_mtime = (Path("templates") / self.template_name).stat().st_mtime
        cache_key = f"{self.url}:{template_mtime}:{md5(self.content)}"

        # If the HTML exists in the cache, we don't need to regenerate it
        # and we can skip writing if the file already exists.
        if cache.contains(cache_ns, cache_key):
            if not out_path.exists():
                html = cache.get(cache_ns, cache_key)
                assert isinstance(html, str)
                out_path.parent.mkdir(exist_ok=True, parents=True)
                out_path.write_text(html)
            return out_path

        html = self.render_full_html(env)
        cache.set(cache_ns, cache_key, html)

        out_path.parent.mkdir(exist_ok=True, parents=True)
        out_path.write_text(html)

        return out_path

    def clear_cache(self, clear_body: bool = True) -> None:  # pragma: no cover
        """
        Clear the HTML cache for this page, so it will be rebuilt from
        scratch on the next build.
        """
        if clear_body:
            cache.purge(namespace="render_body_html", prefix=f"{self.url}:")
        cache.purge(namespace="render_full_html", prefix=f"{self.url}:")

    @property
    def is_featured(self) -> bool:
        """
        Returns True if this is a featured post.

        TODO(2026-01-21): Rework the index attributes so this can be
        set directly.
        """
        return self.index.feature

    @property
    def is_excluded(self) -> bool:
        """
        Returns True if this is an excluded post.

        TODO(2026-01-21): Rework the index attributes so this can be
        set directly.
        """
        return self.index.exclude
