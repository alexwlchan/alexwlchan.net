---
layout: post
title: Creating a personal wrapper around yt-dlp
summary: I've written a new script which calls yt-dlp with my preferred options, so I don't have to copy my configuration across different projects.
tags:
  - yt-dlp
  - my tools
---
I download a lot of videos from YouTube, and [yt-dlp] is my tool of choice.
Sometimes I download videos as a one-off, but more often I'm downloading videos in a project -- my bookmarks, my collection of TV clips, or my social media scrapbook.

I've noticed myself writing similar logic in each project -- finding the downloaded files, converting them to MP4, getting the channel information, and so on.
When you write the same thing multiple times, it's a sign you should extract it into a shared tool -- so that's what I've done.

[yt-dlp_alexwlchan](https://github.com/alexwlchan/yt-dlp_alexwlchan) is a script that calls yt-dlp with my preferred options, in particular:

* Download the highest-quality video, thumbnail, and subtitles
* Save the video as MP4 and the thumbnail as a JPEG
* Get some information about the video (like title and description) and the channel (like the name and avatar)

All this is presented in a CLI command which prints a JSON object that other projects can parse.
Here's an example:

```console?prompt=$
$ yt-dlp_alexwlchan.py "https://www.youtube.com/watch?v=TUQaGhPdlxs"
{
  "id": "TUQaGhPdlxs",
  "url": "https://www.youtube.com/watch?v=TUQaGhPdlxs",
  "title": "\"new york city, manhattan, people\" - Free Public Domain Video",
  "description": "All videos uploaded to this channel are in the Public Domain: Free for use by anyone for any purpose without restriction. #PublicDomain",
  "date_uploaded": "2022-03-25T01:10:38Z",
  "video_path": "\uff02new york city, manhattan, people\uff02 - Free Public Domain Video [TUQaGhPdlxs].mp4",
  "thumbnail_path": "\uff02new york city, manhattan, people\uff02 - Free Public Domain Video [TUQaGhPdlxs].jpg",
  "subtitle_path": null,
  "channel": {
    "id": "UCDeqps8f3hoHm6DHJoseDlg",
    "name": "Public Domain Archive",
    "url": "https://www.youtube.com/channel/UCDeqps8f3hoHm6DHJoseDlg",
    "avatar_url": "https://yt3.googleusercontent.com/ytc/AIdro_kbeCfc5KrnLmdASZQ9u649IxrxEUXsUaxdSUR_jA_4SZQ=s0"
  },
  "site": "youtube"
}
```

Rather than using the yt-dlp CLI, I'm using the Python interface.
I can [import the `YouTubeDL` class](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#embedding-yt-dlp) and pass it some options, then pull out the important fields from the response.
The library is very flexible, and [the options are well-documented](https://github.com/yt-dlp/yt-dlp/blob/5513036104ed9710f624c537fb3644b07a0680db/yt_dlp/YoutubeDL.py#L198-L577).

This is similar to my [`create_thumbnail` tool](/2024/create-thumbnail/).
I only have to define [my preferred behaviour](/2025/create-thumbnail-is-exif-aware/) once, then other code can call it as an external script.

I have ideas for changes I might make in the future, like tidying up filenames or supporting more sites, but I'm pretty happy with this first pass.
All the code is in [my yt-dlp_alexwlchan GitHub repo][repo].

This script is based on my preferences, so you probably don't want to use it directly -- but if you use yt-dlp a lot, it could be a helpful starting point for writing your own script.

Even if you don't use yt-dlp, the idea still applies: when you find yourself copy-pasting configuration and options, turn it into a standalone tool.
It keeps your projects cleaner and more consistent, and your future self will thnak you for it.

[yt-dlp]: https://github.com/yt-dlp/yt-dlp
[repo]: https://github.com/alexwlchan/yt-dlp_alexwlchan
