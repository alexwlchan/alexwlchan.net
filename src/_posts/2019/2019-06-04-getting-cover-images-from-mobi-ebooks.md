---
layout: post
date: 2019-06-04 19:43:14 +0000
title: A script for getting cover images from mobi ebooks
summary:
category: Programming and code
link: https://github.com/alexwlchan/get-mobi-cover-image
---

As part of a recent project, I've been writing code to get thumbnails for a bunch of different file formats.
Most of them have been pretty easy -- images and PDFs are both common and simple.

One format I'd been struggling with for a while is the .mobi ebook format -- I couldn't find any good libraries for parsing it, and Google found several people who'd asked about doing it, [but without any answers](https://xkcd.com/979/).
There's enough information that I might be able to write my own parser, but it's more effort than I want to spend.

This morning, I finally found the bits I needed.
Several other people have written code that gets the cover image out of the file, and I wrapped that in a script that saves that image as a standalone file:

```console
$ python get_mobi_cover.py pg59664-images.mobi
cover-41bFd.jpeg
```

If you're interested, all the code is [on GitHub](https://github.com/alexwlchan/get-mobi-cover-image).
