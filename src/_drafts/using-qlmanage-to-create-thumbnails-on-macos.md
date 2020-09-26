---
layout: post
title: Using qlmanage to create thumbnails on macOS
tags: macos
---

macOS has a feature called [Quick Look](https://en.wikipedia.org/wiki/Quick_Look), which lets you preview files.
If you look at a file in the Finder, you see a small preview in the icon.
If you select the file and press the space bar, you get a full-size preview:

<img src="/images/2020/quick_look_1x.png" srcset="/images/2020/quick_look_1x.png 1x, /images/2020/quick_look_2x.png 2x, /images/2020/quick_look_3x.png 3x" alt="macOS Finder window with a Quick Look preview in the foreground. The preview shows an ochre colour cat tilting his head and looking towards the camera.">

If the file has multiple pages (say, a slideshow or a long PDF), you can scroll through to see previews of each page.

Apple includes plugins for a number of common file formats, including PDFs, images, and HTML files.
Third-party developers can then write their own plugins, so that their documents can be previewed with Quick Look -- even if the document is a non-standard format.
All this means that Quick Look
is a pretty thorough tool for generating document previews on the Mac -- or at least, all the documents your Mac knows how to open.

Quick Look includes a command-line interface, which lets you trigger it from a terminal.
If you run `qlmanage -p`, it open a Quick Look preview in a new window.
For example:

```console
$ qlmanage -p ~/Downloads/IMG_5494.jpeg
```

Even more useful for me, you can use it to generate bitmap thumbnails of my files with the `-t` and the `-o` flags.
For example:

```console
$ mkdir -p thumbnails
$ qlmanage -t -o thumbnails ~/Downloads/IMG_5494.jpeg
```

This writes a PNG file to the `thumbnails` folder, with a tiny preview of my JPEG image.
If you want a larger (or smaller) thumbnail, you can pass the `-s <SIZE>` flag to specify a target width.
For example, if you wanted a preview which was 1000&nbsp;pixels wide:

```
$ qlmanage -t -o thumbnails -s 1000 ~/Downloads/IMG_5494.jpeg
```

(Note: the size is "up to", not "exactly".
My original image is 4032 pixels wide; if I request a thumbnail that's 5000 pixels wide, I only get a 4032px wide thumbnail.)

I've spent a bunch of time writing my own code for generating file thumbnails, including [using pdftocairo for PDFs](/2019/07/creating-preview-thumbnails-of-pdf-documents/) and [a Python script for MOBI ebooks](/2019/06/getting-cover-images-from-mobi-ebooks/).
It's a complex problem, and every so often I find a new file that needs some tweak to the code.
I'm looking forward to replacing it all with some new code that shells out to `qlmanage`, and letting the OS handle thumbnailing for me.
