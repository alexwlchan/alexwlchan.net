---
layout: page
title: Changelog
---

## September 2024

*   Hide the background texture when you print the page.
*   Fix a bug where Python console sessions weren't being highlighted in TIL posts.

## August 2024

*   Remove Twitter from my contact page.
*   Fix an invalid value in the X-Frame-Options header.
    I was returning `ALLOW`, but I should have been returning `ALLOWALL`.

## June 2024

*   Add syntax highlighting [for Python console sessions](/til/2024/how-to-highlight-python-console-in-jekyll/).
*   Add a `utm_source` parameter to links in the RSS feed, so I can track how many people are reading via RSS.
*   Allow serving the site in an `<iframe>` by changing the X-Frame-Options header from `DENY` to `ALLOW`.
*   De-duplicate styles for inline SVGs, to reduce page weight.
*   Fix a bug where embedded YouTube videos were appearing too wide on mobile devices.
*   Fix a bug where inline SVGs had empty `<defs>` tags.
*   Remove all uses of `polyfill.io` because of a supply chain attack, and serve the JavaScript directly from this domain only. (This only affected a single page.)

commit 154565731ae7b4c4fe977c14d66d4f44ed1d9f0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 26 09:50:55 2024 +0100

    Add a snippet to highlight missing alt text

commit 6bfd8a148e79bc1b4ee6188feac0cb9378d68b39
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 22 08:31:06 2024 +0100

    Remove this balance style; I don't actually like it
