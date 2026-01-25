"""
The model for an HTML page which is going to be rendered in the site.
"""

from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Literal, Self, TypedDict

from jinja2 import Environment
import minify_html
from pydantic import BaseModel, Field, model_validator
import yaml

from .fs import find_paths_under
from .tint_colours import TintColours
from .text import markdownify


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

    # The HTML content of the file
    html_content: str = ""

    # What's the URL of this page?
    url: str = ""

    # The layout template to use
    layout: Literal["page", "post", "til"] | None = None

    # What template should I use?
    template_name: str = ""

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

    card_path: Path | None = None

    def __repr__(self) -> str:  # pragma: no cover
        """
        Returns a debugging representation of this page.
        """
        if self.md_path is not None:
            return f"<{type(self).__name__} md_path={self.md_path!r}>"
        else:
            return f"<{type(self).__name__} url={self.url!r}>"

    @classmethod
    def from_path(cls, src_dir: Path, md_path: Path) -> "HtmlPage":
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
        else:
            return HtmlPage(
                src_dir=src_dir,
                md_path=md_path,
                content=content,
                **front_matter,
            )

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

        if self.layout == "page" and self.md_path.name == "index.md":
            self.url = f"/{self.md_path.parent.relative_to(self.src_dir)}/".replace(
                "./", ""
            )
        elif self.layout == "page":
            relative_path = self.md_path.relative_to(self.src_dir).with_suffix("")
            self.url = f"/{relative_path}/"
        elif self.layout == "post":
            assert self.date is not None
            self.url = f"/{self.date.year}/{self.slug}/"
        elif self.layout == "til":
            assert self.date is not None
            self.url = f"/til/{self.date.year}/{self.slug}/"
        else:  # pragma: no cover
            raise ValueError(f"unrecognised layout: {self.layout!r}")

        return self

    @model_validator(mode="after")
    def calculate_template_name(self) -> Self:
        """
        Calculate the template name of this page, if not set explicitly.
        """
        if self.template_name != "":
            return self

        if self.layout == "page":
            self.template_name = "page.html"
        elif self.layout == "post":
            self.template_name = "post.html"
        elif self.layout == "til":
            self.template_name = "til.html"
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

    @property
    def is_featured(self) -> bool:
        """
        Returns True if this is a featured post.

        TODO(2026-01-21): Rework the index attributes so this can be
        set directly.
        """
        return self.index.feature

    @property
    def is_new(self) -> bool:
        """
        Returns True if this page was published recently, False otherwise.
        """
        if self.date is None:
            return False
        else:
            return (datetime.now(tz=timezone.utc) - self.date).days <= 21

    def __getattr__(self, name: str) -> Any:
        """
        Look up an attribute, trying in extra_variables first.
        """
        try:
            return self.extra_variables[name]
        except KeyError:
            return super().__getattr__(name)  # type: ignore


class Article(HtmlPage):
    """
    An article is a long-form piece of writing, usually with original thought.
    """

    # When this article was first written. All articles must have a date.
    date: datetime

    # What order is this in the list of all articles?
    order: int = -1

    # Articles always use the `post.html` template
    # TODO: Rename this to `article.html` for consistency.
    template_name: str = "post.html"

    # The short filename for this card, used on /articles/ to reduce page
    # weight. For example, "dominant-colours" might become "do".
    card_short_name: str | None = None

    def __hash__(self) -> int:
        """
        Return a hash; this is so I can use articles as dict keys when
        working out the short names for cards.
        """
        return hash(repr(self))
