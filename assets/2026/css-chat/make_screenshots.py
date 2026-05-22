#!/usr/bin/env python3
"""
Create screenshots of HTML pages (https://alexwlchan.net/2026/css-chat/).
"""

import os
from urllib.request import pathname2url

from playwright.sync_api import sync_playwright


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.webkit.launch()
        context = browser.new_context(device_scale_factor=2)
        page = context.new_page()

        for filename in ("chat1", "chat2", "chat3", "chat4", "chat5", "chat6"):
            absolute_path = os.path.abspath(f"{filename}.html")
            file_uri = pathname2url(absolute_path, add_scheme=True)
            page.goto(file_uri)

            if filename == "chat1":
                width, height = 600, 500
            else:
                width, height = 500, 574

            page.screenshot(
                path=f"{filename}.png",
                full_page=True,
                clip={"x": 0, "y": 0, "width": width, "height": height},
            )

        browser.close()
