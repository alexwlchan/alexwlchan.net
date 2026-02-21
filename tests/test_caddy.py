"""
Tests for `mosaic.caddy`.
"""

from pathlib import Path

import pytest

from mosaic.caddy import parse_caddy_redirects, Redirect


@pytest.mark.parametrize(
    "line, redirect",
    [
        (
            "redir /old-path/ /new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
        (
            "  redir /old-path/ /new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
        (
            "\tredir /old-path/ /new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
        (
            "\tredir /old-path/ https://alexwlchan.net/new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
    ],
)
def test_parse_ignores_whitespace(
    tmp_path: Path, line: str, redirect: Redirect
) -> None:
    """
    The parser ignores whitespace at the start of a line.
    """
    redir_path = tmp_path / "redirects.Caddyfile"
    redir_path.write_text(line)
    assert parse_caddy_redirects(redir_path) == [redirect]


def test_parser_finds_domain(tmp_path: Path) -> None:
    """
    The parser finds domain names.
    """
    redir_path = tmp_path / "redirects.Caddyfile"
    redir_path.write_text(
        "books.alexwlchan.net {\n"
        "  redir / https://alexwlchan.net/book-reviews/\n"
        "  redir /reviews https://alexwlchan.net/book-reviews/\n"
        "}\n"
        "\n"
        "til.alexwlchan.net {\n"
        "  redir / https://alexwlchan.net/til/ permanent\n"
        "  redir /atom.xml https://alexwlchan.net/til/atom.xml permanent\n"
        "}"
    )
    assert parse_caddy_redirects(redir_path) == [
        Redirect(
            lineno=2, source="https://books.alexwlchan.net/", target="/book-reviews/"
        ),
        Redirect(
            lineno=3,
            source="https://books.alexwlchan.net/reviews",
            target="/book-reviews/",
        ),
        Redirect(lineno=7, source="https://til.alexwlchan.net/", target="/til/"),
        Redirect(
            lineno=8,
            source="https://til.alexwlchan.net/atom.xml",
            target="/til/atom.xml",
        ),
    ]
