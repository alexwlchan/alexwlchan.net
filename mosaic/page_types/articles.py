"""
Models for articles.
"""

from datetime import datetime, timezone
from pathlib import Path

from ._base import BaseHtmlPage


class Article(BaseHtmlPage):
    """
    An article is a long-form piece of writing, usually with original thought.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a BookReview.
    md_path: Path
    src_dir: Path
    date: datetime

    # What order is this in the list of all articles?
    order: int = -1

    # The short filename for this card, used on /articles/ to reduce page
    # weight. For example, "dominant-colours" might become "do".
    card_short_name: str | None = None

    # An external URL that this page should like to, like a link blog.
    # This is used on the HTML version of the page, and where clicking
    # on the RSS feed entry will take the reader.
    link: str | None = None

    # Whether the articles index should link directly to the external page.
    link_direct: bool | None = None

    # An external URL that is the canonical copy of this page, used
    # for external posts I've copied to this site
    canonical_url: str | None = None

    def __hash__(self) -> int:
        """
        Return a hash; this is so I can use articles as dict keys when
        working out the short names for cards.
        """
        return hash(repr(self))

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        # TODO: Rename this to `article.html` for consistency.
        return "post.html"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/{self.date.year}/{self.slug}/"

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
