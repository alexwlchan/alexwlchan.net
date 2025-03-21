---
layout: page
title: Changelog
---

### March 2025

Small improvements:

*   Add a `title` attribute to the `<iframe>` elements for embedded YouTube videos.
*   Reduce the permissions given to embedded YouTube videos, which should reduce the amount of tracking by Google.
*   Cards on the articles page (`/articles/`) will now rearrange themselves if you resize the window.
    Previously, they'd be laid out based on the width when the page was loaded, and they could look weird if you resized the window.
*   Fix a hover state bug in my embedded tweets.
    If you hovered over a quoted tweet, all the text would be underlined.
    It's not meant to be, and now it isn't.