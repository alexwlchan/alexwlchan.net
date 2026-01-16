---
layout: til
title: Downloading avatars from Tumblr
date: 2025-02-09 22:19:32 +00:00
date_updated: 2025-08-18 21:25:55 +01:00
summary: |
  There's an API endpoint that lets you download avatars in a variety of sizes.
tags:
  - tumblr
---
<style>
  blockquote > pre {
    margin-left:  0;
    margin-right: 0;
    padding: 0;
    border: none;
    background: none;
  }
</style>

I'm working on a project where I need to download Tumblr avatars.
The Tumblr API has [an endpoint](https://www.tumblr.com/docs/en/api/v2#avatar--retrieve-a-blog-avatar) precisely for this:

> **`/avatar` — Retrieve a Blog Avatar** <br>
> You can get a blog's avatar in 9 different sizes. The default size is 64x64.
>
> Examples
>
> <pre><code>https://api.tumblr.com/v2/blog/david.tumblr.com/avatar/512
> https://api.tumblr.com/v2/blog/david.tumblr.com/avatar</code></pre>

This URL will redirect you to the location of the actual image file -- the avatar URL in the example above redirects to `https://64.media.tumblr.com/avatar_fdf0635a9d74_512.png`.

Most avatars are PNG, but I've seen a handful of avatars in other formats.

Here's a Python snippet I wrote which will download the avatars to a filename with the appropriate extension:

```python
from pathlib import Path

import httpx


def download_tumblr_avatar(blog_identifier: str) -> Path:
    """
    Download an avatar from Tumblr, and return a path to
    the downloaded file.
    """
    resp = httpx.get(
        f"https://api.tumblr.com/v2/blog/{blog_identifier}/avatar/512",
        follow_redirects=True,
    )
    resp.raise_for_status()

    content_type = resp.headers["content-type"]

    ext_mapping = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }

    try:
        ext = ext_mapping[content_type]
    except KeyError:
        raise RuntimeError(f"Unexpected Content-Type: {content_type!r}")

    dl_path = f"{blog_identifier}.{ext}"

    with open(dl_path, "xb") as out_file:
        out_file.write(resp.content)

    return dl_path


if __name__ == "__main__":
    print(download_tumblr_avatar(blog_identifier="david.tumblr.com"))
    print(download_tumblr_avatar(blog_identifier="staff"))
    print(download_tumblr_avatar(blog_identifier="marco"))
    print(download_tumblr_avatar(blog_identifier="t:WX5xItRbCiJH_GJDsIdhAQ"))
```
