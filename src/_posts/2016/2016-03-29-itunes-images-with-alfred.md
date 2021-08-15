---
layout: post
date: 2016-03-29 07:56:00 +0000
summary: Using Alfred and a Python script to retrieve artwork from the iTunes, App
  and Mac App Stores.
tags: alfred python
title: Get images from the iTunes/App/Mac App Stores with Alfred
category: Working with macOS
---

Several weeks ago, Dr. Drang posted a [Python script](http://leancrew.com/all-this/2016/03/images-from-the-itunes-app-mac-app-stores/) for getting artwork from the iTunes Store.
It uses the iTunes API, which is super handy – I’d never even known it existed. I still rip a fair amount of music from CDs, and having artwork from iTunes is nice.
(A script is a better approach than "buy one song from the album, get the artwork", which is what I used to do.)

Thing is, I do most of my web searches through [Alfred](https://www.alfredapp.com).
I don't really want to go out to the command-line for this one task.
Wouldn't it be nice if I could get iTunes artwork through Alfred?

<img src="/images/2016/itunes-alfred.png" alt="A grey search bar with the query “ipic ios drafts”, and a single result “Get iTunes artwork for ‘ios drafts’”." style="max-width: 575px;">

Hmm.

Calling a script is a fairly simple Alfred workflow.
I created a keyword input for "ipic", which requires an argument, and then that argument is passed to the "Run Script" action.
That action has a single-line Bash script: calling out to Dr. Drang's script, passing my input as a command-line argument.

<img src="/images/2016/alfred-workflow.png" alt="A workflow titled “Search the iTunes Search API”. The background is dark grey, and a light grey box “ipic” links to a second box “Run script”.">

This works fine with Dr. Drang's original script.

Unfortunately, Alfred passes the entire search as a single string.
Although the original script has flags for filtering by content type (e.g. album, film, TV show), you can't use that filtering in Alfred – the script only ever sees a single argument.

So I tweaked the script to add a special case for Alfred.
When Alfred calls the script, it passes an undocumented `--alfred` flag.
Although docopt is nominally passing the command-line flags, it doesn't know about this one.
Instead, I intercept the flags before docopt sees them, and rearrange them if I detect the script is being called by Alfred:

```python
if sys.argv[1] == '--alfred':
    media_type, search_term = sys.argv[2].split(' ', 1)
    if media_type in ('ios', 'mac', 'album', 'film', 'tv', 'book', 'narration'):
        sys.argv = [sys.argv[0], '--{0}'.format(media_type), search_term]
    else:
        sys.argv = [sys.argv[0], sys.argv[2]]
```

By the time docopt is called, the arguments look as if I called the script from the command-line.
It never knows the difference.

This change, along with long-name flags and writing to a tempfile instead of the Desktop, are in [my GitHub fork](https://github.com/alexwlchan/ipic) of Dr. Drang's original script.
