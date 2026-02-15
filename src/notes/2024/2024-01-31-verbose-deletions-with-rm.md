---
layout: note
date: 2024-01-31 19:53:48 +00:00
date_updated: 2025-05-18 18:52:40 +01:00
title: Add the `-v` flag to see what `rm` is deleting
topic: Shell scripting
---
When deleting large directories or anything with wildcards, it's tricky (and annoying!) to tell if anything is happening, or if the process has got stuck.

But `rm` supports a `-v` flag for "verbose", so it shows you the files as they get removed:

```console
$ rm -v *
helloworld.txt
```

This is particularly useful when deleting a directory with `-r`/`--recursive`, because it shows you the individual files that are being deleted:

```console
$ python3 -m venv .venv

$ rm -rv .venv
.venv/bin/Activate.ps1
.venv/bin/python3
.venv/bin/pip3.13
.venv/bin/python
…
```
