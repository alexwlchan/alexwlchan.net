"""
Posts are any dated content.
"""

from datetime import datetime
from pathlib import Path
import re

from ._base import BaseHtmlPage


class Post(BaseHtmlPage):
    """
    A post is a dated piece of writing, usually with original thought.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a Post.
    md_path: Path
    src_dir: Path
    date: datetime

    @property
    def slug(self) -> str:
        """
        Returns a URL slug for the post.
        """
        # Remove the YYYY-MM-DD prefix which is required by Jekyll.
        # TODO(2026-01-20): Get rid of the requirement for this prefix.
        return re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)
