---
layout: post
title: Using AppleScript to open a URL in Private Browsing in Safari
tags: applescript
---

I have a bunch of automations that open URLs.

If I want to open a regular window in Safari (my default browser), I have a variety of options -- I can use [open(1)](https://linux.die.net/man/1/open) on the command-line, or the [webbrowser module](https://docs.python.org/3/library/webbrowser.html) in Python, or with AppleScript, or probably half a dozen other methods I haven't thought of.

If I want to open a private browsing window, my options are more limited.
The Safari AppleScript dictionary doesn't know about private browsing, and all the other approaches I've seen are just passing Safari the URL to open.
They can't give it any instructions beyond "please open this URL".

If you ask Google, there are lots of suggestions, but I struggled to find good code.
Many of the results are broken, slow, or incomplete (they open the private browsing window, but not any URLs).

Rather than wade through more Google results, I came up with my own script for doing it, which opens the window *and* the URL:

```applescript
#!/usr/bin/env osascript

on openPrivateBrowsingWindow(urlToOpen)
  tell application "Safari"
    activate

    tell application "System Events"
      click menu item "New Private Window" of ¬
        menu "File" of menu bar 1 of ¬
        application process "Safari"
    end tell

    -- The frontmost window is the private Browsing window that just got
    -- opened -- change the URL to the one we want to open.
    tell window 1 to set properties of current tab to {URL:urlToOpen}
  end tell
end openPrivateBrowsingWindow

on run argv
  openPrivateBrowsingWindow(argv)
end run
```

I save this as a script in my $PATH and mark it as executable, and then I can open a new private browsing window from anywhere by running:

```console
$ open_private_browsing "https://example.org"
```

When you run this code, you may get an error (or a silent failure if you trigger it through a GUI rather than a terminal):

> open_private_browsing:114:232: execution error: System Events got an error: osascript is not allowed assistive access. (-1719)

This is the macOS security system kicking in: it doesn't let arbitrary scripts or applications click menu items in other applications.
To allow this script to work, open the *Security & Privacy* preference pane.
Under *Accessibility*, allow access to whatever application is triggering the script (in my case, iTerm 2), and it should be good.
