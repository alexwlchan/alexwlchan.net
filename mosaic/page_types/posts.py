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

    # Whether this post should be featured in the site-wide indexes
    is_featured: bool = False

    # Whether this post should be excluded from the site-wide indexes
    is_excluded: bool = False

    @property
    def slug(self) -> str:
        """
        Returns a URL slug for the post.
        """
        return re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)
