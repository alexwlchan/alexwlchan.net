---
layout: til
title: Get the embedded artwork from an MP3 file
date: 2024-07-20 21:30:02 +01:00
summary: |
  Use the command `eyeD3 [MP3_FILE] --write-images [FOLDER]`.
tags:
  - ffmpeg
  - python:eyeD3
---
I had a collection of MP3 files from podcasts, and the MP3s had the show cover art embedded in the files.
I wanted to extract the cover art as standalone images.

Initially from Stack Overflow I was directed to this command:

```console
$ ffmpeg -i podcast_episode.mp3 -an -c:v copy cover_art.jpg
```

This mostly works, but it doesn't know about image formats -- for example, I ran it on one file and it created a PNG file with a `.jpg` extension.

I found a better command using the [eyeD3 Python library](https://pypi.org/project/eyed3/), which seems to get all the embedded artwork (including e.g. chapters) and writes them with file extensions that match the image format:

```console
$ eyeD3 podcast_episode.mp3 --write-images embedded_artwork
```
