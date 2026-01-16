---
layout: til
title: Where does AirDrop save files on macOS?
summary: Look in `/private/tmp`.
date: 2025-04-30 07:17:20 +01:00
tags:
  - macos
---
I have mixed reliability with AirDrop -- the sending machine is usually able to send all the bits, but the receiving machine doesn't always put the file somewhere I can find it, say my Downloads folder.

Every so often I see the temporary folder where AirDropped files are saved before they're copied to a more findable location -- it's `/private/tmp`.
If I've received a file using AirDrop but it's not appearing anywhere, look there.
