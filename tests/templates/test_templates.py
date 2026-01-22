"""
Tests for `mosaic.templates`.
"""

from pathlib import Path


from mosaic import templates as t


def test_liquid_comments_are_ignored(tmp_path: Path) -> None:
    """
    Test that Liquid style comments get removed.
    """
    env = t.get_jinja_environment(src_dir=tmp_path / "src", out_dir=tmp_path / "out")
    tmpl = env.from_string(
        "Hello world!\n"
        "{% comment %}don’t show this{% endcomment %}\n"
        "Blue and yellow makes green\n"
        "{% comment %}don't show this either{% endcomment %}\n\n"
        "Red and yellow makes orange"
    )

    assert tmpl.render() == (
        "Hello world!\nBlue and yellow makes green\n\nRed and yellow makes orange"
    )
