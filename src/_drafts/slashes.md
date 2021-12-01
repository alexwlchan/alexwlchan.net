---
layout: post
title: A tale of two path separators
summary: macOS allows both the slash and colon as path separators, and this caused me no small amount of confusion.
tags: macOS
---

I was reminded yesterday that macOS will happily let you create files that appear to have slashes in their name, as shown here by the Finder:

<img src="/images/2021/slashed_files.png" style="width: 644px;" alt="A Finder window with two entries. The first is a folder named 'a/b/c' (a slash b slash c), the second is a text file named 'x/y/z' (x slash y slash z).">

I made the folder with the "New Folder" button in Finder, and the text file by saving it in TextEdit.
Even though I understand how this works, it breaks my brain a bit every time.

If you didn't know how this works, you could get a clue by running `ls`:

```console
$ ls
a:b:c/     x:y:z.txt
```

The files have either colons or slashes in their name, depending on how you look at them.

I don't understand all the nuances, but I know this is a side-effect of the fact that macOS has not one but *two* path separators: the slash (`/`) and the colon (`:`).
The two separators are used in different contexts, and the system will translate between them as needed.

These two separators reflect the two parent systems of modern macOS: [classic Mac OS] and the [Unix-like NeXTSTEP].
When they were joined together, Apple's engineers had to build a file system that was compatible with both the classic Mac's file system ([the Mac OS Extended File System, aka HFS+][hfs+]), and with NeXTSTEP's file system (the Unix file system, aka UFS).
Among other differences, these systems had different path separators: HFS+ used a colon, while UFS used a slash.

There's a [Usenix 2000 paper written by several Apple engineers][usenix2000] which describes the problems of combining classic Mac OS and Unix in more detail.
It actually describes exactly what we're seeing with the Finder and `ls`:

> [The translation layer] can create a user-visible schizophrenia in the rare cases of file names containing colon characters, which appear to Carbon applications as slash characters, but to BSD programs and Cocoa applications as colons.

AppleScript is where you're most likely to encounter colons as path separators in modern macOS:

```console
$ which osascript
/usr/bin/osascript

$ osascript -e 'tell application "Finder" to get (path to me)'
alias Phoenix SSD:usr:bin:osascript
```

This is likely because AppleScript goes back to System 7, which only had to care about HFS+ and colons.
It can give you a UNIX- (or POSIX-) style path, but you have to ask for it explicitly:

```console
$ osascript -e 'tell application "Finder" to get POSIX path of (path to me)'
/usr/bin/osascript
```

In 2017, Apple replaced HFS+ with [the Apple File System, aka APFS][APFS], but these dual path separators remain.
I can't find any documentation to confirm it, but I assume that's for backward compatibility reasons -- picking a single path separator would break an enormous amount of software.

The "slashes in filenames" breaks my brain because I started programming after Unix-style filesystems had become totally dominant.
In my mind, slash is *the* directory separator, and Windows is weird for using the backwards slash (`\`).
In reality, file systems have used [a variety of directory separators][separator], and it's only the current Unix hegemony that makes this seem weird.
On another timeline, forward slashes in a filename would seem totally normal.

[classic Mac OS]: https://en.wikipedia.org/wiki/Classic_Mac_OS
[Unix-like NeXTSTEP]: https://en.wikipedia.org/wiki/NeXTSTEP
[hfs+]: https://en.wikipedia.org/wiki/HFS_Plus
[usenix2000]: http://www.wsanchez.net/papers/USENIX_2000/
[APFS]: https://en.wikipedia.org/wiki/Apple_File_System
[separator]: https://en.wikipedia.org/wiki/Path_(computing)#Representations_of_paths_by_operating_system_and_shell
