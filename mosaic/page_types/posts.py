"""
Posts are any dated content.
"""

from datetime import datetime
from pathlib import Path
import re

from pydantic import BaseModel, Field

from ._base import BaseHtmlPage


class IndexInfo(BaseModel):
    """
    Toggles for how this page appears in the site-wide indexes.
    """

    exclude: bool = False
    feature: bool = False


class Post(BaseHtmlPage):
    """
    A post is a dated piece of writing, usually with original thought.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a Post.
    md_path: Path
    src_dir: Path
    date: datetime

    # Toggles for how this page appears in the site-wide indexes.
    # TODO(2026-01-20): Decompose this into individual booleans.
    index: IndexInfo = Field(default_factory=lambda: IndexInfo())

    @property
    def slug(self) -> str:
        """
        Returns a URL slug for the post.
        """
        return re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)

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
