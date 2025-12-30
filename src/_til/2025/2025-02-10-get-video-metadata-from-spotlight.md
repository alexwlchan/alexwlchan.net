---
layout: til
title: Get video dimensions on macOS with built-in tools
date: 2025-02-10 09:43:42 +0000
summary: |
  If the video file is indexed by Spotlight, you can use `mdls` to get the width and `height` of a video file.
tags:
  - macos
  - video
is_unlisted: true
---
You can look up Spotlight metadata attributes with the [`mdls` command][mdls], which allows you to get the dimensions of video files:

```console
$ mdls -name kMDItemPixelWidth -raw speech.mp4
640⏎

$ mdls -name kMDItemPixelHeight -raw speech.mp4
360⏎
```

However, this only works for files indexed by Spotlight.
If the video file is somewhere that's excluded by Spotlight, e.g. a temporary directory, this won't work:

```console
$ mdls -name kMDItemPixelWidth -raw /tmp/speech.mp4
(null)⏎

$ mdls -name kMDItemPixelHeight -raw /tmp/speech.mp4
(null)⏎
```

{% update 2025-12-05 %}
   This doesn't account for videos which have a non-trivial pixel aspect ratio. For a more reliable way to get the dimensions of a video, see [The square pixels that aren't square](/2025/square-pixels).
{% endupdate %}

[mdls]: https://alexwlchan.net/man/man1/mdls.html
