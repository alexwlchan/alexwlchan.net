---
layout: til
date: 2024-01-31 19:53:48 +00:00
title: Add the `-v` flag to see what `rm` is deleting
tags:
  - shell scripting
---
When deleting large directories or anything with wildcards, it's tricky (and annoying!) to tell if anything is happening, or if the process has got stuck.

But `rm` supports a `-v` flag for "verbose", so it shows you the files as they get removed:

```console
$ rm -v *
helloworld.txt
```
