---
layout: til
title: "How do Dreamwidth posts IDs work?"
summary: |
  They were deliberately non-sequential as an anti-spam technique.
  It's no longer required, but it's in the codebase now and hasn't been changed since it was written.
date: 2019-05-11 23:26:38 +01:00
tags:
  - dreamwidth
---

Dreamwidth IDs (posts, comments) don't increment one-by-one, but via algebraic manipulations. Comments don't go 1, 2, 3, they go 256, 540, 721, whatever.

The exact pattern is [something like](https://github.com/dreamwidth/dw-free/blob/2c5f1a9a11efbcf43a9eaa73a6ae43a533ec439d/cgi-bin/DW/Collection.pm#L54):

```
display_id = collection_id * 256 + internal_id
```

This is an old anti-bot measure: if a bot saw URLs with `/1.html`, `/2.html`, `/3.html`, it assumes it's a sequence and continues in progression, which could overwhelm the site.
These days it's not needed (hooray CDNs!) but it's baked into the site now.
