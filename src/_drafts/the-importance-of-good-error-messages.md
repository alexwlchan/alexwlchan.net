---
layout: post
title: The importance of good error messages
summary: An Excel mistake shows why learning to write good error messages is a critical skill for software developers
tags: programming
---

Last week, the UK government came under fire for suspected [poor use of Excel](https://www.engadget.com/microsoft-excel-england-covid-19-delay-114634846.html), which led to an undercounting of COVID-19 cases.
Excel spreadsheets can only handle about a million rows, and anything after that gets truncated.
I don't want to talk about the decision to use Excel; instead I want to talk about how Excel handles this particular failure mode.

I created a large CSV spreadsheet using Python, then I opened it with Excel 2016 on my work Mac.
This is the message I received:

<img src="/images/2020/excel_truncation_error_1x.png" srcset="/images/2020/excel_truncation_error_1x.png 1x, /images/2020/excel_truncation_error_2x.png 2x" alt="An Excel alert dialog that says 'File not loaded completely', with a single 'OK' button.">

This is not a good error.
What does it even mean?

I get other errors that sound like this all the time.
My word processor didn't load all the fonts.
My email client didn't load remote images.
My presentation software didn't load all the animations.
These are all fairly minor issues, so I can ignore this error from Excel as well, right?

What this error actually means is that I had too many rows or too many columns in my CSV -- it's the same error message for both -- but that's not at all clear.
I can totally imagine clicking through this without realising that I was about to incur data loss.
(And indeed, I've heard of multiple people doing just that in the last week alone.)

What I find extra egregious is that the only available action is to click "OK".
Of course somebody will click through -- what else can they do?!
A "Cancel" button would give us a tiny hint that we might want to rethink what we're doing, but Excel tells us what we're doing is completely fine.

**Good error messages explain what's gone wrong, and give clear steps for how to fix the issue.**
This does neither -- and nor do most other error messages, which is why people just learn to search for the button that makes the message go away, so they can get on with their work.

This isn't Excel-specific -- **software development as an industry is generally terrible at writing error messages and user-facing text**.
On Twitter, I saw a lot of people suggest alternative tools that the COVID tracers should be using instead of Excel.
At least 95% of those tools will have similar -- if not even more confusing -- error messages and help text.

**If you write software, you need to learn to write good error messages.**
Practice explaining things.
Talk to your users.
Find out what their mental model of your software is, and how they describe it.
Write your user-facing text in their terms, not yours.
It's hard, but it's skill you can learn -- and it pays dividends in the usability of your software.

*This post was originally [a thread on Twitter](https://twitter.com/alexwlchan/status/1313400618216755200).*
