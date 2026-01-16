---
layout: til
date: 2024-04-01 20:14:30 +01:00
title: The `open` command can ask questions
summary: |
  If you pass an argument that can't be easily identified as a file or a URL, `open` will ask you what to do next.
  This may be a surprise if you were trying to use it in a script.
tags:
  - shell scripting
  - macos
---
This is something I discovered by accident -- I had a shell script that called `open *.mp3`, and it offered me a selection prompt rather than just opening the file.

After a bit of investigating, it turned out to be caused by a file with a colon in the filename.
Here's a minimal example that shows this behaviour:

```console
$ touch 'A:B.mp3'
$ open A:B.mp3
A:B.mp3?
[0]	cancel
[1]	Open the file A:B.mp3
[2]	Open the URL  (null)

Which did you mean?
```

I suspect this is because `open` can open URLs in a web browser as well as open files on disk, and the colon makes it unclear which it should do.
If you put something that looks more like a URL in here, the ambiguity is more obvious:

```console
$ open http://localhost:5858
http://localhost:5858?
[0]	cancel
[1]	Open the file http://localhost:5858
[2]	Open the URL  http://localhost:5858

Which did you mean?
```

This could mean _"a file called `localhost:5858` in the `http` folder"_, or it could mean _“the URL `http://localhost:5858`”_ -- and both of those options can work!

## Can you tell `open` what to pick?

Kinda.

From the man page on macOS Ventura:

```
-u  Opens URL with whatever application claims the url scheme, even if
    URL also matches a file path
```

So for example, this command will open the URL in my web browser:

```console
$ open -u http://localhost:5858
```

There doesn't seem to be a corresponding flag for "always open this as a file path".
Even if you specify an application name with the `-a` flag, it still prompts you for ambiguous filenames.

You can force it to open with TextEdit (`open -e`) or the default text editor (`open -t`), but that's only useful if you're opening a text file.

Note also that the `-u` flag seems to be relatively new: it doesn't appear in either copy of the `open(1)` man page that I found online ([unix.com](https://www.unix.com/man-page/osx/1/open/), [ss64.com](https://ss64.com/mac/open.html)).

## Never trust arbitrary input!

The reason I had filenames with colons is because I was using `youtube-dl` to download some YouTube videos, and it puts the video title in the filename.
When I downloaded a file with a colon in the title, I got the unexpected `open` behaviour.

For a simple script this is fine, but it may cause issues elsewhere -- e.g. if you're calling `open` in a context where you're not expecting it to ask for input.