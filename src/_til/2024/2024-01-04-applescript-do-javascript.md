---
layout: til
date: 2024-01-04 22:59:15 +00:00
date_updated: 2024-01-20 11:48:34 +00:00
title: "Get and manipulate the contents of a page in Safari with `\"do JavaScript\"`"
tags:
  - safari
  - applescript
---
Here's an AppleScript which runs `document.querySelector` in a Safari tab and returns the matching HTML:

```applescript
tell application "Safari"
    tell document 1
        get (do JavaScript "document.querySelector(\"main\").innerHTML")
    end tell
end tell
```

## You need that `.innerHTML` property

If you try to run the AppleScript without the `.innerHTML` property, e.g.

```applescript
set selectedText to (do JavaScript "document.querySelector(\"main\")")
```

You get an error further down in the script:

```
The variable selectedText is not defined.
```

I suspect this is because `document.querySelector` returns some sort of DOM object which AppleScript doesn't know how to store in a variable, whereas `.innerHTML` returns a string that it can store quite happily.

## Use case #1: Get the contents of tweets I have open in Safari

I wanted a way to programatically get the contents of tweets I had open in Safari.
This is the AppleScript I used:

```applescript
tell application "Safari"
    tell document 1
        get (do JavaScript "document.querySelector('article').innerHTML")
    end tell
end tell
```

Alternatives that didn't work:

*   I used to use the Twitter API, but there's no (reasonably priced) read API for me to use.
*   Because Twitter relies so heavily on JavaScript, fetching the page separately (e.g. `curl https://twitter.com/…`) doesn't actually get the contents of the tweet – it just gets an error page, or a page with the JS that will eventually load the tweet.
*   Similarly, this breaks the `get source` action in AppleScript (`tell application "Safari" to get source of document 1`) – the HTML it returns doesn't contain the contents of the tweet.

But the rendered HTML is available to JavaScript running on the page, so we can exfilitrate it this way.

## Use case #2: Move videos between YouTube accounts

I had two YouTube accounts, and I wanted to move videos from the "Watch Later" playlist in one to the other.
I opened the two accounts in different windows, and then I repeatedly ran this AppleScript:

```applescript
tell application "Safari"
    -- Get the path to the video at the top of the playlist in window 1
    -- e.g. /watch?v=123456789
    tell tab 1 of window 1
        set theYouTubeUrl to do JavaScript "document.querySelector('a#video-title.ytd-playlist-video-renderer').getAttribute('href')"
    end tell

    tell tab 1 of window 2
        -- Open that video in window 2, and wait for it to load
        set the URL to "https://www.youtube.com" & theYouTubeUrl
        delay 5

        -- Open the actions menu, which contains the "Save" button, and wait
    -- for the menu to open
        do JavaScript "document.querySelector('button[aria-label=\"More actions\"]').click()"
        delay 1

        -- Click the "Save" button, and wait for the next dialog to appear
        do JavaScript "document.querySelectorAll('.ytd-menu-service-item-renderer').forEach(function(r) { if (r.innerHTML === 'Save') { r.click(); } })"
        delay 1

        -- The next dialog will show a list of playlists; click the checkbox
        -- for "Watch Later"
        do JavaScript "document.querySelector('yt-formatted-string[aria-label=\"Watch Later Private\"]').click()"
    end tell

    tell tab 1 of window 1
        -- Open the "Actions" menu in window 1, which includes the "Remove from
    -- Watch Later" button.
        do JavaScript "document.querySelector('.ytd-playlist-video-list-renderer button[aria-label=\"Action menu\"]').click()"
    end tell
end tell
```

I don't automatically click the "Remove from Watch Later" button, because this isn't 100% reliable – sometimes it won't get to the Save button if the video takes too long to load, or it's a "YouTube for Kids" video that can't be saved for later.
But it did save me a lot of clicking!
