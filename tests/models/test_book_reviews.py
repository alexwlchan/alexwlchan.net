"""
Tests for `mosaic.models.book_reviews`.
"""

import pytest

from mosaic.models import BookContributor, book_attribution


@pytest.mark.parametrize(
    "contributors, attribution",
    [
        ([BookContributor(name="Jean-Luc Ficard")], "by Jean-Luc Ficard"),
        (
            [BookContributor(name="Emily Ficinson", role="editor")],
            "edited by Emily Ficinson",
        ),
        (
            [
                BookContributor(name="Faye N. Dom"),
                BookContributor(name="Diana Prints", role="translator"),
            ],
            "by Faye N. Dom",
        ),
        (
            [
                BookContributor(name="Faye N. Dom"),
                BookContributor(name="Diana Prints", role="editor"),
            ],
            "by Faye N. Dom",
        ),
        (
            [
                BookContributor(name="Faye N. Dom"),
                BookContributor(name="Diana Prints", role="narrator"),
            ],
            "by Faye N. Dom",
        ),
        (
            [
                BookContributor(name="Mr Milkshake", role="retold by"),
                BookContributor(name="Anne Onymous", role="illustrator"),
            ],
            "retold by Mr Milkshake",
        ),
        (
            [
                BookContributor(name="Mr Milkshake", role="compiled by"),
                BookContributor(name="Anne Onymous", role="illustrator"),
            ],
            "compiled by Mr Milkshake",
        ),
    ],
)
def test_attribution_line(
    contributors: list[BookContributor], attribution: str
) -> None:
    """
    Tests for `attribution_line`.
    """
    assert book_attribution(contributors) == attribution
