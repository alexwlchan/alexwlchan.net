---
layout: page
title: Changelog
---

### March 2025

Notable changes:

*   I added "new" banners to articles I've written recently, and any new articles will be pinned to the homepage for several weeks.
    Previously, the homepage was just a random selection of six articles I'd written at any time.

    I wrote more about this change in [An unexpected lesson in CSS stacking contexts](/2025/new-banner/).

Bugfixes and small improvements:

*   Add a `title` attribute to the `<iframe>` elements for embedded YouTube videos.
*   Reduce the permissions given to embedded YouTube videos, which should reduce the amount of tracking by Google.
*   Cards on the articles page (`/articles/`) will now rearrange themselves if you resize the window.
    Previously, they'd be laid out based on the width when the page was loaded, and they could look weird if you resized the window.
*   Fix a hover state bug in my embedded tweets.
    If you hovered over a quoted tweet, all the text would be underlined.
    It's not meant to be, and now it isn't.
*   Reduce the size of the homepage (`/`) by 50% and list of articles (`/articles/`) by 5% by tightening up the size of article cards.

## February 2025

Notable changes:

*   Add [good embedded toots](/2025/good-embedded-toots/) for embedding Mastodon posts with lightweight HTML and CSS.

Bugfixes and small improvements:

*   I tidied up the appearance of "block" elements like code blocks and blockquotes.
    Previously they used the per-page tint colour as a background, but now they use a consistent shade of grey in the background.
    I wrote about this change in [Making all the roundrects consistent](/2025/style-updates-2025#making-all-the-roundrects-consistent).
