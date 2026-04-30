"""
Integration tests for the site.

Given a built instance of the site, run a Caddy web server and interact
with it using Playwright. This assumes there's a pre-built instance of
the site in `_out`.
"""

from collections.abc import Iterator

from playwright.sync_api import Browser, Page, expect, sync_playwright
import pytest

from mosaic import caddy
from mosaic.git import git_root


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """
    Launch an instance of WebKit we can interact with in tests.
    """
    with sync_playwright() as p:
        browser = p.webkit.launch()
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Iterator[Page]:
    """
    Open a new page in the browser which we can interact with.

    This fixture will check that the page loads with no errors or warnings.
    """
    p = browser.new_page()

    # Capture anything that gets logged to the console.
    console_messages = []
    p.on("console", lambda msg: console_messages.append(msg))

    # Capture any page errors
    page_errors = []
    p.on("pageerror", lambda err: page_errors.append(err))

    yield p

    # Check there weren't any console errors logged to the page.
    console_errors = [
        msg.text
        for msg in console_messages
        if msg.type == "error" or msg.type == "warning"
    ]
    assert console_errors == []

    # Check there weren't any page errors
    assert page_errors == []


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    """
    Run a local web server using Caddy, which is only running during tests.
    """
    out_dir = git_root() / "_out"
    port = 7575

    with caddy.local_webserver(out_dir, port) as url:
        yield url.rstrip("/")


def test_git_file_not_found(base_url: str, page: Page) -> None:
    """
    If we look up a non-existent Git file, we get redirected to /files/
    and see an error about the missing file.
    """
    resp = page.goto(base_url + "/projects/chives/files/does/not/exist.txt")

    assert resp is not None
    assert resp.status == 200
    assert resp.url == base_url + "/projects/chives/files/?missing=does/not/exist.txt"

    expect(page.get_by_text("File not found:")).to_be_visible()
    expect(page.get_by_text("does/not/exist.txt")).to_be_visible()
