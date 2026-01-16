---
layout: til
title: "SVGs are only rendered on GitHub if you use an `<img>` that points to another file"
date: 2024-01-04 22:07:01 +00:00
tags:
  - svg
  - github
---
I was trying to write a Markdown file to render on GitHub, and include an SVG file.

You need to insert an `<img>` tag that links to the SVG elsewhere.

This works for both inline links (to files in the same repository) and external links (to files not hosted on GitHub):

```
<img src="./another_file_in_the_repo.svg">
<img src="https://example.net/my_great_image.svg">

![](./another_file_in_the_repo.svg)
![](https://example.net/my_great_image.svg)
```

## What doesn't work

Here are two approaches I tried that **don't** work:

*   Insert the `<svg>` tag directly into the Markdown:

    ```markdown
    This is the image I'm about to use:

    <svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
      …
    </svg>

    This is a description of the image I just used.
    ```

    This works in certain environments (e.g. my blog, the Marked.app Markdown preview) but not on GitHub.

    GitHub's Markdown renderer completely skips the `<svg>` element – you get two `<p>` elements for the text either side, but nothing in between.
    I'm guessing that's for security reasons, to avoid a malicious SVG wrecking havoc on the rest of the page.

*   Insert an `<img>` tag with a base64-encoded SVG:

    ```markdown
    This is the image I'm about to use:

    <img src="src="data:image/svg+xml;base64,PHN2…">

    This is a description of the image I just used.
    ```

    In this case GitHub will render an `<img>` tag, but it has an empty `src` attribute.

