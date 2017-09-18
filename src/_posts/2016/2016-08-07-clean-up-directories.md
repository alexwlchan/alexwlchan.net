---
date: 2016-08-07 22:46:00 +0000
layout: post
minipost: true
slug: clean-up-directories
summary: A pair of Python scripts I've been using to clean up my mess of directories.
tags: python
title: 'Python snippets: Cleaning up empty/nearly empty directories'
---

Last month, I wrote about [some tools](/2016/07/clearing-disk-space-on-os-x/) I'd been using to clear disk space on my Mac.
I've been continuing to clean up my mess of files and folders as I try to simplify my hard drive, and there are two new scripts I've been using to help me.
Neither is particularly complicated, but I thought they were worth writing up properly.

Depending on how messy your disk is, these may or may not be useful to you &ndash; but they've saved a lot of time for me.

Of course, you should always be *very* careful of code that deletes or rearranges files on your behalf, and make sure you have good backups before you start.

<!-- summary -->

## Deleting (nearly) empty directories

As I rearrange, delete or de-duplicate old files, I can often end up with empty directories.
When they're not holding anything, they only clutter up my disk.
I'd like to get rid of them, but they're often nested quite heavily &ndash; I'd like to delete them automatically where possible.

In my last post, I mentioned the Unix [`find` utility](http://linux.die.net/man/1/find).
It's possible to use `find` to delete empty directories like so:

```console
$ find <path_to_dir> -type d -empty -delete
```

But this only works if the directory is truly empty &ndash; no files or subdirectories.

Unfortunately, a directory can appear to be empty in the Finder, but still contain some hidden items.
Any file whose name starts with a dot is treated as a hidden file: this includes the infamous `.DS_Store` file, old `.git` directories, and other developer cruft.
If any of those are present, this command won't touch the parent directory.

I don't care about these hidden files: if the visible contents of the directory are gone, there's nothing I care to salvage from those hidden files.

So when I'm clearing folders, I really want to delete anything that's truly empty, or which only contains hidden files.
For that, I use the following Python script:

```python
import os
import shutil

while True:
    to_delete = []
    for root, dirs, _ in os.walk('.'):
        for d in dirs:
            full_path = os.path.join(root, d)
            if all(s.startswith('.') for s in os.listdir(full_path)):
                to_delete.append(full_path)

    if to_delete:
        for p in to_delete:
            print(p)
            shutil.rmtree(p)
    else:
        break
```

When run in a directory, it uses `os.walk` to get every directory below the current path.
For each directory, it uses `os.listdir` to get the contents of the directory, and the generator in `all()` is what determines whether the directory should be deleted.
It checks that every filename in the directory starts with a `.` &ndash; unless the directory is empty, in which case `os.listdir` returns an empty list, and then the condition is trivially true.

It runs in a loop until it doesn't find anything else to delete.
That's because I often had parent directories whose only visible contents were other empty directories &ndash; and once the script ran, those parents became eligible for deletion.
Letting the script run repeatedly saves me invoking it multiple times.

## Flattening a set of nested directories

Among my many crufty old folders, I've got directories that have many layers of nesting.
A typical example is old Photos.app libraries, which look something like this:

```
Photos Library.photoslibrary/
  Masters/
    2012/
      03/
        20/
          20120320-221722/
            IMG_0020.PNG
```

And that's for one file: there are hundreds of similar paths for my other photos.
Yuck!

When I find a directory like this with lots of deep nesting, I really want to pull up the individual files, and discard the structure &ndash; it's usually not useful.
It's much easier to look through all the files when they're all together, not scattered across dozens of individual directories.

So once again, to Python:

```python
import os
import shutil

for root, _, files in os.walk('.'):
    for f in files:
        if os.path.exists(f):
            continue
        else:
            shutil.move(os.path.join(root, f), f)
```

Like the last script, I'm using `os.walk`, but this time I'm interested in the individual files.
Run inside a directory, it grabs every file in a subdirectory, and hoists it into the current directory.

If a tree has multiple files with the same name, I only move the first: in practice, naming conflicts were rare enough that I could just deal with them by hand.

Once I've run this, I usually run the first script as well: this creates a lot of empty directories I no longer care about.
Voila: a nested structure is reduced to a single directory of files, which can be processed or deleted with ease.
