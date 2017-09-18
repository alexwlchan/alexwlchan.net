---
date: 2015-05-17 20:16:00 +0000
layout: post
slug: nvalt-and-marked
summary: A Python script that takes a note from nvALT and opens it in Marked.
tags: python
title: Previewing notes from nvALT in Marked
---

I find [nvALT][nv] to be an indispensable note-taking application. I have thousands of plain-text notes, but it's still incredibly fast and easy to look up a specific note. I also lean heavily on [Marked][marked] for previewing notes &ndash; particularly complex notes with lots of links and images.

Until recently, I've been using a Keyboard Maestro macro from [Patrick Welker][ink] to take a note from nvALT and preview it in Marked. The AppleScript in the macro takes the title of a note, converts it to a filename, and passes the filename to Marked.

That works in about 95% of cases, but I've encountered two problems:

1. OS X does strange things with file separators (the colon and the slash). Having a colon or slash in the title of a note means that it isn't picked up by this script.
2. The script assumes that all my notes have the same extension: `.md`. This is almost always the case, but sometimes notes appear with the `.txt` or `.mdown` extension. I could play whack-a-mole with file extensions, but it's easier to have the script do it for me.

I've written a Python script to replace the AppleScript, which seems to solve both of these problems. I've been using it for the last few weeks, and now I'd like to share it.

<!-- summary -->

The main part of the script is a function, `get_note_path()`, which looks up the path to the frontmost note in nvALT. Here it is:

{% highlight python linenos %}
import os

from applescript import asrun, asquote

NOTEDIR = os.path.join(os.environ['HOME'], 'Dropbox', 'Notes')

def get_note_path():
    """Returns a path to the frontmost note in nvALT."""

    # Get the title of the frontmost note
    title = asrun("""tell application "System Events" to tell process "nvALT"
        get value of text field 1 of group 1 of toolbar 1 of window 1
    end tell""").strip()

    # Escape certain characters in note names to accomodate for the OS X
    # filesystem
    title = title.replace(":", "-")
    title = title.replace("/", ":")

    # Get the filename of the note. I'm assuming that there are not multiple
    # notes with the same title but different file extensions
    for filename in os.listdir(NOTEDIR):
        name, _ = os.path.splitext(filename)
        if name == title:
            filepath = os.path.join(NOTEDIR, filename)
            return filepath
{% endhighlight %}

I'm using Dr. Drang's [`applescript` module][drang] to get the title of the note: the AppleScript is just a line taken from Patrick's script. Since `asrun()` includes a newline, I have to remove that first.

On lines 15&ndash;18, I'm doing the special character replacement. A colon in a note title become a dash in the filename, and a slash becomes a colon. As the colon and the slash are the only path separators on OS X, I think these are the only special cases. (If there are others, I haven't encountered them yet, and they're not hard to add.)

(Incidentally, this character replacement is why I wrote my new script in Python, not AppleScript. It's one line in Python. In AppleScript, it's [more like ten][repl]. That basic string manipulations in AppleScript are so hard is one of several reasons why I don't like it.)

Then on lines 20&ndash;24, I look for every file in my notes folder which matches the title of this note. Initially, I wrote `if title in ff`, but that doesn't work: the title needs to match exactly, or it's the wrong note. I'm assuming that while I may have notes with the wrong extension, I'm unlikely to have notes with identical titles and different extensions. I just get the first note that matches.

The second part of the script is much simpler, and taken almost wholesale from Patrick's original macro:

```python
asrun("""tell application "Marked"
    open %s
    activate
end tell""" % asquote(get_note_path()))
```

This is just a wrapper around the AppleScript: the `asquote()` turns the path to the note into an AppleScript-suitable string, and then tells Marked to open the file.

I have this script bound to the same ⇧⌘M shortcut as Patrick's original macro, to take advantage of muscle memory. Over the next few weeks, I'll try to post some more of my new macros which use `get_note_path()`. I have some fun ideas.

[nv]:     http://brettterpstra.com/projects/nvalt/
[marked]: http://marked2app.com/
[ink]:    http://rocketink.net/2013/01/my-nvalt-setup.html
[drang]:  http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/
[repl]:   http://foolsworkshop.com/applescript/2008/05/an-applescript-replace-text-method/