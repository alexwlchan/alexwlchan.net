---
layout: post
title: Going between Finder and the Terminal
summary: A few shell aliases I use to go between the Finder and the Terminal.
tags:
  - macos
  - automation
---
Earlier today, Dr. Drang [wrote a post][drang] about a few automations he uses to go between the Terminal's command line and the Finder's GUI.
I particularly like his shell script `sel` for selecting multiple Finder items.

I have a couple of similar tools that I use, and I thought it would be worth sharing them for comparison.

[drang]: http://www.leancrew.com/all-this/

## `reveal` (aka `open -R`)

The [`open` command](https://ss64.com/mac/open.html) is a versatile tool.
It's normally used to open files, but you can pass the `-R` flag to reveal a file in Finder:

```console
$ open -R ~/repos/alexwlchan.net/README.md
```

When you run this command, it activates the Finder and opens a window to the folder that contains the file you selected.
It also highlights the file in the folder:

{%
  picture
  filename="open_r.png"
  alt="A Finder window in column view with the folder 'alexwlchan.net' opened, and inside the folder the file 'README.md' is highlighted."
  width="600"
  class="screenshot"
%}

This is useful if I'm working on a file in the terminal, and I want to do something with it in the Finder.
I've used it as I [clean up my messy data](/2024/digital-decluttering/) -- I use terminal scripts to identify files I could purge, then I open them in Finder to check they're the right file before actually deleting them.

I also use it for finding files sometimes -- I have directories with hundreds of files, and path-completion in the fish shell can make it easier to find a file in Terminal than in Finder.

I have this bound to an alias:

```console
$ alias 'reveal' 'open -R'
$ reveal README.md
```

This alias might seem silly -- `reveal` is only one character shorter than `open -R` -- but the purpose of aliases isn't just to save typing; it's also to make things easier to find.

I've forgotten `open -R` half a dozen times because I think of "open" as "open a document in an application".
Browsing files in the Finder feels like a different activity, so I'd never remember I could do Finder-related things with the `open` command.

The word "reveal" is a better fit for how I think of this action -- I'm revealing a file in Finder, nor opening it.

A couple of notes:

*   You can use `open -R` with an absolute path, or with a path that's relative to your working directory.
    Both of these commands reveal the same file:

    ```console
    $ open -R ~/repos/alexwlchan.net/README.md
    $ cd ~/repos/alexwlchan.net; open -R README.md
    ```

*   I mostly use `open -R` to reveal files, but it can also reveal folders:

    ```console
    $ open -R ~/repos/alexwlchan.net
    ```

*   `open -R` is smart enough to know whether you already have the relevant folder open in a Finder window.
    If you already have a Finder window open in the folder, it brings that window to the front and highlights the file, rather than creating a new window.

*   I only use `open -R` with one file at a time.
    If you try to reveal multiple files this way, it opens a new Finder window for every file.
    If you want to select multiple files in a single Finder window, you should look at Dr. Drang's `sel` script.

## `reveal (furl)`

As well as paths, you can use `open -R` with `file:///` URIs.
For example, this command reveals the file `index.html` in my `_site` folder:

```console
$ open -R file:///Users/alexwlchan/repos/alexwlchan.net/_site/index.html
```

I have a lot of static websites on my Mac -- local wikis, private image galleries, that sort of thing.
I open the HTML files in Safari, and then I can browse the site like any other.
They all appear with the `file:///` URI scheme, because the website is coming from my filesystem, not an HTTP server.

If I'm browsing a site and I want to find the website directory in the Finder, I can pass the `file:///` URI from Safari into `reveal`.
I have another shell alias [via Dr. Drang][furl] that lets me get the URL from the frontmost Safari window:

```console
$ alias furl="osascript -e 'tell application \"Safari\" to get URL of document 1'"
```

and I can combine this with `reveal`:

```console
$ reveal (furl)
```

and I can open the static website I'm looking at in the Finder.

[furl]: https://leancrew.com/all-this/2017/04/getting-urls-from-safari/

## `ffile`

Suppose I'm working in the Terminal, and I want to run a script against a file.
I structure a lot of my scripts so they take a path to a file as a command-line argument, then do some processing on that file.
If it's easier to find the file in Finder than in the Terminal, I need a way to get the path of the file I've found into the Terminal.

If you've selected a file in Finder, you can get the selection using AppleScript.
This is the AppleScript I use:

```applescript
tell application "Finder"
    get POSIX path of first item of (selection as alias list)
end tell
```

I wrap this in another shell alias using [osascript](https://ss64.com/mac/osascript.html):

```console
$ alias ffile 'osascript -e "tell application \"Finder\" to get POSIX path of first item of (selection as alias list)"'
```

I picked this name because it makes me think "finder file".
I'm not sure that name works, but it's stuck in my muscle memroy now.

I can then use `ffile` to get the path to the selected file I have in Finder, or pass a selected file to another script:

```console
$ ffile
/Users/alexwlchan/repos/alexwlchan.net/README.md

$ python3 run_my_script.py (ffile)
```

A couple of notes:

*   This only gets the first item of the selection, which is fine for me.
    AppleScript can get all the items, but in practice when I'm using this alias I only select one item at a time.

    Here "first" means "the first item you clicked" -- Finder remembers the order that you clicked on items.

*   This only gets the selection from the frontmost Finder window.
    If there's nothing selected in the frontmost window but you have selected something in the background window, it will fail rather than getting the selection from the background window.
