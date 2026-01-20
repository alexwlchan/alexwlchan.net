---
layout: til
title: Get the dimensions of a video file with `mediainfo`
date: 2025-02-10 10:10:51 +00:00
tags:
  - video
index:
  exclude: true
---
Here are two examples:

```console
$ mediainfo '--Inform=Video;%Width%' speech.mp4
640

$ mediainfo '--Inform=Video;%Height%' speech.mp4
360
```

{% update date="2025-12-05" %}
   This doesn't account for videos which have a non-trivial pixel aspect ratio. For a more reliable way to get the dimensions of a video, see [The square pixels that aren't square](/2025/square-pixels).
{% endupdate %}
