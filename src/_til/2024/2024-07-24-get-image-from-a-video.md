---
layout: til
title: Get an image from a video with ffmpeg
date: 2024-07-24 21:17:35 +01:00
tags:
  - ffmpeg
---
I had some video files, and I wanted to extract an image from the video to use as a thumbnail.

This is the `ffmpeg` command I used, which extracts a single frame from a given timestamp:

```console
$ ffmpeg -i video.mp4 -ss 01:02:03.000 -vframes 1 thumbnail.png
```
