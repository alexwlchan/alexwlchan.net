---
date: 2013-03-30 19:57:00 +0000
layout: post
slug: timezone-bug
summary: A strange bug with OS X's timezone handling
tags: dates, os x
title: Strange clock bug in OS X
---

Tomorrow's switch to British Summer Time seems to have uncovered quite an unusual bug in my mum's MacBook Pro. I haven't been able to reproduce it, but it was so strange that I thought it worth briefly documenting here (in addition to filing a bug report, of course). I haven't managed to find anybody else who's had this problem, although I'm really not sure what to type into Google for this.

For reasons that remain unknown, the clock in the menu bar got stuck whenever the machine was put to sleep. Minutes would continue to increment once you woke the laptop up, but anything that had elapsed in the sleep period seemed to get lost.

My mum had put the laptop away at around half past five, and when she reopened it at ten to eight, the clock in the menu bar read 17:30. As she used the laptop, this steadily ticked away, minute-by-minute, but remained stuck at a time nearly three hours previously.

She called me downstairs to take a look at it (since it's an utterly bizarre behaviour). A quick trip to the Date&nbsp;&&nbsp;Time pane of System&nbsp;Preferences seemed to fix the problem, just by opening the pane. As I opened it, the menu bar clock snapped back to the correct time.

Presumably when you open that part of System Preferences, OS X looks up what the current timezone setting is, and in doing so, it reset whatever had got stuck in the menu bar clock. Unfortunately I have no idea where the blockage actually was.

I'm probably never going to find out what caused this bug. It may be a complete coincidence that this occurred just before the switch to BST, or there might be an obvious connection.

It's hard to extrapolate the cause of a bug from a single data point, but it feeds into my general perception that working with dates is incredibly hard. Implementing them in code, accounting for clock changes, leap years and other oddities of the calendar, even more so. As I've said before, I find this really quite fascinating, and I hope to learn more about this in the future.
