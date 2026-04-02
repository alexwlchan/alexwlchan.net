"""
Posts are any dated content.
"""

from datetime import datetime
from pathlib import Path


from ._base import BaseHtmlPage


class Post(BaseHtmlPage):
    """
    An article is a long-form piece of writing, usually with original thought.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a BookReview.
    md_path: Path
    src_dir: Path
    date: datetime
