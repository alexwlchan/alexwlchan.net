---
layout: post
date: 2025-11-08 23:13:56 +0000
title: Detecting AV1-encoded videos with Python
summary: I wrote a Python test to find videos that are encoded with AV1, so I can convert them to a codec my iPhone can play.
tags:
  - video
  - python
---
In [my previous post][av1-on-iphone], I wrote about how I've saved some AV1-encoded videos that I can't play on my iPhone.
Eventually, I'll upgrade to a new iPhone which supports AV1, but in the meantime, I want to convert all of those videos to an older codec.
The problem is finding all the affected videos -- I don't want to wait until I want to watch a video before discovering it won't play.

I already use [pytest] to run some checks on my media library: are all the files in the right place, is the metadata in the correct format, do I have any [misspelt tags][fuzzy-tags], and so on.
I wanted to write a new test that would check for AV1-encoded videos, so I could find and convert them in bulk.

In this post, I'll show you two ways to check if a video is encoded using AV1, and a test I wrote to find any such videos inside a given folder.

[av1-on-iphone]: /2025/av1-on-my-iphone/
[pytest]: https://docs.pytest.org/en/stable/
[fuzzy-tags]: /2020/using-fuzzy-string-matching-to-find-duplicate-tags/

{% table_of_contents %}

## Getting the video codec with ffprobe

In my last post, I wrote an [ffprobe] command that prints some information about a video, including the codec.
(ffprobe is a companion tool to the popular video converter [FFmpeg].)

{% code lang="console" %}
$ ffprobe -v error -select_streams v:0 \
    -show_entries stream=codec_name,profile,level,bits_per_raw_sample \
    -of default=noprint_wrappers=1 "input.mp4"
codec_name=av1
profile=Main
level=8
bits_per_raw_sample=N/A
{% endcode %}

I can tweak this command to print just the codec name:

{% code lang="console" %}
$ ffprobe -v error -select_streams v:0 \
    -show_entries stream=codec_name \
    -of csv=print_section=0 "input.mp4"
av1
{% endcode %}

To run this command from Python, I call the [`check_output` function][check_output] from the [`subprocess` module][subprocess].
This checks the command completes successfully, then returns the output as a string.
I can check if the output is the string `av1`:

{% code lang="python" names="0:subprocess 1:is_av1_video 2:path 5:output" %}
import subprocess


def is_av1_video(path: str) -> bool:
    """
    Returns True if a video is encoded with AV1, False otherwise.
    """
    output = subprocess.check_output([
        "ffprobe",
        #
        # Set the logging level
        "-loglevel", "error",
        #
        # Select the first video stream
        "-select_streams", "v:0",
        #
        # Print the codec_name (e.g. av1)
        "-show_entries", "stream=codec_name",
        #
        # Print just the value
        "-output_format", "csv=print_section=0",
        #
        # Name of the video to check
        path
    ], text=True)

    return output.strip() == "av1"
{% endcode %}

Most of this function is defining the ffprobe command, which takes quite a few flags.
Whenever I embed a shell command in another program, I always replace any flags/arguments with the long versions, and explain their purpose in a comment -- for example, I've replaced `-of` with `-output_format`.
Short flags are convenient when I'm typing something by hand, but long flags are more readable when I return to this code later.

This function works, but the ffprobe command is quite long, and it requires spawning a new process for each video I want to check.
Is there a faster way?

[ffprobe]: https://ffmpeg.org/ffprobe.html
[FFmpeg]: https://www.ffmpeg.org/
[subprocess]: https://docs.python.org/3/library/subprocess.html
[check_output]: https://docs.python.org/3/library/subprocess.html#subprocess.check_output

## Getting the video codec with MediaInfo

While working at the Flickr Foundation, I discovered [MediaInfo], another tool for analysing video files.
It's used in [Data Lifeboat] to get the [dimensions] and [duration] of videos.

You can run MediaInfo as a command-line program to get the video codec:

```console
$ mediainfo --Inform="Video;%Format%" "input.mp4"
AV1
```

This is a simpler command than ffprobe, but I'd still be spawning a new process if I called this from subprocess.

Fortunately, MediaInfo is also available as a library, and it has [a Python wrapper][pymediainfo].
You can install the wrapper with `pip install pymediainfo`, then we can use the functionality of MediaInfo inside our Python process:

{% code lang="pycon" names="0:pymediainfo 1:MediaInfo 2:media_info" %}
>>> from pymediainfo import MediaInfo
>>> media_info = MediaInfo.parse("input.mp4")
>>> media_info.video_tracks[0].codec_id
'av01'
{% endcode %}

This code could throw an `IndexError` if there's no video track -- if it's a `.mp4` file which only has audio data -- but that's pretty unusual, and not something I've found in any of my videos.

I can write a new wrapper function:

{% code lang="python" names="0:pymediainfo 1:MediaInfo 2:is_av1_video 3:path 6:media_info" %}
from pymediainfo import MediaInfo


def is_av1_video(path: str) -> bool:
    """
    Returns True if a video is encoded with AV1, False otherwise.
    """
    media_info = MediaInfo.parse(path)

    return media_info.video_tracks[0].codec_id == "av01"
{% endcode %}

This is shorter than the ffprobe code, and faster too -- testing locally, this is about 3.5&times; faster than spawning an ffprobe process per file.

[Data Lifeboat]: https://www.flickr.org/programs/content-mobility/data-lifeboat/
[MediaInfo]: https://mediaarea.net/en/MediaInfo
[dimensions]: /til/2025/get-video-dimensions-with-mediainfo/
[duration]: /til/2025/mediainfo-duration/
[pymediainfo]: https://github.com/sbraz/pymediainfo

## Writing a test to find videos with the AV1 codec

Now we have a function that tells us if a given video uses AV1, we want a test that checks if there are any matching files.
This is what I wrote:

{% code lang="python" names="0:glob 1:test_no_videos_are_av1 2:av1_videos 3:p" %}
import glob


def test_no_videos_are_av1():
    """
    No videos are encoded in AV1 (which doesn't play on my iPhone).

    This test can be removed when I upgrade all my devices to ones with
    hardware AV1 decoding support.

    See https://alexwlchan.net/2025/av1-on-my-iphone/
    """
    av1_videos = {
        p
        for p in glob.glob("**/*.mp4", recursive=True)
        if is_av1_video(p)
    }

    assert av1_videos == set()
{% endcode %}

It uses the [glob module][glob] to find `.mp4` video files anywhere in the current folder, and then filters for files which use the AV1 codec.
The `recursive=True` argument is important, because it tells glob to search below the current directory.

I’m only looking for `.mp4` files because that's the only format I use for videos, but you might want to search for `.mkv` or `.webm` too.
If I was doing that, I might drop glob and use [my snippet for walking a file tree](/2023/snake-walker/) instead.

The test builds a set of all the AV1 videos, then checks that it's empty.
This means that if the test fails, I can see all the affected videos at once.
If the test failed on the first AV1 video, I'd only know about one video at a time, which would slow me down.

[glob]: https://docs.python.org/3/library/glob.html#module-glob

## Putting it all together

You can use ffprobe or MediaInfo -- I prefer MediaInfo because it's faster and I already have it installed, but both approaches are fine.

Here's my final test, which uses MediaInfo to check if a video uses AV1, and scans a folder using glob.
I've saved it as `test_no_av1_videos.py`:

{% code lang="python" names="0:glob 1:pymediainfo 2:MediaInfo 3:is_av1_video 4:path 7:media_info 14:test_no_videos_are_av1 15:av1_videos" %}
import glob

from pymediainfo import MediaInfo


def is_av1_video(path: str) -> bool:
    """
    Returns True if a video is encoded with AV1, False otherwise.
    """
    media_info = MediaInfo.parse(path)

    return media_info.video_tracks[0].codec_id == "av01"


def test_no_videos_are_av1():
    """
    No videos are encoded in AV1 (which doesn't play on my iPhone).

    This test can be removed when I upgrade all my devices to ones with
    hardware AV1 decoding support.

    See https://alexwlchan.net/2025/av1-on-my-iphone/
    """
    av1_videos = {
        p
        for p in glob.glob("**/*.mp4", recursive=True)
        if is_av1_video(p)
    }

    assert av1_videos == set()
{% endcode %}

In one folder with 350 videos, this takes about 8 seconds to run.
I could make that faster by reading the video files in parallel, or caching the results, but it's fast enough for now.

When I buy a new device with hardware AV1 decoding, I'll delete this test.
Until then, it's a quick and easy way to find and re-encode any videos that won't play on my iPhone.
