---
layout: post
date: 2022-12-31 12:42:13 +00:00
title: A script to get Live Text from images
summary: Using Apple's built-in tools to get OCR text from an image, but without going through a GUI.
tags:
  - images
  - swift
---

One of my favourite new features on Apple's OSes in the last few years is Live Text, which is an [optical character recognition][ocr] tool that lets you select text in images.
This sort of tech has been around for decades, but having it built into the OS makes it much easier to use.
The text recognition isn't perfect, but it works reliably and it's good enough most of the time.

This is the promise of "it just works": I [open an image in Preview][preview], hover my cursor over the text, I get a text selection cursor, then I right-click to get a menu of options:

<figure style="width: 491px;">
  {%
    picture
    filename="live_text.jpg"
    alt="A picture of a railway sign with the text highlighted, and a popover menu offering several options: ‘Look up “Passengers must not pass this point or cross the line”’, ‘Translate “Passengers must not pass this point or cross the line”’, Search with Google, Copy, or Share."
    width="491"
    class="screenshot"
  %}
  <figcaption>
    Staying off the tracks at <a href="/2022/bure-valley/">the Bure Valley Railway</a>.
  </figcaption>
</figure>

This framework is also available for apps to use, and I found some instructions in an Apple article [Recognizing Text in Images][docs].
I've been able to wrap this in a Swift script that lets me get live text on the command line.
You can download the script [from GitHub][script].

You pass the path to your image as a single command-line argument.
Any text found in the image will be returned as a JSON list:

```console
$ get_live_text railway-sign.jpg
["Passengers must","not pass this point","or cross the line"]
```

If the image doesn't contain any text, it returns an empty list:

```console
$ get_live_text dancers.jpg
[]
```

I've got [a second script][second] which scans a directory for images, gets Live Text for each of them, and saves the output to a JSON file.

I can think of a bunch of things I might do with this, starting with full-text search of images.
(You can do search images by text if they're in your Photos Library, but I have a lot of images which aren't, including everything on my work laptop and my [screenshot collection][screenshots].)

Live Text may not be most accurate OCR tool, but for me it's the most convenient.
I've tried and failed to install command-line OCR in the past; getting this working took less than 15 minutes.

*[**Update, 7 February 2024:** if you're not comfortable running scripts, you might prefer using the [Shortcuts app] which is already installed on your Mac. I've made [a shortcut](/files/2022/Get text from images.shortcut) which does something similar to this script, but doesn't require as much programming knowledge.]*

[ocr]: https://en.wikipedia.org/wiki/Optical_character_recognition
[preview]: https://support.apple.com/en-gb/guide/preview/prvw625a5b2c/mac
[docs]: https://developer.apple.com/documentation/vision/recognizing_text_in_images#3601255
[script]: https://github.com/alexwlchan/get_live_text
[screenshots]: /2022/screenshots/
[second]: https://github.com/alexwlchan/pathscripts/blob/main/macos/get_all_live_text
[Shortcuts app]: https://support.apple.com/en-gb/guide/shortcuts-mac/apdf22b0444c/mac
