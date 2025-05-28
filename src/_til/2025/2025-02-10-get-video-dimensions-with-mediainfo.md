---
layout: til
title: Get the dimensions of a video file with `mediainfo`
date: 2025-02-10 10:10:51 +0000
tags:
  - video
---
Here are two examples:

```console
$ mediainfo '--Inform=Video;%Width%' speech.mp4
640

$ mediainfo '--Inform=Video;%Height%' speech.mp4
360
```
