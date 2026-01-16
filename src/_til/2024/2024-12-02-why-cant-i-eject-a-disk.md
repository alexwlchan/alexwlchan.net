---
layout: til
title: How can I work out what program is keeping a disk open?
date: 2024-12-02 08:46:34 +00:00
tags:
  - macos
summary: |
  Use `sudo lsof` and grep for the name of the disk you're trying to eject.
---
Sometimes when I go to eject a disk on macOS, I can't and the computer won't tell me why:

{%
  picture
  filename="cant_eject_disk.png"
  width="507"
  alt="A dialog box 'The disk “Media (Saffron)” wasn't ejected because one or more programs may be using it."
  class="screenshot"
%}

I've wrecked an APFS volume by force ejecting it so I'd rather avoid that if I can, but how do I know what programs are using it?
Sometimes it tells me the name of macOS apps but other times it just knows that *something* is using the disk.

Based on a few Internet searches, I've cobbled together the following steps.

First, use `lsof` to see all open files, and grep for the name of the volume I'm trying to eject:

```console
$ sudo lsof | grep Saffron
bztransmi 60758                  root    6r      REG               1,27 4163181904              808769 /Volumes/Media (Saffron)/plex/Movies/Still Alice.mp4
mds       98474                  root    6r      DIR               1,27        992                   2 /Volumes/Media (Saffron)
mds       98474                  root   34r      DIR               1,27      14272                  21 /Volumes/Media (Saffron)/.Spotlight-V100/Store-V2/A448E67A-FA2B-45BC-B6D9-9EF563D5719E
mds       98474                  root   56r      DIR               1,27        992                   2 /Volumes/Media (Saffron)
mds       98474                  root   73w      REG               1,27         49             1270183 /Volumes/Media (Saffron)/.Spotlight-V100/Store-V2/A448E67A-FA2B-45BC-B6D9-9EF563D5719E/journals.scan/journal.6898
mds_store 98476                  root  twd       DIR               1,27      14272                  21 /Volumes/Media (Saffron)/.Spotlight-V100/Store-V2/A448E67A-FA2B-45BC-B6D9-9EF563D5719E
  … skip several hundred entries …
mds_store 98476                  root  362u      REG               1,27       4096             1058890 /Volumes/Media (Saffron)/.Spotlight-V100/Store-V2/A448E67A-FA2B-45BC-B6D9-9EF563D5719E/live.12.indexHead
```

If it's a user-visible app, I can stop it the "proper" way.
For example, `bztransmit` is part of Backblaze -- it was trying to upload a file from the disk, so I used the Backblaze menubar helper to pause the current backup.
Now Backblaze is no longer holding the disk open!

If it's `mds_store`, I just kill it by ID.
This is the Spotlight indexer and I don't know of a "good" way to interrupt it -- but I've also never seen any issues from stopping it using `kill`.
I can get the process ID from the `lsof` output.

```console
$ sudo kill -9 98476
```
