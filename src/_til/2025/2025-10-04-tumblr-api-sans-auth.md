---
layout: til
title: Using the Tumblr v1 API doesn't require auth
summary: You can get information from `https://{username}.tumblr.com/api/read`.
date: 2025-10-04 06:46:34 +01:00
tags:
  - tumblr
---
I'm working on a project to get some data from Tumblr, and I wanted to use the Tumblr API.

Their docs mostly talk about the v2 API, which requires OAuth to get information about individual posts (which is what I wanted).
OAuth is complicated and fiddly and I wanted to avoid it if I could.

The [v1 API](https://www.tumblr.com/docs/en/api/v1) is still around and (mostly) works without authentication.
You can make a single GET request to get information about a blog, or by passing the `id` query parameter, a single post.
The API can return XML or JSON:

```console
$ curl 'https://staff.tumblr.com/api/read' --get --data 'id=769680688183164928' | xmllint --format -
<?xml version="1.0" encoding="UTF-8"?>
<tumblr version="1.0">
  <tumblelog name="staff" timezone="US/Eastern" uuid="t:0aY0xL2Fi1OFJg4YxpmegQ" title="Tumblr Staff"/>
  <posts start="0" total="2953">
    <post id="769680688183164928" url="https://staff.tumblr.com/post/769680688183164928" url-with-slug="https://staff.tumblr.com/post/769680688183164928/tumblr-theyre-here-communities-are-finally" type="Regular" date-gmt="2024-12-12 17:31:44 GMT" date="Thu, 12 Dec 2024 12:31:44" unix-timestamp="1734024704" format="html" reblog-key="VnDRK9a9" slug="tumblr-theyre-here-communities-are-finally" state="published" note-count="4647">
    …

$ curl 'https://staff.tumblr.com/api/read/json' --get --data 'id=769680688183164928'
var tumblr_api_read = {
  "tumblelog": {
    "title": "Tumblr Staff",
    "description": "",
    "name": "staff",
    …
```

However, the v1 API is an incomplete solution -- it only returns publicly accessible posts.
Tumblr blogs can choose to make their blogs visible only to logged-in users, in which case the API just returns a 404 Not Found.

It was useful for some quick and dirty crawling, but it's not a complete solution.
