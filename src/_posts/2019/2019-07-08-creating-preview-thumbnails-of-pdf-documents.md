---
category: Python
date: 2019-07-08 21:44:29 +0000
layout: post
summary: null
title: Creating preview thumbnails of PDF documents
---

Whenever I get an important document, I scan it or save it as a PDF.
It's a format that seems pretty likely to remain readable in the medium-term[^1], even if I start using a different computer or operating system.
I've created a small app for managing my scans (*docstore*, code is [on GitHub](https://github.com/alexwlchan/docstore)), and as part of the app I create small thumbnails of each PDF.
The thumbnails make it easier to skim a list of documents, especially when companies use a consistent letterhead.

Here's an example of some thumbnails, for the documents for a recent trip:

![A list of three documents, with a thumbnail on the left and a title on the right.](/images/2019/pdf_thumbnails.png)

If I'm searching the list, the turquoise of the Trainline email stands out against, say, the dark green stripe used by my bank.

When I was working out how to do this, I found a lot of Google results for PDF thumbnails in other applications -- the macOS Finder, Windows Explorer, Adobe Acrobat -- but not much on creating them if you're writing your own code.

After experimenting with a couple of different tools, I found one I like and which works consistently.
The tool I'm use is [pdftocairo](https://www.mankier.com/1/pdftocairo), a command-line tool that converts PDFs to images.

Here's the command I use:

```console
$ pdftocairo my_document.pdf -jpeg -singlefile -scale-to-x 400
```

These creates a new file `my_document.jpg` in the same directory, which is a 400-pixel wide preview of the first page.

I'm using the following options:

*   `-jpeg` creates a JPEG output file.
    I've experimented a bit and the format doesn't seem to make much difference for size/quality, so I picked JPEG somewhat arbitrarily.
*   `-singlefile` is an option that justs gets the first page.
*   `-scale-to-x 400` resizes the image to 400 pixels wide.

The quality varies at larger sizes (particularly with font rendering if you don't have the right fonts installed), but for creating small thumbnails the images look fine.
I've used a wrapper around this utility for several thousand documents now, and they've all worked a treat.

[^1]: If you want to keep documents for proper long-term preservation and archiving, you can use the [PDF/A standards](https://en.wikipedia.org/wiki/PDF/A). I don't use PDF/A -- most of my documents don't need to last more than a few years. Plus, I don't even know how to convert a regular PDF to PDF/A!
