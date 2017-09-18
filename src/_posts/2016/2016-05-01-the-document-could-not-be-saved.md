---
date: 2016-05-01 19:55:00 +0000
layout: post
slug: os-x-hates-textmate
summary: "Debugging a strange interaction between TextMate and OS X\u2019s security\
  \ system."
tags: os-x textmate
title: "\u201CThe document could not be saved\u201D"
---

I try not to make unreasonable complaints about the quality of software.
I write software for a living, and writing bug-free software is *hard*.
A trawl through the code I've written would reveal many embarrassing or annoying bugs.
People in glass houses, etc.

But I do have some basic expectations of the software I use.
For example, I expect that my text editor should be able to open, edit, and save files.

![A screenshot of a TextMate window showing a dialog "The document 'hello.txt' could not be saved.  Please check Console output for reason."](/images/2016/textmate-error.png)

Two days ago, TextMate on my laptop decided it didn't fancy saving files any more.
Actually, it decided that ⌘+S should do nothing, and trying to click "Save" in the File menu would throw this error dialog.
A trawl of Google suggests that I'm the only person who's ever hit this error.
If so, here's a quick write-up of what I tried for the next person to run into it.

<!-- summary -->

I still don't fully understand what caused the problem, but this is what I tried to fix it:

*   **Check the logs in Console.app.**

    The "Console output" in the error message refers to [Console.app][console], the log viewer that can be found in the Utilities folder.
    Unfortunately, I could see literally nothing being logged when I tried to save files.
    Whatever caused this was keeping schtum.

*   **Blow away the app config and start from scratch.**

    I deleted the app configuration with [AppCleaner][cleaner] and downloaded a fresh copy of TextMate from GitHub.
    I'd assumed this was a problem with TextMate flakiness, so starting afresh would fix things, right?
    Nope.

*   **Reboot or restart in Safe Mode.**

    Turning it off and on again didn't help, nor did restaring my Mac in [Safe Mode][safemode].

*   **Delete the quarantine attribute.**

    My newly downloaded version of TextMate had quarantine attribute, because I'd downloaded it via Safari:

    <div class="codehilite"><pre><span></span><span class="gp">$</span> xattr -l TextMate.app
    <span class="go">com.apple.quarantine: 0062;57264649;Safari;EB7AAA88-11E1-42E8-9D88-D90B03E5973E</span>
    </pre></div>

    Usually this attribute is used by the Finder to warn you about the dangers of opening files saved from the Internet.
    Perhaps OS X thought that TextMate was too dangerous to be allowed write privileges?

    Deleting this attribute is potentially risky, but I'd downloaded the file directly from GitHub over HTTPS.
    I threw caution to the wind:

    <div class="codehilite"><pre><span></span><span class="gp">$</span> xattr -r -d com.apple.quarantine TextMate.app
    </pre></div>

    But the app persisted in its stubbornness.

*   **Delete my system cache files.**

    TextMate 2 has historically been a bit flakey for me, but after starting afresh twice and completely scrubbing the system, I was pretty sure it wasn't to blame.
    If it was hitting an internal error, I'd hope it would give a more useful log – either in Console.app, or in the error dialog.
    At this point, I was more suspicious of OS X.

    I blew away the contents of `~/Library/Cache`, and finally TextMate spluttered into life.
    I don't know if this alone fixed the problem, or if it was the combination of the above – I don't really care, I could finally save files again!

I strongly suspect this was an overzealous security system that thought TextMate shouldn't be allowed write access.
It's definitely one of the things that the OS X sandbox is able to limit, and it wouldn't be the first time it's gone on a rampage.
(A few months back, it decided to block opening any text file, and I had to restore from backup.)

In years past, Apple liked to trumpet the superior security of Mac&nbsp;OS.
But security is always a trade-off between safety and usability, and when it goes wrong like this, it leaves a sour taste in the mouth.
This bug is unlikely to show up in any of Apple's quality metrics &ndash; there's no crash, not even an error log, but it is annoying.

I'd love to see Apple focus on bugfixes and stability in the next few releases of OS X.
This sort of bug seems rare, but it would be even better if it was non-existent.

[cleaner]: https://freemacsoft.net/appcleaner/
[safemode]: https://support.apple.com/en-us/HT201262
[console]: https://en.wikipedia.org/wiki/List_of_OS_X_components#Console
