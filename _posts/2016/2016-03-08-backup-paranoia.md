---
date: 2016-03-08 08:52:00 +0000
layout: post
summary: Running a backup is good protection against data loss, but it's not perfect.  I
  take extra measures to ensure I have really safe backups.
tags: backups
title: Backup paranoia
---

By now, you've probably read about the [KeRanger ransomware](http://arstechnica.co.uk/security/2016/03/first-mac-targeting-ransomware-hits-transmission-users-researchers-say/).
Ransomware is not a new idea, but this is the first time it's come to the Mac.
It if works as described, it's a nasty piece of work.
And if you read the same articles as me, you saw comments like *If you don't have backups, you deserve what you get*.[^1]

[^1]: This was mixed with the idea that BitTorrent is only used for piracy, which means your computer is fair game for malware authors.  I'm not interested in that discussion (at least not today).

It's important to [keep good backups](http://mattgemmell.com/backups/), but they're not foolproof.  In this case, I'm not sure backups would always save you.

Claud Xiao and Jin Chen, two security researchers, have [worked out what the malware does](http://researchcenter.paloaltonetworks.com/2016/03/new-os-x-ransomware-keranger-infected-transmission-bittorrent-client-installer/):

> After connecting to the C2 server and retrieving an encryption key, the executable will traverse the “/Users” and “/Volumes” directories, encrypt all files under “/Users”, and encrypt all files under “/Volumes” which have certain file extensions.

The "/Volumes" directory is where OS X mounts disks (both external and internal).  It includes "Macintosh HD" and any external drives you have mounted.  If your backup drives were mounted when the ransomware got to work, they'd be no help at all.

My backup regime has extra steps that I always thought were paranoid, but now I'm not so sure.
Here are a few of my suggestions:

*   **Only mount your backup drives when you need them.**

    If your backup drive is permanently mounted, then it's always exposed to problems on your computer.
    There's a much higher risk of accidental data corruption, malware or random OS bugs.
    If you only mount the drives when backups are running, it's much less exposed.

    I have scripts that auto-mount my drives before my nightly backups start, and auto-eject them when they finish.
    Most of the time, they're not mounted.

    This gives you extra time.
    When something goes wrong, you’ve got a chance to spot it and take action – before it propagates to the backups.

*   **Keep an offsite backup that's hard to modify.**

    It’s good to have a backup that’s completely isolated, so anything that goes wrong with your computer cannot possibly affect it.
    Keep a copy of your data on a drive that's outside the house – it's safe from your computer, and from environmental problems like theft or a fire.
    This is an *offsite backup*.

    I have two offsite backups: an external drive that I keep at the office, and online backups with [Crashplan](http://www.code42.com/crashplan/).
    The latter is particularly nice, because it stores old versions of every file.
    Even if files do get corrupted or encrypted, I can always roll back to a known good version.

*   **When you go travelling, don't just leave your computer running.**

    If you're at home when something goes wrong, you have options.
    You can triage.  Diagnose.  Work out if you're affected.
    If needs be, you can pull the plug (literally).
    That's much harder if you're away from the house, perhaps impossible.

    So ask yourself: *should I leave my computer on while I'm away?*
    If it's not doing anything useful, turn it off.
    And if you have to keep it running, does it need network access?

*   **Disconnect your backups when you're away from home.**

    If you do have to leave your computer running while you're away, you don't need up-to-date backups – very little is changing.
    Unmount and unplug your backup drives, so they're protected from any problems in your absence.

Nothing is watertight – you could do everything above, and just get unlucky.
Data loss happens to the best of us.

But what these suggestions get you is extra time when you have problems.
When you're in a rush, you can panic and make mistakes.
In a crisis, having time to breathe and think is invaluable.
