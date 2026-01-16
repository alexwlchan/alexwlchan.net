---
layout: til
title: Use `rm -v` to see which files are being removed
date: 2025-05-18 18:52:40 +01:00
tags:
  - shell scripting
---
I made a typo today that revealed an interesting flag in `rm`: if you pass `-v`/`--verbose`, it prints the name of every file it's deleting.

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