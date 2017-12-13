---
date: 2016-02-09 12:49:00 +0000
layout: post
summary: It turns out that an SSH client on your iPhone can be really handy.
tags: ios
title: Saved by the Prompt
---

One of the most-used apps on my iPhone is [Prompt][prompt], an SSH client by [Panic][panic].
I use it for connecting to the Linode web server that powers this blog.
SSH on the iPhone might seem silly.
(I only ever installed it as an experiment.)
But in sticky situations, it turns out that having the Unix command line in my pocket can be really useful.

A recent example: I was staying at a hotel for work, and the booking reference had been sent in an Excel spreadsheet.
When viewed in Safari on iOS, the booking number was "helpfully" recognised as a number, and shown in the approximated form `1.41+E9`.
Since I don't have a spreadsheet app installed, I had no way to see the original number.

There are plenty of tools for converting Excel files into nicer formats, but they all need a command-line.
No problem with Prompt: I synced the spreadsheet to my Linode with Dropbox, then used [csvkit][csvkit] to turn the file into a CSV.
Voila: the booking reference.

All that took less than five minutes, and used just a handful of megabytes of data.

I never use Prompt for long sessions &ndash; I'd always grab a laptop for that.
But when I'm in a pinch, I can fall back on my trusty command-line tools.
There's a lot you can do with simple Linux tools that's much harder to do with full-sized iOS apps.
If you're comfortable in the shell, it's a great app to have handy.

[prompt]: https://www.panic.com/prompt/
[panic]: https://www.panic.com/
[csvkit]: https://github.com/onyxfish/csvkit
