---
layout: post
date: 2020-07-12 07:34:45 +0000
title: How to do parallel downloads with youtube-dl
tags: shell-scripting
---

I'm a regular user of [youtube-dl](http://ytdl-org.github.io/youtube-dl/), a command-line program for downloading videos from YouTube (and other sites).
You can use youtube-dl to download individual videos, or you can ask it to download an entire playlist.
When it's downloading a playlist, it downloads the individual videos one-by-one, which isn't particularly fast.

Here's a shell snippet that downloads playlist videos in parallel, which is faster:

```shell
youtube-dl --get-id "$PLAYLIST_URL" \
  | xargs -I '{}' -P 5 youtube-dl 'https://youtube.com/watch?v={}'
```

The first command (`--get-id`) gets a list of video IDs in the playlist, one per line.
Those IDs get piped to [xargs](https://linux.die.net/man/1/xargs), which calls individual instances of youtube-dl to download each video.
Because I'm passing `-P 5` to xargs, it runs up to 5&nbsp;parallel instances of youtube-dl at a time.

In some informal testing as I was writing this post, I downloaded the same 10 video playlist twice.
One-by-one: 3m&nbsp;30s.
In parallel: 35s.
