---
layout: post
date: 2024-09-18 06:45:46 +00:00
title: Going between Finder and the Terminal
summary: A few shell scripts I use to go between the Finder and the Terminal.
tags:
  - macos
  - automation
colors:
  index_light: "#565656"
  index_dark:  "#dbe3e9"
---
Earlier this week, Dr. Drang [wrote a post][drang] about a few automations he uses to go between the Terminal's command line and the Finder's GUI.
He has some neat ideas, and I particularly like his AppleScript `sel` for selecting multiple items in Finder.
I've written a couple of similar scripts, and I thought they were worth sharing.

[drang]: http://www.leancrew.com/all-this/

## `reveal` (aka `open -R`)

The [`open` command](https://ss64.com/mac/open.html) is a versatile tool.
It's normally used to open files, but you can pass the `-R` flag to reveal a file or folder in Finder instead:

```console
$ open -R ~/repos/alexwlchan.net/README.md
```

When you run this command with the path to a folder, it activates Finder and opens a window to that folder.

When you run this command with the path to a file, it activates Finder and opens a window to the folder that contains that file.
It also highlights the file in the folder:

{%
  picture
  filename="open_r.png"
  alt="A Finder window in column view with the folder 'alexwlchan.net' opened, and inside the folder the file 'README.md' is highlighted."
  width="600"
  class="screenshot"
%}

This is useful if I'm working on a file in the terminal, and I want to do something with it in the Finder.
I've used it as [I clean up my messy data](/2024/digital-decluttering/) -- I run terminal scripts to identify files I could purge, then I open them in Finder and check they're the right file before actually deleting them.
I also use it when I'm looking for files -- I have directories with hundreds of files, and path-completion in the fish shell can make it easier to find a file in Terminal than in Finder.

I wrap this in a small shell script called `reveal`:

```shell
#!/usr/bin/env sh
# Reveal the file/folder in the Finder.
#
# Usage examples:
#
#     reveal .                    # reveal the current folder
#     reveal ~/Desktop            # reveal a folder
#     reveal ~/Desktop/cat.jpg    # reveal a file
#

set -o errexit
set -o nounset

open -R "$@"
```

This alias might seem redundant -- `reveal` is only one character shorter than `open -R` -- but the purpose of aliases isn't just to save typing; it's also to make things easier to find.

I've forgotten `open -R` half a dozen times because I think of "open" as "open a document in an application".
Browsing files in the Finder feels like a different activity, so I never remember I can do Finder-related things with the `open` command.

The word "reveal" is a better fit for how I think of this action, so I actually remember to use it.

A couple of notes:

*   You can use `open -R` with an absolute path, or with a path that's relative to your working directory.
    Both of these commands reveal the same file:

    ```console
    $ open -R ~/repos/alexwlchan.net/README.md
    $ cd ~/repos/alexwlchan.net; open -R README.md
    ```

    It also supports passing `file:///` URIs, which can point to folders or files:

    ```console
    $ open -R file:///Users/alexwlchan/repos/alexwlchan.net
    $ open -R file:///Users/alexwlchan/repos/alexwlchan.net/README.md
    ```

    I use these a lot when I'm testing static websites on my Mac.

*   `open -R` is smart enough to know whether you already have the relevant folder open in a Finder window.
    If you already have a Finder window open in the folder, it brings that window to the front and highlights the file, rather than creating a new window.

*   I only use `open -R` with one file at a time.
    If you try to reveal multiple files this way, it opens a new Finder window for every file -- even if they're in the same folder.
    If you want to select multiple files in a single Finder window, you should look at Dr. Drang's `sel` script.

## `ffile`

Suppose I'm working in the Finder, and I want to run a script against a file.
I structure a lot of my scripts so they take a path to a file as a command-line argument, then do some processing on that file.
If it's easier to find the file in Finder than in the Terminal, I need a way to get the path of files I'm looking at into the Terminal.
I could find the file manually, or drag the file's [proxy icon](https://leancrew.com/all-this/2016/07/intuitive-by-proxy/) into the Terminal (which inserts the complete path for you), but I find both of those too slow.

I have an AppleScript `ffile` that prints the path of the file I have selected:

```applescript
#!/usr/bin/env osascript
# Get the path to the first item which is selected in the
# frontmost Finder window.

tell application "Finder"
  get POSIX path of first item of (selection as alias list)
end tell
```

I picked this name because it makes me think "finder file".

I can use `ffile` to get the path to the selected file I have in Finder, or pass that path to another script:

```console
$ ffile
/Users/alexwlchan/repos/alexwlchan.net/README.md

$ python3 run_my_script.py (ffile)
```

This gives me an efficient way to run the same script over multiple files, one-by-one.
I select the first file in Finder, and write my command using `ffile`.
Then when I select the next file in Finder, I can use `up arrow`, `enter` to select the previous command from history, and run it unmodified -- because `ffile` will get the path to the new file.
I can run the same command repeatedly, without having to copy a new path each time.

This only gets the first item of the selection, which is fine for me.
Here "first" means "the first item you clicked" -- Finder remembers the order that you selected your files.
If I want to get the paths of multiple files, I usually drag the selection from Finder into the Terminal.

## `trash`

There are two ways to delete files on macOS.

If you're in the Terminal, you can use the Unix [`rm` command][rm] to remove a file, which deletes it immediately.
If you're in Finder, you can move the file to the Trash.
That leaves the file on disk, but gives you a safety net to recover the file until you empty the Trash.

If I want the safety net of the Trash when I'm deleting a file from the Terminal, I could use `ffile` to reveal the file in Finder and delete it from there -- but that's one too many steps.
Instead, I wrote an AppleScript `trash.scpt` that moves files and folders to the Trash:

```applescript
#!/usr/bin/env osascript
# Move one or more files to the Trash in macOS.
#
# Examples:
#
#     osascript trash.scpt ~/Desktop/cat.jpg     # Trash a single file
#     osascript trash.scpt ~/Desktop/photos      # Trash a folder
#     osascript trash.scpt dog.png fish.gif      # Trash multiple files at once
#

on run argv
  repeat with filePath in argv
    set posixPath to (POSIX file filePath)

    tell application "Finder"
      if posixPath exists
        log filePath
        delete posixPath
      end if
    end tell
  end repeat
end run
```

The key is the `delete` command in the Finder's AppleScript dictionary, which deletes a file by moving it to the Trash rather than deleting it from disk.

I get the command-line arguments with `on run argv`, and iterate over them using `repeat with filePath in argv`.

I have to convert the path to a `POSIX file` before I pass it to the `delete` command.
I don't really understand how paths and aliases work in AppleScript; it's always trial and error until I get something that works.

The `delete` command fails if you try to delete a non-existent file, so I added a manual check that the file exists.
In theory this exposes a race condition, where the file could be deleted between my check and calling the `delete` command, but that's very unlikely to happen on my local disk.

The output from this script is a bit strange -- I'm manually printing the names of the files as they get deleted (`log filePath`), but it also prints an AppleScript log for the last file that gets deleted:

```console
$ osascript trash.scpt dog.png fish.gif
dog.png
fish.gif
document file fish 07.51.23.gif of item .Trash of folder alexwlchan of folder Users of startup disk
```

To improve the output, I've wrapped the AppleScript in a shell script:

```shell
#!/usr/bin/env bash
# Move one or more files to the Trash in macOS.
#
# Examples:
#
#     trash ~/Desktop/cat.jpg     # Trash a single file
#     trash ~/Desktop/photos      # Trash a folder
#     trash dog.png fish.gif      # Trash multiple files at once
#

osascript trash.scpt "$@" 2>&1 1>/dev/null
```

The `"$@"` forwards all the arguments from the shell script to the underlying AppleScript.
The AppleScript log (`document file …`) is being printed to stdout, which I'm discarding with `1>/dev/null`.
My manual logs (`log filePath`) are being printed to stderr, which I'm redirecting to stdout with `2>&1`.
It's awkward but it does the job.

This script isn't as robust as I'd like, but it's good enough, and I have an easy exit hatch if something goes wrong.
I've used it plenty of times and never had any issues, but if it ever breaks I can always open the file in Finder and trash it that way instead.

You can also move an item to the Trash [using Swift][swift], so maybe I'll rewrite this script if AppleScript ever flakes out on me -- but for now, why replace something that works?

[rm]: https://ss64.com/mac/rm.html
[swift]: https://developer.apple.com/documentation/foundation/filemanager/1414306-trashitem
