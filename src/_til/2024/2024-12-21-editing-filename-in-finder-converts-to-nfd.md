---
layout: til
title: Editing a filename in Finder will convert it to NFD
date: 2024-12-21 21:10:06 +00:00
tags:
  - macos
  - unicode shenanigans
summary: |
  Even if the filename looks the same, it may be invisibly converted to a different sequence of bytes.
---
I noticed this while working on a file called `Besźel.jpg`.

The file had been written as `Bes\xc5\xbael.jpg`, but editing the filename in Finder would convert it to NFD.

```pycon
>>> import unicodedata
>>> unicodedata.normalize('NFC', 'Besźel').encode('utf8')
b'Bes\xc5\xbael'
>>> unicodedata.normalize('NFD', 'Besźel').encode('utf8')
b'Besz\xcc\x81el'
```

Indeed, even interacting with the filename caused this conversion – I pressed `enter` to make the filename selectable, pressed ⌘+C to copy everything but the file extension, then pressed `enter` to finish.
This triggered it!
I was confused because the filename looked the same -- I hadn't made any visible changes, but the sequence of bytes had changed.

Once you know this is a thing, the fact that Finder converts to NFD is easy to find online -- but it took me a minute or so to work out what was happening with this file.

I removed the special character from the filename rather than try to get it working; exactitude wasn't important for my particular problem.
