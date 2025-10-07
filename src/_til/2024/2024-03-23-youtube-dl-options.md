---
layout: til
date: 2024-03-23 07:03:19 +0000
title: My config for running youtube-dl
summary: The flags and arguments I find useful when I’m using youtube-dl.
tags:
  - yt-dlp
---

youtube-dl has a lot of options, and I only use a small subset of them.
These are some notes on the flags I find most useful.

## Downloading subtitles

I've gotten in the habit of downloading subtitles for any videos I download, and I'm gradually backfilling subtitles for any videos I downloaded in the past.

Even if I don't use subtitles (at least, not right now), they're very small and it might be useful to have them as an easily searchable index of downloaded videos.

For consistency, I'm downloading all my subtitles as SRT.
I'm not sure which subtitle format is "best", but I already have hundreds of SRT files lying around and it feels good to be consistent.

Here's how to download subtitles with a video:

```console
$ youtube-dl --write-subs --convert-subtitles=srt "$VIDEO_URL"
```

Not all YouTube videos have subtitles supplied by the uploader, but YouTube themselves can autogenerate subtitles that they've added to a lot of videos.
Here's how to download those:

```
$ youtube-dl --write-subs --write-auto-subs --convert-subtitles=srt "$VIDEO_URL"
```

According to the youtube-dl help text, this is only for YouTube.

## Removing video ID from the filename

When you download a video with the default options, the video ID is appended as a suffix in brackets, for example `Wind turbines [DeHfYHZrgDc].webm`.
I don't always want that ID in the filename.
I could remove it afterwards, but it'd be nicer if it wasn't there at all.

You can choose how to name the downloaded file with the `-o`/`--output` flag, for example:

```console
$ youtube-dl --output "%(title)s.%(ext)s" "$VIDEO_URL"
```