---
layout: post
date: 2019-06-09 10:36:43 +0000
title: Converting Acorn images on the command-line
summary: I wrote some AppleScript to help me do batch conversion of Acorn images into formats like PNG and JPEG.
tags: applescript acorn
category: Working with macOS
---

I've just finished creating some images for a new post, and I drew them all in the macOS image editor [Acorn].
Now I have a folder full of .acorn files, and I want to convert them all to PNG images.
You can convert an individual file to PNG in the Acorn GUI (*File > Save As… > Format > Save*), but that gets tedious with more than a few images.

Normally when I want to do batch image conversions, I whip up a quick Python script and I invoke [ImageMagick] via the command line, but ImageMagick doesn't know how to work with Acorn files:

```console
$ convert chui.acorn chui.jpg
convert: no decode delegate for this image format `ACORN' @ error/constitute.c/ReadImage/512.
convert: no images defined `chui.jpg' @ error/convert.c/ConvertImageCommand/3275.
```

Luckily, Acorn does have a pretty good AppleScript scripting dictionary, so we can build something to replace ImageMagick for this use case.
In this post, I'm going to walk through a short script I wrote that lets me convert Acorn images on the command line.
This is the interface I'm aiming for:

```console
$ convert_acorn chui.acorn chui.jpg
```

Note: I'm still using Acorn 5, so these commands might be slightly different if you're running Acorn 6.

[Acorn]: https://flyingmeat.com/acorn/
[ImageMagick]: https://imagemagick.org/index.php



## Opening and saving an image

If we have the path to an image, the Acorn dictionary makes it quite simple to open that file and save it to a new path.
Working in Script Editor:

```applescript
tell application "Acorn"
  set theDocument to (open "/Users/alexwlchan/Desktop/chui.acorn")
  save theDocument in "/Users/alexwlchan/Desktop/chui.png"
end tell
```

It's smart enough to work out that because I used the ".png" file extension, it should save a PNG file.
And it works even if the document is already open.

That alone could be enough!
Add a few command-line parameters, and I can trigger an image conversion from the command line.
But this script is a bit untidy -- it leaves the window open when it's done.
If I run this on 100 images, it'll open 100 Acorn windows, and that's bound to slow down my Mac.
It'd be nicer if it closed the windows when it's done.

Closing a document is a small addition:

```applescript
tell application "Acorn"
  set theDocument to (open "/Users/alexwlchan/Desktop/chui.acorn")
  save theDocument in "/Users/alexwlchan/Desktop/chui.png"
  close theDocument
end tell
```

But now it'll close the window even if it was already open -- for example, if it's an image I'm still tweaking.

The optimal behaviour would be for the script to close anything that wasn't already open, but leave everything else untouched.
This takes a bit more code.



## Is this image already open?

AppleScript gives us a way to iterate over the windows of an application:

```applescript
tell application "Acorn"
  repeat with theWindow in (every window)
    -- do stuff with the window
  end repeat
end tell
```

The brackets around `(every window)` aren't necessary, but I often add them in AppleScript to help me read it.
There are two words, but one unit.
In another language they might be a single variable like `allWindows`, so adding the parentheses helps me remember the logical grouping.

This loop seems to be a bit buggy -- sometimes if I close a window, it still gets counted.
I don't think this is Acorn-specific, because I've seen similar issues with Safari.
I also don't know how you can get around it, short of relaunching the app.
So let's be conservative and assume that if a window is in this loop, we shouldn't close it.

Each window can have an associated document, which is the file open in that window.
But we have to be careful -- every document is in a window, but not every window has a document.
For example, the Acorn tools palette and the colour picker both appear in this loop, but neither of them have an open document.

```applescript
set theDocument to (document of theWindow)
if theDocument is not missing value then
  -- do stuff with the document
end if
```

In turn, a document has an associated path, which is the location of the document on disk.
But that might be empty, if this is a new document that I haven't saved yet -- so we need to check for that too.


```applescript
set thePath to (file of theDocument)
if thePath is not missing value then
  -- do stuff with the path
end if
```

If we're still going, we know we're looking at an image which has been saved to the disk at least once.
Is it the image we're looking for?

If you inspect that variable, you'll see it's an AppleScript-style path:

```
Macintosh FusionDrive:Users:alexwlchan:Desktop:chui.acorn
```

Pretty much nothing else uses this style of path -- when I'm working on the command line, I'm always working with POSIX-style paths, such as:

```
/Users/alexwlchan/Desktop/chui.acorn
```

We can convert the AppleScript style path to a POSIX path, and compare it to the image we want to convert:

```applescript
if (POSIX path of thePath) = "/Users/alexwlchan/Desktop/chui.acorn" then
  save theDocument in "/Users/alexwlchan/Desktop/chui.png"
  return
end if
```

The `return` statement means the script will exit once it's done the export.

Stepping back, let's see what those nested loops look like put together:

```applescript
set originalPath to "/Users/alexwlchan/Desktop/chui.acorn"
set exportPath to "/Users/alexwlchan/Desktop/chui.png"

tell application "Acorn"
  repeat with theWindow in (every window)
    set theDocument to (document of theWindow)
    if theDocument is not missing value then
      set thePath to (file of theDocument)
      if thePath is not missing value then
        if (POSIX path of thePath) = originalPath then
          save theDocument in exportPath
          return
        end if
      end if
    end if
  end repeat

  set theDocument to (open originalPath)
  save theDocument in exportPath
  close theDocument
end tell
```

The three lines at the end handle the case where the image isn't already open -- it opens the image, does the export, then closes the window.

In another language, I'd reduce the nesting with a `continue` statement to skip to the next loop iteration.
That tends to make cleaner, more readable code -- but as far as I know, you can't do that in AppleScript.

If you copy and paste this code into the built-in Script Editor, you can trigger a conversion with Acorn.
But what if we want to go one step further, and trigger a conversion from the command line?



## Invoking AppleScript from the command line

You can run AppleScript on the command line with `osascript`.
For example, if you type this into a Terminal:

```console
$ osascript -e 'say "Hello World"'
```

You should hear your Mac speaking to you!

In a similar way, we can copy our code into a file, and add a shebang that says it should be run with `osascript`:

```applescript
#!/usr/bin/env osascript

set originalPath to "/Users/alexwlchan/Desktop/chui.acorn"
set exportPath to "/Users/alexwlchan/Desktop/chui.png"

tell application "Acorn"
  ...
```

If we then mark the file as executable (`chmod +x convert_acorn`), then typing `convert_acorn` at a command prompt will run our script.
Pretty neat, right?

What about parsing some command-line arguments?
If you wrap your entire script in `on run argv`, you then get access to command-line arguments.
Like so:

```applescript
on run argv
  if (count of argv) is not 2
    log "Usage: " & (name of me) &" <ORIGINAL_PATH> <EXPORT_PATH>"
    error number 1
  end if

  set arg1 to (item 1 of argv)
  set arg2 to (item 2 of argv)
  set workingDir to (do shell script "pwd") & "/"

  if arg1 starts with "/"
    set originalPath to arg1
  else
    set originalPath to workingDir & arg1
  end if

  if arg2 starts with "/"
    set exportPath to arg2
  else
    set exportPath to workingDir & arg2
  end if

  tell application "Acorn"
    ...
  end tell
end run
```

First the code checks that the user passes exactly two arguments, and exits with code 1 if not.
In the error message, the `me` object refers to the current script, and `name of me` is the filename -- this prints a usage message that includes the name of the file.

If you do pass two arguments, the next few lines need to convert whatever you're written into an absolute POSIX path.
This turns out to be a little tricky -- as far as I know, there's no built-in way to resolve a path passed as a command-line argument into an absolute path.

The code has to handle two cases:

*   You pass in a relative path (e.g. `chui.acorn`), or
*   You pass in an absolute path (e.g. `/Users/alexwlchan/Desktop/chui.acorn`).

This code is definitely fragile, but it works well enough for me in my limited testing, so I'll leave it for now.



## Putting it all together

This is the final script, including a comment at the top explaining how to use it:

```applescript
#!/usr/bin/env osascript

-- Convert an Acorn file to another format (for example, PNG or JPEG)
--
-- Takes two paths as arguments: the original path and the export path.
-- For example:
--
--    convert_acorn ~/Desktop/fire.acorn ~/Desktop/fire.png
--
-- will create a new PNG image.
--
-- The script tries to be well-behaved about your windows: if the Acorn file
-- is already open for editing, it uses that, otherwise it opens the file
-- and then closes it afterward.
--
-- Taken from https://alexwlchan.net/2019/06/acorn-on-the-command-line/

on run argv
  if (count of argv) is not 2
    log "Usage: " & (name of me) &" <ORIGINAL_PATH> <EXPORT_PATH>"
    error number 1
  end if

  set arg1 to (item 1 of argv)
  set arg2 to (item 2 of argv)
  set workingDir to (do shell script "pwd") & "/"

  if arg1 starts with "/"
    set originalPath to arg1
  else
    set originalPath to workingDir & arg1
  end if

  if arg2 starts with "/"
    set exportPath to arg2
  else
    set exportPath to workingDir & arg2
  end if

  tell application "Acorn"
    repeat with theWindow in (every window)
      set theDocument to (document of theWindow)
      if theDocument is not missing value then
        set thePath to (file of theDocument)
        if thePath is not missing value then
          if (POSIX path of thePath) = originalPath then
            save theDocument in exportPath
            return
          end if
        end if
      end if
    end repeat

    set theDocument to (open originalPath)
    save theDocument in exportPath
    close theDocument
  end tell
end run
```

To use it, copy that code into a file `convert_acorn` and make it executable with `chmod +x`.
Then copy that file somewhere to your path, and you can trigger Acorn conversions from the command line.

```console
$ convert_acorn chui.acorn chui.jpg
```

This won't save hours of time or make possible what was previously impossible, but it does save me a bunch of repetitive clicking, and you'll see the images it created in my next post!
