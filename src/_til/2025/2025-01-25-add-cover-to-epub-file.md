---
layout: til
title: Getting and setting the cover image from an EPUB file
date: 2025-01-25 23:23:52 +00:00
tags:
  - epub
---
I've only done this with a small number of EPUB files, but it seems to work so far.

## How to get the cover from an EPUB file

1.  Find the [`content.opf` file](/til/2025/find-content-opf-in-epub).
2.  Look for an `<item properties="cover-image" …>` element in the `<manifest>`, which will point to the path to the cover image, for example:
  
    ```xml
    <item
      id="cover-image"
      properties="cover-image"
      href="media/cover.png"
      media-type="image/png"/>
    ```

## How to set the cover in an EPUB file

1.  Add the cover image to the EPUB package.
2.  Find the [`content.opf` file](/til/2025/find-content-opf-in-epub).
3.  Add an `<item properties="cover-image" …>` element in the `<manifest>` which points to the cover image you've added:
  
    ```xml
    <item
      id="cover-image"
      properties="cover-image"
      href="media/cover.png"
      media-type="image/png"/>
    ```

4.  Add a `<meta name="cover" …>` element in the `<metadata>` which points to the `<manifest>` element you just added:
  
    ```xml
    <meta name="cover" content="cover-image"/>
    ```

## Don't use pandoc

While researching this question, I asked Claude hwo to solve this.
It suggested using [pandoc]

```
pandoc input.epub -o output.epub --epub-cover-image=cover.png
```

I was already dubious because pandoc is a big dependency to add to an app, but even more so when I realised that this mangles the formatting.

[pandoc]: https://pandoc.org/
