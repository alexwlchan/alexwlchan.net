---
layout: post
date: 2021-09-21 21:50:31 +0000
title: Hiding favicons in Safari 15 (kinda)
summary: How to reduce the visual intrusiveness of favicons in Safari 15.
tags: macos safari
---

Apple released Safari 15 today, a release which has had a pretty controversial beta cycle.
Apple showed off a major redesign at WWDC 2021, including a complete revamp of how tabs work.
That design was roundly criticised, and they've almost completely rolled back to the previous design.

Almost.

Unfortunately, Safari 15 doesn't allow you to disable favicons, and I find this incredibly annoying:

<img src="/images/2021/safari_15_tabs_eww.png" style="width: 670px;" alt="Four browser tabs with icons next to each of the tab titles. The icons are all different colours and just noisy.">

I don't want random splotches of colour in my tab UI, eww.

There used to be a preference to disable it, but it's been removed in Safari 15.
(Screenshot of preferences for [Safari 13](/images/2021/safari_13_preferences.png), [Safari 15](/images/2021/safari_15_preferences.png).)
This is what my tab bar used to look like:

<img src="/images/2021/safari_13_tabs_notitle.png" style="width: 670px;" alt="Four browser tabs with the same tabs as before, but now the tab titles only have text. And there's more text than before!">

If you like favicons, more power to you – but I find them unhelpful and distracting, and I want to be able to turn them off.

Until Apple provides that preference (FB9643385), I found a way to at least make them more uniform and monochrome, and so less distracting:

<img src="/images/2021/safari_15_monochrome.png" style="width: 670px;" alt="The same tabs as before, but now there's a monochrome letter in the tab titles.">

To get this effect, run these three commands in Terminal:

```
sudo chmod 000 /Users/alexwlchan/Library/Safari/Favicon\ Cache
sudo chmod 000 /Users/alexwlchan/Library/Safari/Template\ Icons/
sudo chmod 000 /Users/alexwlchan/Library/Safari/Touch\ Icons\ Cache/
```

To reverse it and go back to the standard behaviour, run these three commands:

```
sudo chmod 755 /Users/alexwlchan/Library/Safari/Favicon\ Cache
sudo chmod 755 /Users/alexwlchan/Library/Safari/Template\ Icons/
sudo chmod 755 /Users/alexwlchan/Library/Safari/Touch\ Icons\ Cache/
```

These three folders are where Safari keeps the various icons it puts in the tab bar.
By changing their permissions to `000`, they become unreadable, so Safari has to fall back to the generic letter icons.

This has the unfortunate side effect of [removing favicons from history](/images/2021/safari_monochrome_history.png), where I did find them useful.
It's just the tab bar where I don't want to see them.

I still find this less obtrusive version a downgrade, so I've installed an old version of Safari Technology Preview – I share this permissions hack in case somebody else dislikes favicons, and would prefer the monochrome versions.
