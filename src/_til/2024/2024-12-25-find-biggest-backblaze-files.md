---
layout: til
title: How to find the biggest files backed up by Backblaze
date: 2024-12-25 23:28:50 +00:00
tags:
  - backblaze
summary: |
  Look at the file <code>/Library<wbr>/Backblaze.bzpkg<wbr>/bzdata<wbr>/bzfilelists<wbr>/bigfilelist.dat</code>.
---
This is something I stumbled across in [a Reddit comment](https://www.reddit.com/r/backblaze/comments/gjah54/comment/fqlkoih/) by Brian Wilson, who was a co-founder and CTO at Backblaze.
He shared some useful advice about debugging a backup:

> The list of the very largest files on your system is found here:
>
> <code>/Library/Backblaze.bzpkg/bzdata/bzfilelists/bigfilelist.dat</code>

There's one line per file, and each line has three parts:

*   A letter saying whether Backblaze will try to back it up (`t`) or will never try to back it up (`n`)
*   The size in bytes
*   The absolute path to the file

Here's an example from my desktop Mac:

```
t 2261245289 /Users/alexwlchan/repos/alexwlchan.net/.git/objects/pack/pack-512675481a8ff1e5e00b84d4bc17e0bdec66fc55.pack
```

This tells us that Backblaze intends to back up this file (`t`) and the file is 2261245289 bytes in size, or about 2.3GB.

The list of largest files doesn't seem to be sorted, so if you want to find the biggest files Backblaze will try to back up, this shell script will sort those files in increasing order of size:

```shell
cat /Library/Backblaze.bzpkg/bzdata/bzfilelists/bigfilelist.dat \
  | grep '^t' \
  | cut -b 3- \
  | sort -h
```