---
layout: note
date: 2026-05-06 19:27:20 +01:00
title: Testing the width of a page on a mobile device using Playwright
summary: Create a new browser context with a narrow screen, then get `document.body.scrollWidth` to get the width of the displayed page.
topics:
  - Software testing
  - Blogging about blogging
hidden_topics:
  - Playwright
---
One perennial source of bugs on this site is incorrect page widths on mobile devices: something isn't wrapping or cropping properly, and it forces the whole page to be too wide.

For a long time I've been playing whack-a-mole with these bugs, but after writing about [using Playwright][using-playwright], I realised I could write a regression test.

Here's the approximate test I came up with.
It creates a new browser context with a mobile screen size, opens the page I'm interested in, then runs some JavaScript on the page to measure the scroll width:

```python {"names":{"1":"test_page_is_right_size_on_narrow_screens","2":"browser","4":"base_url","6":"width","7":"height","8":"context","14":"page","20":"scroll_width"}}
def test_page_is_right_size_on_narrow_screens(browser: Browser, base_url: str) -> None:
    """
    Check that on narrow screens, pages size to fit the screen.

    This is a regression test for issues I've had in the past where
    some wide element breaks the page when the window is narrower than it.
    """
    width = 350
    height = 650

    context = browser.new_context(viewport={"width": width, "height": height})

    page = context.new_page()
    page.goto(base_url + "/computers-and-code/")

    scroll_width = page.evaluate("document.body.scrollWidth")

    assert scroll_width == width
```

I don't think I'd want to write a regression test for every CSS change, but it's cool I can do it for this class of especially annoying bugs.

[using-playwright]: /2026/playwright/
