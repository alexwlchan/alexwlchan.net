---
layout: post
date: 2014-06-23 13:04:00 +0000
tags: instapaper applescript
title: Catching instapaper:// URLs from ReadKit
---

I use [ReadKit][rk] to manage my Instapaper queue on my Mac.
Although Instapaper's web interface is much nicer than it used to be, I still prefer ReadKit for processing lots of items at once.
But sometimes I try to open an item in Safari, and I get an error:

> **There is no application set to open the URL instapaper://private-content/480777221.**
>
> Search the App Store for an application that can open this document, or choose an existing application on your computer.

These are items that I've [added to Instapaper by email][em], which don't have a URL associated with them in Instapaper's database.
(Email newsletters are one example.)
Instead, the URL refers to an Instapaper database entry, which Safari can't open.
If I was on iOS, an `instapaper://` URL would be redirected to the Instapaper iOS app.

But the item does exist in the Instapaper web interface, which can be opened in Safari.
It has a URL that looks like this:

```
https://instapaper.com/read/480777221
```

(Of course, that link doesn't work unless Safari is logged into my account, but I always am.)

I wanted a way to catch these `instapaper://` links, and redirect to the appropriate item in the web interface without hitting an alert.

<!-- summary -->

I started with this AppleScript:

```applescript
on open location instapaperURL

    set py_script to "python -c 'import sys; print sys.argv[1][29:]' \"" & instapaperURL & "\""
    set instapaper_id to (do shell script py_script)

    tell application "Safari"
        open location "https://www.instapaper.com/read/" & instapaper_id
        activate
    end tell

end open location
```

It gets passed a URL, and then extracts the item's ID with a Python one-liner.
(I'd use AppleScript, but jumping through the hoops of AppleScript text delimiters is unnecessarily verbose here.)
Once AppleScript has the ID, it constructs the URL for the web interface, and passes that to Safari.

This gets saved *as an app*, not as a script.
When it gets run, it's supposed to be passed a URL, and then it runs the script above.

So I needed to register the app as able to open `instapaper://` URLs.
I edited the `Info.plist` file in the app bundle (right click > Show Package Contents…) to add the following lines:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLName</key>
        <string>Instapaper</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>instapaper</string>
        </array>
    </dict>
</array>
```

Now any `instapaper://` URLs get passed to this small app, which processes them using the script above and opens the web interface in Safari.
It's only a small annoyance, but it's another little thing that I don't need to think about again.

[rk]: http://readkitapp.com
[em]: https://www.instapaper.com/save/email
