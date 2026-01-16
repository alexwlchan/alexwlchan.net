---
layout: post
date: 2023-12-29 07:46:33 +00:00
title: Getting the path to the note I have open in Obsidian
summary: Although Obsidian doesn’t support AppleScript, I can use System Events to find out which note I have open.
tags:
  - obsidian
  - applescript
---
I have a bunch of Python scripts I use to clean up text files, and I call them by passing the path to the text file as an argument, for example:

```console
$ python clean_up_text.py /path/to/text/file.md
```

This is mostly fine, but finding that path is a bit annoying when I want to run them on a note I have open in Obsidian.
It's not hard, it just takes a few steps – open the "More options" menu, click "Reveal in Finder", drag the file from Finder into terminal.
I wanted a way to make it a bit quicker.

I've written a little script which gives me a path to the note I currently have open in Obsidian, so now I can run something more like:

```console
$ python clean_up_text.py $(path_to_frontmost_obsidian_note)
```

I've managed to do this with a bit of AppleScript and Python, even though Obsidian doesn't have any AppleScript support.

---

The inspiration for this script was another script I have for getting the frontmost URL from my web browser.
The crux of that script is a single line of AppleScript that controls Safari:

```applescript
tell application "Safari" to get URL of document 1
```

Unfortunately this isn't quite as simple in Obsidian – it doesn't have any AppleScript support, so you can't do anything with `tell application "Obsidian"`.

(The lack of AppleScript is annoying, but understandable.
It's a niche technology on a marginal platform, and Apple seems to have completely forgotten it exists.
Much as I find AppleScript useful, it's hard to justify the time/effort to add support for it in a new app today.)

But even if Obsidian doesn't have its own AppleScript dictionary, it is still visible from the AppleScript universe – as a process in System Events.
We can't see much, but we can see its windows, for example:

```applescript
tell application "System Events"
    tell process "Obsidian" to get title of front window
end tell
```

The window title has three parts, separated by hyphens: the name of the note, the name of the vault, and the Obsidian version:

```
Short story ideas - textfiles - Obsidian v1.4.16
```

This is the same title that shows up in the "Window" menu – it's a bit of Obsidian poking into macOS where AppleScript can see it.
Because Obsidian always uses the title as the filename (e.g. this file is called `Short story ideas.md`), we can use this to find the path to the Markdown file.

---

To find the Markdown file, you match the vault name to a folder on disk, then you search for files that match the note title.
There are a bunch of ways you could do this; I picked Python because that's what I'm familiar with, but you could use another language just as easily.

This is the script I wrote, which I named [`obnote`](https://github.com/alexwlchan/scripts/blob/main/macos/obnote).
Hopefully the comments are enough to explain what's going on:

```python
#!/usr/bin/env python3
"""
Print the path to the Markdown file which is currently open
in Obsidian (if any).

This relies on knowing the on-disk locations of my Obsidian vaults,
so you won't be able to use this without changing it for your own setup.

Note: this will print the *first* file with the same name as your
open note, which may cause issues if you have multiple notes with
the same title.
"""

import os
import subprocess


def get_file_paths_under(root=".", *, suffix=""):
    """
    Generates the absolute paths to every matching file under ``root``.

    See https://alexwlchan.net/2023/snake-walker/
    """
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            p = os.path.join(dirpath, f)

            if os.path.isfile(p) and f.lower().endswith(suffix):
                yield p


def get_applescript_output(script):
    """
    Run an AppleScript command and return the output.
    """
    cmd = ["osascript", "-e", script]

    return subprocess.check_output(cmd).strip().decode("utf8")


if __name__ == "__main__":
    window_title = get_applescript_output("""
        tell application "System Events"
            tell process "Obsidian" to get title of front window
        end tell
    """)

    # The window title will be something of the form:
    #
    #     Short story ideas - textfiles - Obsidian v1.4.16
    #
    note_title, vault_name, _ = window_title.rsplit(" - ", 2)

    # Match the vault name to a path on disk.
    #
    # This is very specific to my setup, so if you want to use it on
    # your computer, you'll need to customise this bit.
    if vault_name == "textfiles":
        vault_root = os.path.join(os.environ["HOME"], "textfiles")
    else:
        raise ValueError(f"Unrecognised vault name: {vault_name}")

    # Find Markdown files that match the name of this note.
    for path in get_file_paths_under(vault_root, suffix=".md"):
        if os.path.basename(path) == f"{note_title}.md":
            print(path, end="")
            break
    else:  # no break
        raise RuntimeError(f"Could not find note with title {note_title}")
```

This does assume that notes have unique titles – that I won't, for example, have two notes in different folders both called `Short story ideas.md`.
That's true in my vault, but you might want to be careful using it if you reuse note titles.

Now I can invoke my text cleanup scripts like so:

```console
$ python clean_up_text.py $(obnote)
```

This is especially useful when I want to run the same cleanup script on multiple notes in quick succession.
I can run this command once, switch to Obsidian and select a new note, then return to my terminal and press `up-arrow` and `enter` to run the cleanup on my new note.

There are lots of other ways you could solve this problem – for example, I realised as I wrote this post that you could look at the `.obsidian/workspace.json` file – but this works for me, and I had a bit of fun while writing it.
