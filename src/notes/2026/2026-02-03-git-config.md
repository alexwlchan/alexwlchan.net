---
layout: note
title: My Git config
date: 2026-02-03 22:17:10 +00:00
summary: How I set up Git on a new computer.
topic: Git
---

Set TextMate as [my text editor](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration#_core_editor) for commit messages:

```console
$ git config --global core.editor "/usr/local/bin/mate -w"
```
