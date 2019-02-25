#!/usr/bin/env python
"""
extracturls.py
~~~~~~~~~~~~~~

This script gets a list of all the URLs in Safari Reading List, and
writes them all to a file.

Requires Python 3.
"""

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