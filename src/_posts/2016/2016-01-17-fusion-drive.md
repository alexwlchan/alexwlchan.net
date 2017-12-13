---
date: 2016-01-17 13:13:00 +0000
layout: post
summary: If you send a Mac with a Fusion Drive to get repaired to the Apple Store,
  make sure it comes back in one piece.
title: A cautionary tale about Fusion Drive repairs
---

In September, my iMac became pretty sluggish.
Apps were slow to launch, the Finder was like treacle, and anything that touched the disk caused the fans to spin up.
I had a disk failure.

Since my iMac is sealed up tightly, I didn't want to try replacing the drive myself.
I took the machine to the local Apple Store.
The repair was a terrible experience[^1] – it overran by a month and with very poor communications from the Apple Store.
There's not much I could do about that.

But listening to Casey's [iMac tale of woe](http://atp.fm/episodes/152) on the latest ATP, I realised there was some useful advice I could give to other people going for a repair.

My iMac has a [Fusion Drive](https://en.wikipedia.org/wiki/Fusion_Drive) – a combination of an SSD and a spinning platter hard drive, presented as a single volume in the OS.
Only the spinning platter part had failed, so that was all that got replaced.

When I got the iMac back, I was a bit tentative: I installed and configured a few key applications, set up Dropbox, played around for a bit.
Once I was happy that the machine was in working order, I tried to copy my iTunes directory from my backup disk, and got a surprise from the Finder:

> The item iTunes Media can't be copied because there isn't enough free space.

It turns out that when Apple's Genius had replaced the spinning platter, they hadn't rebuilt the Fusion Drive.
The two devices were showing up as separate volumes in the Finder, and I was trying to copy my massive iTunes folder onto the tiny SSD.

I was, to say the least, quite annoyed.

Fixing this turned out to be fairly easy.
I was worried I'd have to muck about on the command-line, but rebooting into [Recovery Mode](https://support.apple.com/en-us/HT201314) and opening Disk Utility was all I needed.
It immediately said "This disk is damaged, would you like to repair it?".
I clicked "Yes", and it rebuilt my Fusion Drive.

*Cautionary note:* doing so also reformatted both drives, so I had to start my installation from scratch.

So if you have a computer with a Fusion Drive, and you send it to get repaired, **make sure they restore the Fusion Drive**.
Because fixing this problem requires wiping the disk, I'd check it as soon as you get the machine back.

Since the machine was repaired and I rebuilt the Fusion Drive, I've had no more problems.
I'm still annoyed at the Apple Store for doing an incomplete repair, but hopefully this can save somebody else a bit of hassle if it happens again.

[^1]: I filed a long and detailed complaint after the repair was done, and to be fair, I did get a sincere apology.  Even if it took another fortnight before I could get hold of a manager.