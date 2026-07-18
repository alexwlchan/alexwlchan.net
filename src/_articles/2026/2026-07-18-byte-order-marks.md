---
layout: article
date: 2026-07-18 08:11:26 +01:00
title: Fixing a bug with byte order marks
summary: I didn't know to check for UTF-8 byte order marks, so I made a mistake when converting text files. I was meant to use `encoding="utf-8-sig"`.
topic: Text and Unicode
---
Recently I've been tidying up the subtitles in my local media library.
There are two popular file formats for subtitles: SRT ([SubRip Subtitle][wiki-srt]) and WebVTT ([Web Video Text Tracks][wiki-vtt]).

I've been standardising on WebVTT because it works with the HTML5 `<video>` element, and I play all my videos through the `<video>` element embedded in static websites.
However, lots of subtitles are only available as SRT, so I wrote [a Python function][me-chives-srt-to-vtt] to convert SRT files to WebVTT.
The formats looked simple and the conversion seemed straightforward.
Famous last words!

When I spot checked the converted subtitles, I noticed a bug in my handling of [byte order marks (BOM)][wiki-bom], and it took several steps to fix.

## Failing to look for the UTF-8 BOM

A byte order mark is a special use of the [zero width no-break space character][unicode-zwnbsp] `U+FEFF` at the beginning of a text file, which tella a program reading the file about how the text is encoded.
It depends on the exact sequence of bytes used to encode the character.
Here are a few examples:

*   `EF BB BF` -- the file is UTF-8 text.
    UTF-8 always has the same byte order, so it's just telling us about the encoding.
*   `FE FF` -- the file is UTF-16 text, with [big-endian][wiki-big-endian] byte order (UTF-16BE).
*   `FF FE` -- the file is UTF-16 text, with [little-endian][wiki-little-endian] byte order (UTF-16LE).
*   `00 00 FE FF` -- the file is UTF-32 text, with big-endian byte order.

All of my SRT input files were UTF-8 encoded, and some of them had the UTF-8 byte order mark, and I wasn't handling it correctly.
For example, suppose I had this input SRT file:

<pre><code><span class="c">&lt;U+FEFF&gt;</span>1
00:00:01,001 --> 00:00:10,010
You have grown, Keyne.

2
00:02:00,002 --> 00:20:00,020
Soon you’ll be needing another name.</code></pre>

When I convert to WebVTT, I want to add the `WEBVTT` header, remove the sequence numbers, and change the timestamp format.

To remove sequence numbers, I was checking if a line was all digits.
Because the BOM is on the same line as the first sequence number, the line isn't all digits, so I didn't remove it.
Instead, I copied the entire line into the middle of the WebVTT file, BOM and all:

<pre><code>WEBVTT

<span class="c">&lt;U+FEFF&gt;</span>1
00:00:01.001 --> 00:00:10.010
You have grown, Keyne.

00:02:00.002 --> 00:20:00.020
Soon you’ll be needing another name.</code></pre>

The correct conversion would remove both the byte order mark and that first sequence number:

<pre><code>WEBVTT

00:00:01.001 --> 00:00:10.010
You have grown, Keyne.

00:02:00.002 --> 00:20:00.020
Soon you’ll be needing another name.</code></pre>

In my local media library, I can assume everything is UTF-8.
I can safely remove the byte order marks, and my web browser will still decode my subtitles correctly.

## Fixing the converter with `encoding="utf-8-sig"`

In my first fix, I tried to handle the BOM manually.
I wrote code that looked for `U+FEFF` and stripped it from the file, trying to detect it and re-insert it into the converted WebVTT file.
(This was before I realised I could just remove it entirely.)
It was a bit messy, because I was mixing low-level text encoding code with my high-level subtitle conversion steps.

As I was researching this article, I realised there's a more elegant solution: if I open the SRT file with [`encoding="utf-8-sig"`][pydoc-utf-8-sig], Python will automatically detect and skip the optional UTF-8 encoded BOM at the start of the file.
The rest of my code doesn't know or care that it's there.

I [fixed the bug in my function][me-chives-v47], which means future conversions will work correctly -- but what about the broken files I've already generated?

## Detecting the UTF-8 BOM with ripgrep

Initially I tried searching for `U+FEFF` with TextMate, but it crashed consistently with that search, so I turned to command-line tools.

I use [ripgrep][gh-ripgrep] for searching text.
By default it does ["BOM sniffing"][gh-ripgrep-bom-sniffing] on files -- when it reads a file, it looks at the first few bytes, transcodes the file from its actual encoding to UTF-8, then executes the search on the transcoded version.
This is exactly how the BOM is meant to be used, but it's less helpful if the BOM itself is what you're searching for!

Instead, we can disable ripgrep's Unicode support and search raw bytes by using `(?-u:…)` in the regular expression.
(This flag comes [from Rust's regex crate][rust-regex-disable-unicode].)
The following command looks for lines that start with the UTF-8 BOM:

```console
$ rg '^(?-u:\xEF\xBB\xBF)'
```

If you were only looking for the BOM at the start of the file, you'd also want the `--multiline` flag.
That changes the caret `^` to anchor to the start of the file, not the start of any line.
But since I'm looking for BOMs which are in the middle of the file, omitting `--multiline` is correct.

This search threw up dozens of files with a broken BOM.
Initially I opened the broken files in TextMate and edited them manually:

```console
$ rg --files-with-matches --null '^(?-u:\xEF\xBB\xBF)' | xargs -0 mate
```

But I quickly realised this was too slow, so I wrote a Python script to clean up all the files at once:

```python {"names":{"1":"glob","2":"filepath","8":"f","9":"content","18":"f"}}
#!/usr/bin/env python3

import glob

for filepath in glob.glob("**/*.vtt", recursive=True):
    with open(filepath, "rb") as f:
        content = f.read()
        
    if b"\xef\xbb\xbf" in content:
        content = content.replace(b"\xef\xbb\xbf", b"")
        with open(filepath, "wb") as f:
            f.write(content)
        print(filepath)
```

Once I'd run this script, I used my ripgrep command to check it was correct -- and indeed, all the erronous BOMs had been stripped from my media collection.
I also track my subtitle files in a Git repo, so I could confirm the script didn't introduce other changes.

Before this bug, I'd only vaguely heard of byte order marks, and I'd never had to tackle them in anger.
This sort of lesson is exactly why I love managing my local media archives as [hand-built static websites][me-static-websites] -- the lo-fi approach gives me lots of opportunities to explore low-level ideas and learn how things actually work on my computer.

[gh-ripgrep]: https://github.com/burntsushi/ripgrep
[gh-ripgrep-bom-sniffing]: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md#file-encoding
[me-chives-srt-to-vtt]: https://alexwlchan.net/projects/chives/files/src/chives/media.py#:~:text=def%20convert_srt_to_vtt
[me-chives-v47]: https://alexwlchan.net/projects/chives/commits/cefb7120edd3fc233d12660bd9cd906e04ebd419/
[me-static-websites]: /2024/static-websites/
[pydoc-utf-8-sig]: https://docs.python.org/3/library/codecs.html#module-encodings.utf_8_sig
[rust-regex-disable-unicode]: https://docs.rs/regex/latest/regex/#opt-out-of-unicode-support
[unicode-zwnbsp]: https://unicode-explorer.com/c/FEFF
[wiki-bom]: https://en.wikipedia.org/wiki/Byte_order_mark
[wiki-big-endian]: https://en.wikipedia.org/wiki/Big-endian
[wiki-little-endian]: https://en.wikipedia.org/wiki/Little-endian
[wiki-vtt]: https://en.wikipedia.org/wiki/WebVTT
[wiki-srt]: https://en.wikipedia.org/wiki/SubRip
