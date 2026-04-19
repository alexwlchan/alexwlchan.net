"""
Posts are any dated content.
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Self

from pydantic import model_validator

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

    @property
    def slug(self) -> str:
        """
        Returns a URL slug for the post.
        """
        # Remove the YYYY-MM-DD prefix which is required by Jekyll.
        # TODO(2026-01-20): Get rid of the requirement for this prefix.
        return re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\-", "", self.md_path.stem)

    @model_validator(mode="after")
    def set_sharing_card(self) -> Self:
        """
        Find a sharing card for this post.
        """
        card_dir = self.src_dir / "images/cards" / str(self.date.year)

        png_candidate = card_dir / (self.slug + ".png")
        jpg_candidate = card_dir / (self.slug + ".jpg")

        png_exists = png_candidate.exists()
        jpg_exists = jpg_candidate.exists()

        if png_exists and not jpg_exists:
            self.card_path = png_candidate.relative_to(self.src_dir)
            return self
        elif not png_exists and jpg_exists:
            self.card_path = jpg_candidate.relative_to(self.src_dir)
            return self
        elif png_exists and jpg_exists:
            raise ValueError(f"multiple matching cards for {self.md_path}")

        return self
