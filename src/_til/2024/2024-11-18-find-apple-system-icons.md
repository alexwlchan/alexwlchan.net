---
layout: til
title: How to find all of Apple's system icons
date: 2024-11-18 22:06:41 +00:00
tags:
  - macos
summary:
  You need to look for files named `*.icns` inside any subdirectory of `CoreTypes.bundle`.
---
Apple ships a bunch of high-quality icons of Mac hardware as part of macOS.
For a long time you could find all these icons in:

<pre style="text-wrap: wrap;"><code>/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/</code></pre>

but they gradually seem to have split up in newer versions of macOS.
I was looking for an icon for my 2024 Mac mini in macOS Sequoia 15.1, but I could only find older Mac minis in this folder:

{%
  picture
  filename="mac_mini_icons.png"
  width="600"
  class="screenshot"
  alt="A grid of seven Mac mini icons, which is conspicously missing the 2024 Mac mini."
%}

I found a [thread on Apple's discussion forums](https://discussions.apple.com/thread/254485283?answerId=258385613022&sortBy=rank#258385613022) where somebody was asking for a Mac Studio icon, and somebody suggested looking in a sub-bundle:

<pre style="text-wrap: wrap;"><code>/System/Library/CoreServices/CoreTypes.bundle/Contents/Library/CoreTypes-0003.bundle/Contents/Resources/</code></pre>

That folder doesn't exist on my system (I have `CoreTypes-0003.bundle`, but it doesn't have a `Resources` folder).
But this was a clue in the right direction!

I used the following shell commands:

```shell
mkdir -p icons

find /System/Library/CoreServices/CoreTypes.bundle \
  -type f -name "com.apple.*.icns" \
  -exec cp {} icons \;
```

This finds all ICNS files that are anywhere inside `CoreTypes.bundle`, and copies them to a new folder.
Then I could look for my Mac mini icon in that folder, and I don't have to worry about exactly where it lives.
