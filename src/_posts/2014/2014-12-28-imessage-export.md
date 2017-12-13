---
date: 2014-12-28 13:00:00 +0000
layout: post
link: https://github.com/alexwlchan/imessage-archive
tags: os-x python
title: A script for exporting from iMessage
---

I have a bit of a love-hate relationship with iMessage. It's the main way I talk to my long-distance girlfriend (along with Skype and FaceTime), but it's also pretty buggy. Messages arrive multiple times, out-of-order, or not at all. But it's convenient, so I keep using it.

The iOS and OS X Messages app both use SQL databases to store their data (`sms.db` and `chat.db`, respectively). I sometimes worry about losing the messages in an iOS update, or database corruption, so I wanted to get my messages out of SQL and into a plaintext format. I've started writing a script that takes the SQL files, and exports each thread as a JSON file.

The script, and all my notes, are in a GitHub repo. This includes the database schema used by Messages, and some references/useful pointers on edge cases I've run into. Still a work-in-progress, but hopefully useful to somebody.
