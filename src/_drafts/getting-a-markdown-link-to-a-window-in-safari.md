---
layout: post
title: Getting a Markdown link to a window in Safari
tags: macos applescript automation
---

Here's an AppleScript I wrote today, which gets a Markdown-formatted link to whatever's in my frontmost Safari window:

```shell
tell application "Safari"
  set theName to get name of tab 1 of window 1
  set theURL to get URL of tab 1 of window 1

  log "[" & theName & "](" & theURL & ")"
end tell
```

It creates something like:

```
[Getting a Markdown link to a window in Safari – alexwlchan](https://alexwlchan.net/2020/07/getting-a-markdown-link-to-a-window-in-safari/)
```

I use it when the URL doesn't contain much useful information (say, an article ID that's entirely numeric), and I want a bit more context for why I saved a particular link.

This is one of several automations that I have to get URLs from my browser.
Each of them saves a couple of clicks, and it means I don't break my writing flow going to the browser to copy/paste a URL.

I wrote about [an automation for getting tweets](/2019/11/saving-a-copy-of-a-tweet-by-typing-twurl/) last year, and the original idea I got [from Dr. Drang](https://leancrew.com/all-this/2009/07/safari-tab-urls-via-textexpander/) over a decade ago.
I have it bound to `;mdurl` using Keyboard Maestro, with `;md2url` for the second window (if I'm typing into a text box in Safari).
