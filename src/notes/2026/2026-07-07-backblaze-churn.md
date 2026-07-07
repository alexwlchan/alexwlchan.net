---
layout: note
date: 2026-07-07 20:50:49 +01:00
title: Finding high-churn folders that bother Backblaze
summary: I looked at log files in `bzreports_lastfilestransmitted` to work out which folders were generating new content.
topic: Computers and code
hidden_topics:
  - Backblaze
---
I just got back to my personal computer after a day of work.
My Mac has been switched on all day, doing very little.
After a few minutes of idle web browsing, I noticed that `bztransmit` was using 100% of a CPU core, which I found confusing.

`bztransmit` is the background process that uploads files to Backblaze, my offsite backup provider.
When I checked the Backblaze preferences, it claimed I had 169MB of remaining files.
How?!

Nothing I'd done in the last few minutes would generate that much new content, and my Mac had been running all day; ample time to upload anything I created this morning or earlier.
(Even then, 169MB feels like a lot -- most of my work is in text, which is very light on storage.)

I wanted to see exactly what Backblaze was uploading, and this [Reddit post by Brian Wilson][reddit-brianwski] (Backblaze co-founder) was helpful:

> **How can I find which files Backblaze is currently uploading?** […]
>
> You can watch the logs in this location on your Mac: <code>/Library&ZeroWidthSpace;/Backblaze.bzpkg&ZeroWidthSpace;/bzdata&ZeroWidthSpace;/bzlogs&ZeroWidthSpace;/bzreports_lastfilestransmitted&ZeroWidthSpace;/&lt;day_of_week&gt;.log</code> If you watch lines getting appended to those files, make your editor REALLY WIDE to see them super nicely formatted, they report the exact files being transmitted in real time to the Backblaze datacenter, plus a measurement of how fast they were transmitted.

I found the folder he was describing, and the most recently edited file was called `07.log`.
(Perhaps it's day of the month, rather than day of the week?)

The log contains a lot of information about the files being uploaded, but I was really only interested in the paths.
I wanted to see which folders were causing so many uploads.
I wrote a short Python script to search for all the paths in the file, truncate them to a certain depth, and print the most commonly-uploaded folders:

```python {"names":{"1":"collections","2":"Counter","3":"os","4":"pathlib","5":"Path","6":"re","7":"sys","8":"PATH_RE","13":"log_path","16":"max_depth","26":"in_file","27":"paths","31":"m","36":"folders","39":"p","41":"truncated_paths","46":"p","48":"path","49":"count"}}
#!/usr/bin/env python3

from collections import Counter
import os
from pathlib import Path
import re
import sys


# PATH_RE is a regex that finds strings that look like paths in
# my home directory.
PATH_RE = re.compile(os.environ["HOME"] + r"/[A-Za-z0-9\.\-/_]+")


if __name__ == "__main__":
    try:
        log_path = sys.argv[1]
        max_depth = int(sys.argv[2])
    except (IndexError, ValueError):
        sys.exit(f"Usage: {__file__} LOG_PATH MAX_DEPTH")

    # Find all the paths in the Backblaze log file
    with open(log_path) as in_file:
        paths = [Path(m.group(0)) for m in PATH_RE.finditer(in_file.read())]

    # Truncate all the paths to as deep as specified by the `max_depth` argument
    folders = [p.parent for p in paths]
    truncated_paths = [Path(*p.parts[:max_depth]) for p in folders]

    # Print the paths, from most to least common
    for path, count in Counter(truncated_paths).most_common():
        print(f"{count:5d}\t{path}")
```

The script takes two arguments: the path to the log file, and the depth at which to truncate the folders.

I ran the script, which quickly showed one folder being uploaded far more than the rest:

```console {"wrap":true}
$ python3 find_backblaze.py /Library​/Backblaze.bzpkg​/bzdata​/bzlogs​/bzreports_lastfilestransmitted​/07.log 6 | head -n 5
 2292	/Users/alexwlchan/Library/Containers/com.apple.Safari
  997	/Users/alexwlchan/Library
  321	/Users/alexwlchan/Library/Preferences
  267	/Users/alexwlchan/Pictures
  116	/Users/alexwlchan/Library/Photos/Libraries
```

I don't know exactly what's in that `com.apple.Safari` container; a quick poke around shows some caches, some network data, some cookies.
It looks like a big collection of tiny files that get created as I use my web browser, and Backblaze is getting overwhelmed trying to upload them all.

I doubt I'll ever want to restore anything from that folder, so I've excluded it from Backblaze.
Almost immediately, my remaining files dropped to zero and `bztransmit` calmed down.

There are probably other high-churn folders that give Backblaze a headache, so I expect I may run this script again soon.

[reddit-brianwski]: https://www.reddit.com/r/backblaze/comments/4luspc/comment/d3r3icg/