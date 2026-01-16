---
layout: til
date: 2024-06-26 09:29:09 +01:00
title: How to get the selected item in Finder using AppleScript
tags:
  - applescript
  - macos
---
I was doing some stuff today where I was selecting items in Finder, and then passing them to a command-line app in Terminal.
I could drag-and-drop the files into Terminal to get their path, but for hundreds of items that gets tedious -- I wanted a way for Terminal to automatically get the current item in Finder.

I found an AppleScript that does this:

```applescript
tell application "Finder" to get POSIX path of first item of (selection as alias list)
```

Open questions if I decide to revisit this snippet:

*   How does this work?
    I'm not sure what `as alias list` is doing here.

*   How do I get the paths of multiple selected items?
    AppleScript has access to them in the `selection` variable, but passing a list of paths between programs is somewhat tricky -- see e.g. problems with parsing the output of `ls(1)`.
    Maybe rewrite this code in JXA and return a JSON array?
