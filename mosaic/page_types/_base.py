"""
The model for an HTML page which is going to be rendered in the site.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Literal, Self, TypedDict

from jinja2 import Environment
import minify_html
from pydantic import BaseModel, Field, model_validator

from mosaic.fs import find_paths_under
from mosaic.tint_colours import TintColours
from mosaic.text import markdownify
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
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
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
        Checks whether this post is part of a topic.
        """
        if self.topic is None:
            return False
        elif self.topic == topic_name:
            return True
        else:
            return any(
                self.belongs_to_topic(topic_name=c.name)
                for c in get_topic_by_name(topic_name).children
            )

    # The source directory to the Markdown source file.
    src_dir: Path | None = None

    # The path to the Markdown source file.
    md_path: Path | None = None

    # The content of the Markdown source file
    content: str = ""

    # The HTML content of the file
    html_content: str = ""

    # The title of the page or post
    title: str = ""

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

    # Extra variables which are specific to this page or template.
    extra_variables: dict[str, Any] = Field(default_factory=lambda: dict())

    card_path: Path | None = None

    # The single topic where this page is saved, which will be used
    # to construct the breadcrumb.
    topic: str | None = None

    def __repr__(self) -> str:  # pragma: no cover
        """
        Returns a debugging representation of this page.
        """
        if self.md_path is not None:
            return f"<{type(self).__name__} md_path={self.md_path!r}>"
        else:
            return f"<{type(self).__name__} url={self.url!r}>"

    def out_path(self, out_dir: Path) -> Path:
        """
        Returns the path where this HTML file should be written.
        """
        return out_dir / self.url.strip("/") / "index.html"

    @model_validator(mode="after")
    def remove_tags_on_hidden_posts(self) -> Self:
        """
        If a post is hidden from the sitewide index, remove its tags.

        TODO(2026-01-21): Decide if this is still the correct behaviour.
        """
        if self.index.exclude:
            self.tags = []
        return self

    @model_validator(mode="after")
    def set_sharing_card(self) -> Self:
        """
        Find a sharing card for this post.
        """
        if self.md_path is None or self.date is None:
            return self

        assert self.src_dir is not None

        card_dir = self.src_dir / "_images/cards" / str(self.date.year)
        if not card_dir.exists():
            return self

        matching_cards = [
            p.relative_to(self.src_dir)
            for p in find_paths_under(card_dir)
            if p.stem == self.slug
        ]
        if len(matching_cards) == 0:
            return self
        elif len(matching_cards) == 1:
            self.card_path = matching_cards[0]
            return self
        else:
            raise ValueError(f"multiple matching cards for {self.md_path}")

    @property
    def slug(self) -> str:
        """
        Returns a URL slug for the post.
        """
        assert self.md_path is not None

        # Remove the YYYY-MM-DD prefix which is required by Jekyll.
        # TODO(2026-01-20): Get rid of the requirement for this prefix.
        return re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)

    def write(self, env: Environment, out_dir: Path) -> Path:
        """
        Write this HTML file to disk, and return the path of the
        newly-written file.
        """
        out_path = self.out_path(out_dir)

        # Steps to render HTML:
        #
        #   1. Run the HTML through the Jinja2 templates, so plugins
        #      and embeds are expanded
        #   2. Convert the Markdown to HTML
        #
        self.html_content = markdownify(env.from_string(self.content).render(page=self))

        template = env.get_template(self.template_name)
        html = template.render(page=self, content=self.html_content)

        html = minify_html.minify(
            html,
            keep_html_and_head_opening_tags=True,
            keep_closing_tags=True,
            minify_css=True,
            minify_js=True,
        )

        out_path.parent.mkdir(exist_ok=True, parents=True)
        out_path.write_text(html)

        return out_path

    def __getattr__(self, name: str) -> Any:
        """
        Look up an attribute, trying in extra_variables first.
        """
        try:
            return self.extra_variables[name]
        except KeyError:
            return super().__getattr__(name)  # type: ignore
