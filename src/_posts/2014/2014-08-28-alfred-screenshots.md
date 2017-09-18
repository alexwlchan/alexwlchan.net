---
date: 2014-08-28 00:32:00 +0000
layout: post
slug: alfred-screenshots
tags: alfred applescript
title: A quick Alfred workflow for opening recent screenshots
---

I'm a big fan of the productivity app [Alfred][alf]. It's one of the
first apps I install on any new Mac, and I use it dozens of times a day.
Here's a quick workflow I whipped up this morning.

[alf]: http://www.alfredapp.com/

When I take a screenshot, I usually want to use it immediately. I could
navigate to my screenshots directory in Alfred, or find it in Finder,[^1]
but it's such an easy task to automate.
I wrote a short workflow to open my most recent screenshot in the Alfred file browser.

<!-- summary -->

We can use AppleScript to get the most recently created file in the
screenshots directory, which should be the latest screenshot:

```applescript
set screenshotFolder to ("/Users/alexwlchan/screenshots" as POSIX file)
set screenshots to (get every file of folder screenshotFolder)
set latestScreenshot to item 1 of reverse of (sort screenshots by creation date)
```

In the final line, we can replace `item 1` by `item n`, for an
integer&nbsp;*n*, to get the *n*th most recent screenshot.

I then put this into a very simple workflow in Alfred. The input is a
keyword (I used "screenshot"), with an optional argument to determine
which screenshot you want. This is connected to a "Run NSAppleScript"
action with the following script:

```applescript
on alfred_script(q)
    tell application "Finder"
        if q is "" then set q to 1
        set screenshotFolder to ("/Users/alexwlchan/screenshots" as POSIX file)
        set screenshots to (get every file of folder screenshotFolder)
        set latestScreenshot to item q of reverse of (sort screenshots by creation date)
    end tell
    search (POSIX path of (latestScreenshot as alias))
end alfred_script
```

Here `q` is the argument passed by the Keyword input. If we don't supply
an argument, then Alfred gives an empty string, so we default to using 1,
for the most recent screenshot. Then we pass the path to this file as
a string to the `search` command, which opens the image in the Alfred
file browser. From there, I can apply any one of my Alfred workflows to
the image, although normally I just open it in Preview for editing.

If you like, you can [download the workflow](/files/open-recent-screenshots.zip).
You'll need to set the path for your own screenshots folder before using
it, but that's all the setup it needs.

I'll be sharing more of my Alfred workflows here in the future. It's an
incredibly versatile app, and I highly recommend [checking it out][alf].

[^1]: Although Mavericks has developed an interesting bug in which new
screenshots don't always show up in the Finder. To make them appear, I
have to look them up with the "Reveal in Finder" command in Alfred.
