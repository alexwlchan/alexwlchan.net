---
layout: note
title: How to do resumable downloads with curl
date: 2023-10-17 20:10:10 +00:00
date_updated: 2026-02-22 07:35:36 +00:00
topic: Shell scripting
summary: |
  You want the [`--continue-at -` flag](https://curl.se/docs/manpage.html#-C), which will resume the transfer from the size of the already-downloaded file.
---

Here's an example of using it to download a large file:

```bash
curl \
   --location \
   --remote-name \
   --continue-at - \
   https://dumps.wikimedia.org/other/wikibase/commonswiki/20231009/commons-20231009-mediainfo.json.bz2
```

It behaves in a "sensible" way at the beginning and end of the download:

*   If you haven't downloaded anything yet, it starts downloading from the first byte of the remote file.
*   If you've already downloaded the complete file, it stops as soon as it checks the byte count with the remote server.
