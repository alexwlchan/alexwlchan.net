---
date: 2015-11-15 21:50:00 +0000
layout: post
summary: A Python script for getting a list of URLs from Safari Reading List.
tags: os-x python
title: Export a list of URLs from Safari Reading List
---

I've accumulated a lot of URLs in Safari's Reading List.  Problem is, trying to navigate a long list in the Safari is quite buggy &ndash; items move around randomly, I lose my place, and I'd really like more space than afforded by a single sidebar.  Wouldn't it be nice if I could pull all those URLs out of Safari, and get them in a standalone file?

A quick poke around Google didn't turn up anything obvious, so I decided to write my own Python script for doing it.

<!-- summary -->

The first task is to find where all the bookmark data is stored.  Safari keeps its bookmark data (which includes Reading List) in a binary plist file:

```
~/Library/Safari/Bookmarks.plist
```

It's possible to turn this into an XML file [using plutil](http://apple.stackexchange.com/a/62431/14295), but the resulting XML is rather messy and hard to work with.  There has to be a better way.

The Python standard library has a [plistlib module](https://docs.python.org/3.5/library/plistlib.html?highlight=plistlib) which supports opening binary plist files.  This can open the plist and turn it into a very large dictionary.  You have to be a little careful when using this module with binary plists: if you don't open the plist file in binary mode, it chokes with a UnicodeDecodeError.

Once you have the plist as a large dict, it's fairly easy to sift through it, and find the part of the file which contains the Reading List data.  The script below grabs this block of data, then picks out the URL from each bookmark.  Finally, it writes each URL to a text file on its own line:

```python
import os
import plistlib

INPUT_FILE  = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')
OUTPUT_FILE = 'readinglist.txt'

# Load and parse the Bookmarks file
with open(INPUT_FILE, 'rb') as plist_file:
    plist = plistlib.load(plist_file)

# Look for the child node which contains the Reading List data.
# There should only be one Reading List item
children = plist['Children']
for child in children:
    if child.get('Title', None) == 'com.apple.ReadingList':
        reading_list = child

# Extract the bookmarks
bookmarks = reading_list['Children']

# For each bookmark in the bookmark list, grab the URL
urls = (bookmark['URLString'] for bookmark in bookmarks)

# Write the URLs to a file
with open(OUTPUT_FILE, 'w') as outfile:
    outfile.write('\n'.join(urls))
```

This uses the Python 3 version of the plistlib module; older versions of Python have a slightly different API.

To use it, just [download the script](/files/readinglist.py), and run it through Terminal:

```console
$ python3 /path/to/readinglist.py
```

and it will create a file of URLs, one per line, in the current directory.

[^1]: Reading List was introduced in OS X Leopard, for which the system Python was 2.5.1.  OS X didn't get 2.6 until Snow Leopard.  However, I think the pool of remaining Leopard users is pretty small.
