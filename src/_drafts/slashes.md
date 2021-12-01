---
layout: post
title: A tale of two path separators
summary: macOS allows both the slash and colon as path separators, and this caused me no small amount of confusion.
tags: macOS
---

I was reminded yesterday that macOS will happily let you create files that appear to have slashes in their name, as the macOS Finder reports:

<img src="/images/2021/slashed_files.png" style="width: 644px;">

I made the folder with the "New Folder" button in Finder, and the text file by saving a file in TextEdit.
Even though I understand how this works, it breaks my brain a bit every time.

If you didn't know how this works, you could get a clue by running `ls`:

```console
$ ls
a:b:c/     x:y:z.txt
```

We see that these files actually have colons in their name, but Finder is presenting them as slashes.

I don't understand all the nuances, but this seems like a side-effect of the fact that macOS has not one but *two* path separators: the slash (`/`) and the colon (`:`).
The two separators are used in different contexts, and the system will translate between them as it goes (which you see in the Finder above).

These two separators in turn reflect the two parent systems of modern macOS: [classic Mac OS] and the [Unix-like NeXTSTEP].
When they were first joined together, Apple's engineers had to build a file system that was compatible with both the Mac's file system (at the time, [the Mac OS Extended File System, aka HFS+][hfs+]), and with NeXTSTEP's file system (the Unix file system, aka UFS).
These systems had different path separators: HFS+ used the colon, while UFS used the slash.

There's a [Usenix 2000 paper written by several Apple engineers][usenix2000] which describes the problems of combining classic Mac OS and Unix in more detail.
It actually describes exactly what we're seeing with the Finder and `ls`:

> [The translation layer] can create a user-visible schizophrenia in the rare cases of file names containing colon characters, which appear to Carbon applications as slash characters, but to BSD programs and Cocoa applications as colons.

Over 20 years later, you can still see both path separators poking through in modern macOS:

```console
$ which osascript
/usr/bin/osascript

$ osascript -e 'tell application "Finder" to get (path to me)'
alias Phoenix SSD:usr:bin:osascript
```

Notice that AppleScript (a language that goes back to System 7, which only had to care about HFS+) is still using the colon as a path separator.

Apple have replaced HFS+ with [the Apple File System, aka APFS][APFS], but these dual path separators remain.
I can't find any documentation to confirm it, but I assume that's for backward compatibility reasons -- unifying the path separators would break an enormous amount of software, and for a change that isn't going to be noticed by most users.

The "slashes in filenames" breaks my brain because I started programming after Unix-like filesystems had become totally dominant.
In my mind, slash is *the* directory separator, and Windows is weird for using the backwards slash (`\`).
In reality, file systems have used [a variety of directory separators][separator], and it's only the Unix hegemony that makes this seem weird.
On another system, forward slashes in a filename would be totally normal.

[classic Mac OS]: https://en.wikipedia.org/wiki/Classic_Mac_OS
[Unix-like NeXTSTEP]: https://en.wikipedia.org/wiki/NeXTSTEP
[hfs+]: https://en.wikipedia.org/wiki/HFS_Plus
[usenix2000]: http://www.wsanchez.net/papers/USENIX_2000/
[APFS]: https://en.wikipedia.org/wiki/Apple_File_System
[separator]: https://en.wikipedia.org/wiki/Path_(computing)#Representations_of_paths_by_operating_system_and_shell
