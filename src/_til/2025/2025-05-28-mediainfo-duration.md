---
layout: til
title: Get the duration of a video file with `mediainfo`
summary: Use `mediainfo --Inform='Video;%Duration%' [VIDEO_FILE]`.
date: 2025-05-28 19:24:07 +0100
tags:
  - video
---
Here's an example:

```console
$ mediainfo --Inform='Video;%Duration%' speech.mp4
5658174
```

This returns the length of the video in milliseconds: 5,658,174 milliseconds is 5,658 seconds, or 1h&nbsp;34m&nbsp;18s.
