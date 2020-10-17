---
layout: post
title: How do I use my iPhone cameras?
summary:
tags: iphone photography
---

On [this week's episode of ATP](https://atp.fm/400), they were talking about how much they use the different cameras on their iPhones.
The iPhone 11 Pro has three cameras: wide (1&times;), ultrawide (0.5&times;) and telephoto (2&times;).
The iPhone 12 Mini only has two cameras: wide (1&times;) and ultrawide (0.5&times;).

Marco and Casey were both considering an upgrade from an 11 Pro to a 12 Mini – they like the idea of the smaller size, but were wondering how much they'd miss the telephoto lens.
Although I'm not upgrading myself, it made me wonder how much I use my different cameras.
**How many photos do I take with each camera?**

I vaguely remembered seeing the name of my iPhone when looking at pictures in Photos.app, so I went to have a look at that again.
It turns out that Photos.app knows not only which phone I was using, but which of the cameras I was using.
Useful!

<figure style="width: 392px;">
  <img src="/images/2020/exif_metadata_1x.png" srcset="/images/2020/exif_metadata_1x.png 1x, /images/2020/exif_metadata_2x.png 2x">
  <figcaption>
    The Info panel in Photos.app.
    You can find this by selecting a photo, then <strong>Window</strong> > <strong>Info</strong> or <strong>⌘I</strong>.
  </figcaption>
</figure>

This is part of the [EXIF metadata](https://en.wikipedia.org/wiki/Exif) on the photo, which includes plenty of other information about my camera -- including the aperture, exposure time, and whether or not the flash went off.
Two interesting fields are Lens Make (e.g. *"Apple"*) and Lens Model (e.g. *"iPhone 11 Pro back triple camera 4.25mm f/1.8"*).
If I could extract that data programatically, I could find out how many times I used each of my cameras.

There's a command-line program called [exiftool](https://exiftool.org) for extracting EXIF metadata, which should do nicely.
(I've never used it myself, but I know it's used in the digitisation workflow at Wellcome.)
I installed it with Homebrew (`brew install exiftool`), and then started playing around.

This is the command I ended up running:

```shell
exiftool \
    -r ~/Pictures/Photos\ Library.photoslibrary/Masters/2020/ \
    -p '${LensMake} / ${LensModel}' 2>/dev/null \
  | sort \
  | uniq -c \
  | sort --human-numeric-sort
```

The first part of the command gets exiftool to print the LensMake and LensModel for each photo in the 2020 folder of my photo library.
The `-r` flag tells it to recurse and find all the photos under the directory, rather than examining a single file.
This gives a line like:

```
Apple / iPhone 11 Pro back camera 4.25mm f/1.8
```

I'm discarding stderr (`2>/dev/null`), otherwise my terminal fills up with warnings about photos that don't have LensMake or LensModel metadata -- usually screenshots.

I pass the output to `sort` (so identical lines appear next to each other), and then I use `uniq -c` to get a tally of the different values.
The tally prints the count, so I sort it a second time to get the numbers in a nice order.

This command takes a couple of minutes to run -- despite being stuck indoors for most of the year, I've taken a lot of photos -- but eventually I get some output:

```
   1 Apple / iPhone 11 Pro back camera 1.54mm f/2.4
   5 Apple / iPhone 11 Pro back dual camera 6mm f/2
   7 Apple / iPhone 11 Pro back dual wide camera 4.25mm f/1.8
  14 Apple / iPhone 11 Pro front TrueDepth camera 2.71mm f/2.2
  26 Apple / iPhone 11 Pro back camera 4.25mm f/1.8
 156 Apple / iPhone 11 Pro back triple camera 6mm f/2
 305 Apple / iPhone 11 Pro back triple camera 1.54mm f/2.4
 549 Apple / iPhone 11 Pro front camera 2.71mm f/2.2
2121 Apple / iPhone 11 Pro back triple camera 4.25mm f/1.8
```

The f-numbers identify the different cameras, even if the exact EXIF values seem to vary -- I wonder if those change between major iOS releases?
I did some Googling, and found [a review that explains how the f-numbers correspond to lenses](https://www.wired.com/review/apple-iphone-11-pro/):

> The iPhone 11 Pro and Pro max have both of those lenses and a telephoto lens. The wide-angle lens has an f/1.8 aperture, the ultra-wide has a f/2.4 aperture, and the telephoto has an f/2.0 aperture.

Dropping those into the exiftool output above, here's how I've used my iPhone cameras this year:

```
 161 telephoto camera / 2× zoom
 306 ultrawide camera / 0.5× zoom
 563 front camera
2154 wide camera      / 1× zoom
```

So the telephoto and ultrawide cameras account for 5% and 10% of my camera use, respectively -- less than I'd have guessed.
I wouldn't be too fussed to lose the telephoto, and I'd rather lose that than the ultrawide -- and judging by Apple's new iPhones, my usage pattern is fairly typical.

I'm not planning to upgrade for another year or two, so this is just a curiosity -- but if you're trying to choose between iPhones this year, the EXIF metadata might help your decision.
