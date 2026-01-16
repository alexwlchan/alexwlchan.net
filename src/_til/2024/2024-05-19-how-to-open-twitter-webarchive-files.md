---
layout: til
date: 2024-05-19 22:24:10 +01:00
title: Open a Safari webarchive from Twitter/X without being redirected
summary: |
  Disabling JavaScript when you open the webarchive file will prevent you from redirecting you to twitter.com.
tags:
  - safari
  - digital preservation
---
Suppose you save a Safari webarchive from Twitter/X.
When you try to open it, the scripts on the page will detect that you're not logged in, and try to redirect you back to `twitter.com`/`x.com`.
This is quite annoying!

This happens with JavaScript on the page, so you can get round it by disabling JavaScript.
Two ways to do this:

1.  Disable JavaScript in your browser when you open the file, so none of the `<script>` tags get executed.

2.  Create a modified version of the webarchive file that doesn't have any JavaScript `<script>` tags.
    Safari webarchive files are [binary plists](/til/2024/whats-inside-safari-webarchive/), so we can open them up, modify their contents, and repack them.

    Here's a Python script that does just that:

    ```python
    """
    Create a copy of a Safari webarchive file that disables all the ``<script>`` tags.
    """

    import pathlib
    import plistlib
    import sys


    if __name__ == "__main__":
        try:
            path = pathlib.Path(sys.argv[1])
        except IndexError:
            sys.exit(f"Usage: {__file__} PATH")

        assert path.suffix == ".webarchive"
        nojs_path = path.with_suffix(".nojs.webarchive")
        assert nojs_path != path

        with open(path, "rb") as in_file:
            webarchive = plistlib.load(in_file)

        old_html = webarchive["WebMainResource"]["WebResourceData"]
        nojs_html = old_html.replace(b"<script", b'<script type="application/json"')
        webarchive["WebMainResource"]["WebResourceData"] = nojs_html

        with open(nojs_path, "xb") as out_file:
            plistlib.dump(webarchive, out_file, fmt=plistlib.FMT_BINARY)

        print(nojs_path)
    ```

    You could also grab a copy of the `nojs_html` and save it to a separate HTML file if that's helpful.
