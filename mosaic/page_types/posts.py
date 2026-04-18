"""
Posts are any dated content.
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Self

from pydantic import model_validator

from mosaic.fs import find_paths_under
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

        try:
            matching_cards = [
                p.relative_to(self.src_dir)
                for p in find_paths_under(card_dir)
                if p.stem == self.slug
            ]
        except FileNotFoundError:
            return self

        if len(matching_cards) == 0:
            return self
        elif len(matching_cards) == 1:
            self.card_path = matching_cards[0]
            return self
        else:
            raise ValueError(f"multiple matching cards for {self.md_path}")
