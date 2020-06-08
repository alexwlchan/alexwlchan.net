---
layout: post
date: 2019-04-11 07:00:43 +0000
title: Getting a transcript of a talk from YouTube
summary: Using the auto-generated captions from a YouTube video as a starting point for a complete transcript.
tags:
category: Programming and code
tags: youtube
---

When I give conference talks, my talks are often videoed and shared on YouTube.
Along with the video, I like to post the slides afterwards, and include an inline transcript.
A written transcript is easier to skim, to search, and for Google to index.
Plus, it makes the talk more accessible for people with hearing difficulties.
Here's an example from PyCon UK last year: [Assume Worst Intent](/2018/09/assume-worst-intent/).

I share a transcript rather than pre-prepared notes because I often ad lib the content of my talks.
I might add or remove something at the last minute, make subtle changes based on the mood of the audience, or make a reference to a previous session that wasn't in my original notes.
A transcript is a more accurate reflection of what I said on the day.

Some conferences have live captioning (a human speech-to-text reporter transcribing everything I say, as I write it), which does the hard work for me!
That's great, and those transcripts are very high quality -- but not every event does this.

If I have to do it myself, writing a new transcript is a lot of work, and slows down posting the slides.
So what I do instead is lean on YouTube to get a first draft of a transcript, and then I tidy it up by hand.

YouTube uses speech-to-text technology to automatically generate captions for any video that doesn't already have them (in a handful of languages, at least).
It's not fantastically accurate, but it's close enough to be a useful starting point.
I can edit and polish the automatically generated transcript much faster than I could create my own from scratch.

## How I do it

I start by using [youtube-dl][yt_dl] to download the automatically generated captions to a file.

```console
$ youtube-dl --write-auto-sub --skip-download "https://www.youtube.com/watch?v=XyGVRlRyT-E"
```

This saves a `.vtt` subtitle file in the current directory.

The `.vtt` file is a format meant for video players -- it describes what words should appear on the screen, when.
Here's a little snippet:

```
00:00:00.030 --> 00:00:03.500 align:start position:0%

again<c.colorE5E5E5><00:00:01.669><c> since</c><00:00:02.669><c> you've</c><00:00:02.790><c> already</c><00:00:02.970><c> heard</c></c><c.colorCCCCCC><00:00:03.300><c> from</c><00:00:03.449><c> me</c></c>

00:00:03.500 --> 00:00:03.510 align:start position:0%
again<c.colorE5E5E5> since you've already heard</c><c.colorCCCCCC> from me
 </c>
```

It's a mixture of timestamps, colour information, and the text to display.
To turn this into something more usable, I have a Python script that goes through and extracts just the text.
It's a mess of regular expressions, not a proper VTT parser, but it does the trick.
You can download the script [from GitHub][script].

This gives me just the content of the captions:

```
again since you've already heard from me
before I'll skip the introduction and
gets right into the talk we're talking
```

I save that to a file, then I go through that text to add punctuation and tidy up mistakes.
If it's not clear from the transcript what I was saying, I'll go back and rewatch the video, but I only need a few seconds at a time.

[yt_dl]: http://ytdl-org.github.io/youtube-dl/
[script]: https://github.com/alexwlchan/junkdrawer/blob/d8ee4dee1b89181d114500b6e2d69a48e2a0e9c1/services/youtube/vtt2txt.py


## Observations

The YouTube auto-captioning software is good, but far from perfect.
Here are a couple of changes I'm especially used to making:

*   It really struggles on proper names.
    If I have a human captioner on the day, I’ll tell them the names in advance so they know what to expect, but there's no way to do the same for YouTube.

*   It prefers US spellings for words, like "color" or "favorite" or "realize".
    Since I use British spellings on this blog, I change all of those.

*   It can struggle with homophones.
    A recent example: "you all write documentation" became "you all right documentation", which sounds the same but makes less sense.

*   It's very unforgiving with my verbal ticks.
    I see just how often I say phrases like "I think", "so" and "because".
    This is useful feedback for me, but I edit them out of the finished transcript, because they're just verbal noise.

Overall it's a lot faster than writing a transcript from scratch, and a lot kinder to my hands.
I spend most of my time reading, not typing, and it takes much less time from start to finish.

If you need some captions and you don't have the time or money for a complete human transcript, the YouTube auto-generated captions are a good place to start.
