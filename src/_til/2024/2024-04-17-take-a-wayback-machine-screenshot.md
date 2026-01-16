---
layout: til
date: 2024-04-17 22:43:30 +01:00
title: How to take a screenshot of a page in the Wayback Machine
summary: |
  Using Playwright to take screenshots and adding some custom styles gets a screenshot of a page without the Wayback Machine overlay.
tags:
  - screenshots
  - playwright
  - wayback machine
---
As part of my [daily screenshots project][daily_screenshots], I wanted to get screenshots of all the versions of my site that are saved in the Wayback Machine.

I found [an article on ScrapingBee][scraping_bee] which explains how to take screenshots using Playwright, but if you run it against a Wayback Machine URL, you get their little overlay that gives you information about the captures:

{%
  picture
  filename="wayback_machine_overlay.png"
  width="640"
  class="screenshot"
  alt="Top of a page saved by the Wayback Machine. There's a white panel which sits above the page, which tells you a bit about the Wayback Machine captures – when the page was saved, how many times it’s been saved, and so on."
%}

I wanted to remove that overlay in my screenshots.
I could crop it out after the fact, but it casts a small drop shadow on the content.
Is there a better way?

Yes!

The [`Page.screenshot()` method][page_screenshot] takes a `style` argument, which is a stylesheet that gets applied to the page before Playwright takes a screenshot.
By adding a rule that hides the Wayback Machine overlay, I can get a screenshot of just the original page:

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    url = "https://web.archive.org/web/20240404013713/https://alexwlchan.net/"

    page.goto(url)
    page.wait_for_load_state("networkidle")
    page.screenshot(
        path="screenshot.png",
        full_page=True,
        timeout=30000.0,
        style="""
            #wm-ipp-base { display: none !important; }
        """,
    )
```

The other options may not be strictly necessary, and were just useful for getting successful screenshots of my website.

[daily_screenshots]: https://github.com/alexwlchan/daily-screenshots
[scraping_bee]: https://www.scrapingbee.com/webscraping-questions/playwright/how-to-take-screenshot-with-playwright/
[page_screenshot]: https://playwright.dev/python/docs/api/class-page#page-screenshot
