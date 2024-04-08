---
layout: til
title: Live Text is aware of how hyphenation works (kinda)
date: 2023-12-26 12:26:12 +0000
tags:
  - live-text
---

Here’s a screenshot from a Kindle book (from *Silo Submerged*, by WJ Davies):

{%
  picture
  filename="the-runner-text-screenshot.png"
  width="562"
  class="screenshot"
  alt="Text where the word 'always' has been split over the third and fourth line."
%}

If I run that through Live Text in Preview or Photos on Ventura, notice how it's smart enough to compress the hyphenated "al-ways" into a single line:

> It suddenly struck him the why of cleaners past. Although most were prone to telling their casters they wouldn't clean, they **always** did. Upon seeing the perfect world that had been shielded from them their entire

But it doesn’t always work – here’s another except from the same trilogy:

{%
  picture
  filename="the-watcher-text-screenshot.png"
  width="562"
  class="screenshot"
  alt="Text where the words 'fe-male' and 'legacy' have been split across multiple lines."
%}

which is transcribed as:

> He understood the need for male and **female** relationships. After all, how else would children be born to continue humanity's **leg-acy**? But he always thought that convention

Interesting that it picked up "female" but not "legacy" -- I wonder if the number of characters on the first line is significant?
