---
layout: note
date: 2026-06-28 23:26:15 +01:00
title: Managing the caption of a photo with AppleScript (but not PhotoKit)
summary: Get/set the `description` of the corresponding `media item` in the Photos app.
topics:
  - Photo management
  - AppleScript
---
In the macOS Photos app, you can set a "caption" for a photo (select **Window** > **Info**, then look for the **Caption** field below a photo).

As far as I can tell, the only way to manage this caption programatically is using AppleScript -- it's not exposed to the PhotoKit APIs.

## Get the description

Look at the `description` field of a `media item` from the Photos Suite.
Here's a script that takes a [local identifier][me-local-identifier] as an argument, and prints the caption (if set):

```applescript {"names":{"2":"argv","3":"targetId","7":"targetMedia","12":"desc"}}
#!/usr/bin/env osascript

on run argv
  set targetId to item 1 of argv

  tell application "Photos"
    set targetMedia to media item id targetId
    set desc to description of targetMedia
    
    if desc is missing value then
      return ""
    else
      return desc
    end if
  end tell
end run
```

## Set the description

Set the `description` field.
Here's a script that takes a local identifier and new caption as arguments:

```applescript {"names":{"2":"argv","3":"targetId","6":"newCaption"}}
#!/usr/bin/env osascript

on run argv
  set targetId to item 1 of argv
  set newCaption to item 2 of argv

  tell application "Photos"
    set targetMedia to media item id targetId
    set description of targetMedia to newCaption
  end tell
end run
```

[me-local-identifier]: /2023/managing-albums-in-photos/#local-identifiers-unambiguously-specify-photos-and-albums