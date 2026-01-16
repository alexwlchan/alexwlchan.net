"""
Tests for `mosaic.css`.
"""

from mosaic.css import create_base_css


def test_css_has_no_imports() -> None:
    """
    The generated CSS has resolved all the @import statements.
    """
    assert "@import" not in create_base_css("css/style.css")
