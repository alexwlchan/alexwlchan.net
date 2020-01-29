---
layout: post
date: 2020-01-29 09:44:49 +0000
title: Excluding lots of folders in Backblaze
summary: Backblaze lets you say “back up everything except these folders”. How do you tell it you have lots of folders you want it to ignore?
category: Working with macOS
---

One of the services I rely on is [Backblaze].
It's an online backup tool that lets me save a copy of my files to the cloud, and gives me an extra level of backup protection.

[Backblaze]: https://www.backblaze.com/

Backblaze isn't my only backup tool -- I also have several local disk clones, a disk in the office, and a lot of my files are in other cloud services -- but it's a last resort if all else fails.
If my house burnt down and my computer and local backups were all destroyed, I could still recover my files from Backblaze.

When you use Backblaze, you can choose which files it saves -- your entire disk, only selected folders, everything except selected folders, and so on.
I like the last option, where Backblaze saves everything, except folders/files I tell it to ignore.
This means the default is safety: unless I explicitly mark a file as unimportant, it's going to be saved to Backblaze.

My computer has folders that I don't need to back up or restore from the cloud: things like build artefacts, caches, code dependencies, my local Docker images, and so on.
They're large and change regularly, but I could recreate them from scratch if necessary.
Because I don't have much upload bandwidth at home, I like to exclude those from Backblaze -- I'd rather it spent time uploading files I *do* care about.

The Backblaze settings allow you to [choose the folders you want to exclude](https://help.backblaze.com/hc/en-us/articles/217664948-How-do-I-exclude-folders-file-types-or-file-sizes-), using a point-and-click interface:

<img src="/images/2020/backblaze_settings.png" alt="A settings panel. There's a tab bar at the top, with the item “exclusions” highlighted in pink. Within the panel, there's a list of folders titled “These folders will not be backed up”">

But I have a lot of these folders, and I don't really want to click through this panel dozens of times.

You can write [more sophisticated rules](https://help.backblaze.com/hc/en-us/articles/220973007-Advanced-Topic-Setting-Custom-Exclusions-via-XML) that do pattern matching and the like, but I prefer this simple list of folders.
I don't want to worry about writing an overly broad rule that accidentally excludes something important.
So how can I populate this list quickly?

I did some spelunking, and I found the `bzinfo.xml` file where this list is stored.
There's an XML block with an item for every folder I've excluded, which looks something like this:

```xml
<do_backup>
    <bzdirfilter dir="/" whichfiles="all"/>
    <bzdirfilter dir="/.mobilebackups/" whichfiles="none"/>
    <bzdirfilter dir="/applications/" whichfiles="none"/>
    ...
</do_backup>
```

By adding lines to this file, we can add new exclusions more quickly than using the GUI.
You also have to restart the Backblaze processes, so the changes are picked up.

I wrote a Python script to automate this for me -- I pass the script a list of paths, and it edits the XML and restarts the relevant processes.
It also saves a backup copy of the rules, so if anything goes wrong, I can always roll back to an old version.
If you'd like to use the script, you can find it below:

{% details %}
<summary>add_backblaze_exclusions.py</summary>

```python
#!/usr/bin/env python3
"""
Script for adding one-off folder exclusions to BackBlaze.

Call it by passing a list of paths you want to exclude as command-line
arguments, e.g.

    python add_backblaze_exclusions.py /path/to/exclude/1 /path/to/exclude/2

It saves a copy of your bzinfo.xml backup rules before editing.

macOS only.

"""

import datetime
import os
import pathlib
import shutil
import subprocess
import sys
from typing import Iterator, List

from lxml import etree


def get_dirs_to_exclude(argv: List[str]) -> Iterator[pathlib.Path]:
    """
    Given a list of command-line arguments (e.g. from sys.argv), get
    a list of directory paths to exclude.
    """
    for dirname in argv:
        path = pathlib.Path(dirname).resolve()

        if not os.path.isdir(path):
            print(f"Skipping {dirname}; no such directory", file=sys.stderr)
            continue

        yield path


def add_exclusion(*, root: etree.ElementTree, exclude_dir: pathlib.Path):
    """
    Given the parsed XML from bzinfo.xml and the path to a directory,
    add that directory to the list of exclusions.
    """
    # The filter inside this XML file is something of the form
    #
    #     <do_backup ...>
    #       <bzdirfilter dir="/path/to/exclude/" whichfiles="none" />
    #       ...
    #     </do_backup>
    #
    # so we want to find this do_backup tag, then add the bzdirfilter elements.
    do_backup_elements = root.xpath(".//do_backup")

    if len(do_backup_elements) != 1:
        raise ValueError("Did not find exactly one <do_backup> element in bzinfo.xml")

    do_backup = do_backup_elements[0]

    # If this directory has already been excluded, we can skip adding it again.
    # Note: directory names are case insensitive.
    already_excluded = {
        dirname.lower()
        for dirname in do_backup.xpath('./bzdirfilter[@whichfiles="none"]/@dir')
    }

    if str(exclude_dir).lower() in already_excluded:
        print(f"{exclude_dir} is already excluded in bzinfo.xml")
        return

    # TODO: Look for the case where a parent is excluded, e.g. if /a/b/c is
    # already excluded, we can safely skip adding an exclusion for /a/b/c/d/e.

    # Create the new exclusion tag.
    dirfilter = etree.SubElement(do_backup, "bzdirfilter")
    dirfilter.set("dir", str(exclude_dir).lower())
    dirfilter.set("whichfiles", "none")

    # Sort the list of exclusions.  This isn't strictly necessary, but makes
    # the file a little easier to read and work with.
    do_backup[:] = sorted(
        do_backup.xpath("./bzdirfilter"), key=lambda f: f.attrib["dir"]
    )


def save_backup_copy(bzinfo_path: str) -> str:
    """
    Save a backup copy of the bzinfo.xml file before making edits.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%m-%S")
    backup_path = f"bzinfo.{today}.xml"

    shutil.copyfile(bzinfo_path, backup_path)
    return backup_path


def restart_backblaze():
    """
    Restart all the BackBlaze processes.
    """
    for cmd in [
        ["sudo", "killall", "bzfilelist"],
        ["sudo", "killall", "bzserv"],
        ["sudo", "killall", "bztransmit"],
        ["killall", "bzbmenu"],
        # The exclusion list doesn't get reloaded in System Preferences
        # when the process restarts; we have to quit and reopen SysPrefs.
        ["killall", "System Preferences"],
        ["open", "-a", "BackBlaze.app"],
    ]:
        subprocess.call(cmd, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    dirs_to_exclude = get_dirs_to_exclude(sys.argv[1:])

    bzinfo_path = "/Volumes/Macintosh HD/Library/Backblaze.bzpkg/bzdata/bzinfo.xml"

    backup_path = save_backup_copy(bzinfo_path)
    print(f"*** Saved backup copy of bzinfo.xml to {backup_path}")

    root = etree.parse(bzinfo_path)

    for exclude_dir in dirs_to_exclude:
        add_exclusion(root=root, exclude_dir=exclude_dir)

    print("*** Writing new exclusions to bzinfo.xml")
    with open(bzinfo_path, "wb") as outfile:
        root.write(outfile, pretty_print=True, xml_declaration=True)

    print("*** Restarting BackBlaze")
    restart_backblaze()
```

{% enddetails %}

Since this is messing with your backup config, you should double-check when it's done -- does the list of folder exclusions in the settings look correct?

I've used this script to exclude lots of folders, and now I'm backing up ~300GB less than I was before.
That's a not-insignificant saving, and it means the files I really care about can be backed up just a bit faster.
