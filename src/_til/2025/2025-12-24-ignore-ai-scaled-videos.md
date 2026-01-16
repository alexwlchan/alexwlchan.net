---
layout: til
title: Ignore AI upscaled YouTube videos with yt-dlp
summary: Filter for formats that don't include `-sr` ("super resolution") in their format ID.
date: 2025-12-24 15:16:54 +00:00
tags:
  - yt-dlp
---
<!-- Card image based on https://www.pexels.com/photo/close-up-of-multi-colored-tulips-250716/ -->

At the end of October, YouTube introduced a "feature" to do [AI upscaling][yt-announcement] of low-resolution videos.

When you're downloading a video with yt-dlp, you can spot AI upscaled videos by looking for the `-sr` suffix in the format ID, or `AI-upscaled` in the format note.
Here's an example from a video uploaded in 2009:

```console
$ yt-dlp --list-formats 'https://www.youtube.com/watch?v=0N1_0SUGlDQ'
[info] Available formats for 0N1_0SUGlDQ:
ID     EXT   RESOLUTION FPS CH │   FILESIZE   TBR PROTO │ VCODEC          VBR ACODEC      ABR ASR MORE INFO
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
sb2    mhtml 48x27        1    │                  mhtml │ images                                  storyboard
…
397    mp4   640x480     30    │    6.06MiB  306k https │ av01.0.04M.08  306k video only          480p, mp4_dash
247-sr webm  960x720     30    │   11.47MiB  578k https │ vp9            578k video only          720p, AI-upscaled, webm_dash
398-sr mp4   960x720     30    │    9.13MiB  461k https │ av01.0.05M.08  461k video only          720p, AI-upscaled, mp4_dash
248-sr webm  1440x1080   30    │   21.22MiB 1071k https │ vp9           1071k video only          1080p, AI-upscaled, webm_dash
399-sr mp4   1440x1080   30    │   18.46MiB  931k https │ av01.0.08M.08  931k video only          1080p, AI-upscaled, mp4_dash
```

Because yt-dlp helpfully [includes `-sr` in the format ID][yt-dlp-sr] of AI upscaled videos, you can exclude them by [adding a format filter][yt-dlp-filtering].

*   If you're using the CLI, add the `--format` flag.
    For example:
    
    {% code lang="console" %}
    $ yt-dlp "https://www.youtube.com/watch?v=0N1_0SUGlDQ" \
        --format 'bestvideo*[format_id!*=-sr]+bestaudio/best[format_id!*=-sr]'
    {% endcode %}

*   If you're embedding it in Python, add `format` to the options passed to `YouTubeDL`.
    For example:
    
    {% code lang="python" names="0:yt_dlp 1:YoutubeDL 2:ydl_opts 5:ydl" %}
    from yt_dlp import YoutubeDL

    ydl_opts = {"format": "bestvideo*[format_id!*=-sr]+bestaudio/best[format_id!*=-sr]"}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=0N1_0SUGlDQ"])
    {% endcode %}

I've added the latter to my [personal wrapper around yt-dlp][yt-dlp-wrapper].

[yt-announcement]: https://blog.youtube/news-and-events/new-features-to-help-creators/
[yt-dlp-filtering]: https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#filtering-formats
[yt-dlp-wrapper]: /2025/yt-dlp-wrapper/
[yt-dlp-sr]: https://github.com/yt-dlp/yt-dlp/issues/14923#issuecomment-3539437820
