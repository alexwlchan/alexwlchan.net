---
layout: article
date: 2026-05-02 07:08:53 +01:00
title: Using Playwright to test my static sites
topics:
  - Software testing
  - Static websites
---
{#
  Social sharing image from https://www.pexels.com/photo/yellow-and-purple-masquerade-masks-8404571/
#}

I build a lot of static websites -- including this site and all of my [local media archives][tiny-archives] -- and I want to test them.
Most of my pages are static HTML and I can write automated tests that analyse the HTML, but for more complex sites I have JavaScript that runs in the browser and modifies the page.
The only way to test that functionality is to open the page in a browser, click around, and see what happens.
I could do that manually, but it quickly gets tedious.

To automate this process, I've been using a testing framework called [Playwright][playwright], which is designed for this sort of end-to-end testing.
It's a tool that allows you to programatically control a web browser, [look at the contents of a page][screenshots], and make assertions about what's there.
Playwright can be used to test or script any kind of web app; I'm using it for static sites because those are the only web apps I have.

Playwright is available as a CLI, or there are libraries to use it with TypeScript, Python, .NET, and Java.
All my other tests are written in Python, so that's what I'm using.

## Writing a basic test with Playwright

To [set up Playwright][playwright-install] with Python, you install the [playwright library][pypi-playwright] using `pip` or `uv`, then install a web browser for Playwright to control.
(You can't use Playwright with the browser you use day-to-day; you need special binaries with control hooks.)

I use Safari as my main browser, and Safari is based on WebKit, so let's install that:

```console
$ uv pip install playwright
$ python3 -m playwright install webkit
```

Then we can start writing tests.
Here's a basic test in which Playwright launches WebKit, opens `example.com`, and checks the text `Example domain` is visible on the page:

```python {"names":{"1":"playwright","2":"sync_api","3":"expect","4":"sync_playwright","5":"test_basic_playwright","7":"p","8":"browser","12":"page"}}
from playwright.sync_api import expect, sync_playwright


def test_basic_playwright() -> None:
    """
    Run a basic test with Playwright: load a web page and check it
    contains the expected text.
    """
    with sync_playwright() as p:
        browser = p.webkit.launch()

        page = browser.new_page()
        page.goto("https://example.com/")
        expect(page.get_by_text("Example domain")).to_be_visible()

        browser.close()
```

For a larger app, you might run your tests with multiple browsers to check compatibility -- Playwright supports lots of other browsers, including Chromium, Firefox, and Mobile Safari in emulation.
I'm just testing private sites where I'm the only user, so a single browser is fine.

This test passes in about half a second on my computer.
That's fine for a single test, but it would add up if I had lots of tests, each starting and stopping the browser every time.
It would be nice to make that process faster, and to reduce some of the boilerplate as well.

## A pair of Playwright fixtures

To reduce the repetition and reuse the browser instance, I have a couple of [pytest fixtures][pytest-fixtures] to simplify things.

The first is a session-scoped fixture that starts the browser at the start of the test run, and closes it when I'm done:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"playwright","5":"sync_api","6":"Browser","7":"sync_playwright","8":"pytest","12":"browser","16":"p","17":"webkit"}}
from collections.abc import Iterator

from playwright.sync_api import Browser, sync_playwright
import pytest


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """
    Launch an instance of WebKit to interact with in tests.
    """
    with sync_playwright() as p:
        webkit = p.webkit.launch()
        yield webkit
        webkit.close()
```

Because this is a session-scoped fixture, it only runs once per test suite -- that means the browser is only started once, then the same instance is reused for all the tests.
This makes a large test suite significantly faster.

My other fixture is a bit more complicated -- it gives you a page to interact with, and at the end of the test it checks the page didn't have any warnings or errors.
This is a strict approach, which helps me spot errors in areas I wasn't explicitly testing.
Here's the fixture:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"playwright","5":"sync_api","6":"Browser","7":"Page","8":"pytest","12":"page","13":"browser","17":"p","20":"console_messages","27":"page_errors","35":"console_errors","38":"msg"}}
from collections.abc import Iterator

from playwright.sync_api import Browser, Page
import pytest


@pytest.fixture(scope="function")
def page(browser: Browser) -> Iterator[Page]:
    """
    Open a new page in the browser.
    
    If there are any errors or warnings when loading the page, the test
    will fail when this fixture is cleaned up.
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
```

These two fixtures allow for tighter, faster tests, focusing on what the test is actually checking.
Here's the example test, rewritten to use this fixture:

```python {"names":{"1":"test_playwright_with_fixture","2":"page"}}
def test_playwright_with_fixture(page: Page) -> None:
    """
    Run a test using my Playwright fixture: load a web page, check it
    contains the expected test, and check it loads without errors.
    """
    page.goto("https://example.com/")
    expect(page.get_by_text("Example domain")).to_be_visible()
```

I use the `page` fixture for most tests, where I want to spot any unexpected errors or warnings.
If I'm testing error handling specifically, I use the `browser` fixture and create a new page which isn't treated as strictly.

## Getting file:/// URIs for Playwright

Normally Playwright is used with `http:` and `https:` URLs, but my static websites are stored as HTML files on my local disk, and I often open them with `file:` URLs.

I could spin up a web server in my tests, but that's extra overhead and might affect the results -- there are [subtle differences][file-vs-http] between how browsers handle pages opened with `file:` vs `http:`.

To convert file paths to `file:` URLs, I use the [`pathname2url` function][pydoc-pathname2url] from the `urllib.request` module.
I combine this with [`os.path.abspath`][pydoc-abspath] to get a full URL I can pass to Playwright:

```pycon {"names":{"1":"os","2":"path","3":"abspath","4":"urllib","5":"request","6":"pathname2url","7":"path"}}
>>> from os.path import abspath
>>> from urllib.request import pathname2url
>>> path = "index.html"
>>> pathname2url(abspath(path), add_scheme=True)
'file:///Users/alexwlchan/repos/alexwlchan.net/index.html'
```

## Assertions in Playwright

Playwright has a different set of assertion helpers to regular Python tests, and it takes some getting used to -- I still have to consult the documentation when I write new tests.

Here are examples of assertions I've written using Playwright:

*   Testing that a redirect is working:

    ```python {"names":{"1":"resp"}}
    resp = page.goto("https://alexwlchan.net/projects/chives/files/doesnotexist.txt")
    
    assert resp is not None
    assert resp.status == 200
    assert resp.url == "https://alexwlchan.net/projects/chives/files/?missing=doesnotexist.txt"    
    ```

*   Test that text does or does not appear on a page:

    ```python {"names":{"1":"playwright","2":"sync_api","3":"expect"}}
    from playwright.sync_api import expect
    
    page.goto("https://www.example.com")
    
    expect(page.get_by_text("Example Domain")).to_be_visible()
    expect(page.get_by_text("Alex Chan")).not_to_be_visible()
    ```
    
    or:
    
    ```python
    assert "Example Domain" in page.content()
    assert "Alex Chan" not in page.content()
    ```

*   Locate an element with a CSS selector, and check it does or doesn't appear on a page:

    ```python
    page.goto("https://www.example.com")

    expect(page.locator("h1")).to_be_visible()
    expect(page.locator("h2.title")).not_to_be_visible()
    ```

*   Locate an element, and make assertions about its attributes:

    ```python
    page.goto("https://www.example.com")
    
    href = page.locator("a").first.get_attribute("href")
    assert href == "https://iana.org/domains/example"
    ```

*   Locate an element, and make assertions about the text it contains:

    ```python
    page.goto("https://www.example.com")
    
    assert page.locator("a").inner_text() == "Learn more"
    ```

*   Check that an element with particular inner text is visible on the page:

    ```python
    page.goto("https://www.example.com/")
    
    expect(page.locator('//h1[text()="Example Domain"]')).to_be_visible()
    ```

*   Locate an element immediately following a different element.
    I've used this a couple of times when I have tables or definition lists with a label in one element, and a value in another:
    
    ```python {"names":{"1":"dt_locator","4":"next_dd"}}
    dt_locator = page.locator('//dt[text()="Profile page:"]')
    next_dd = dt_locator.locator("xpath=following-sibling::*")

    assert (
        next_dd.inner_html().strip()
        == '<a href="https://www.flickr.com/photos/nasahqphoto/">NASA HQ PHOTO</a>'
    )
    ```

*   Check the number of matching elements on a page; for example, the length of a list:

    ```python
    page.goto("https://alexwlchan.net/articles/")
    
    assert page.locator("#list_of_posts li").count() >= 10
    ```

*   Check the title of the page:

    ```python
    page.goto("https://www.example.com/")
    
    assert page.title() == "Example Domain"
    ```

*   Check the behaviour of the page when [JavaScript is disabled][playwright-disable-js]:

    ```python {"names":{"1":"context","5":"page","12":"noscript_elem"}}
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()

    expect(page.locator("noscript .error")).to_be_visible()

    noscript_elem = page.locator("noscript .error")
    assert noscript_elem.inner_text() == "You must enable JavaScript to use this page."
    ```

This is just a fraction of what Playwright can do; it can be used to build far more complicated tests that walk through a web app and test multi-step user flows.
I'm only using it to make assertions about snippets of JavaScript, but it's still useful.

For a long time, I told myself that my static sites were simple enough not to need testing, but that didn't prevent bugs from slipping in, and it limited what I could build.
Now I can write proper tests for my sites, I can be more confident I haven't broken anything, I can experiment faster, and I can try more ambitious ideas.

[file-vs-http]: /2025/learning-how-to-make-websites/#file_uris
[tiny-archives]: /digital-preservation/tiny-archives/
[playwright]: https://playwright.dev/
[playwright-disable-js]: https://playwright.dev/python/docs/api/class-browser#browser-new-context-option-java-script-enabled
[playwright-install]: https://playwright.dev/docs/intro
[pydoc-abspath]: https://docs.python.org/3/library/os.path.html#os.path.abspath
[pydoc-pathname2url]: https://docs.python.org/3/library/urllib.request.html#urllib.request.pathname2url
[pypi-playwright]: https://pypi.org/project/playwright/
[pytest-fixtures]: https://docs.pytest.org/en/stable/explanation/fixtures.html
[screenshots]: /2024/scheduled-screenshots/
