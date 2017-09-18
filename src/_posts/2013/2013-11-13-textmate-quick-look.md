---
date: 2013-11-13 08:16:00 +0000
layout: post
slug: textmate-quick-look
summary: Disabling the Quick Look plugin that comes in the TextMate 2 alpha.
tags: textmate, os x
title: TextMate 2 and Quick Look
---

[Several][1] [people][2] [were][3] talking about TextMate 2 again this evening, so I decided to [download the alpha][4] and give it another spin.
I stopped using it about ten months ago, but I wouldn't mind going back.

Unfortunately, I ran into an immediate problem: it broke Quick Look.
It has its own QL generator, and it claims a lot of common file extensions, then applies its own syntax highlighting to them.
I don't use the word "broke" lightly.
If it was just cosmetic, then perhaps I could lived with it.
(I might even have grown to like it!)

TextMate has a long-lived problem of being slow at handling large files, and this carried over to the QL generator.
Normally the QL preview for a text file renders instantly, even if the file is very large.
With TextMate's QL plugin, the Finder took about 15&nbsp;seconds deciding not to preview a 395&nbsp;byte (!) file, and then crashed.
That's just not cool.

I haven't found a `defaults write` command to disable this, but there is a fairly simple fix: in the app bundle (right click on the icon, then select "Show Package Contents"), there's a folder

```
TextMate.app/Contents/Library/QuickLook/
```

which contains the offending plugin.
Deleting that folder and relaunching the Finder put everything back to rights.

I stopped using TextMate when I assumed that open sourcing it meant that development would grind to a halt.
Since then, I've been using [Sublime Text 2][subl].
It's perfectly functional, but it doesn't feel like a proper Mac app.
I was obviously wrong about TextMate, so I'm giving it a trial for a few weeks to see how it's doing.
If it doesn't do anything horrible, then I might start using it again, but as the old saying goes: once bitten, twice shy.

[subl]: http://www.sublimetext.com

[1]: http://www.marco.org/2013/11/12/textmate2-status
[2]: http://www.hiltmon.com/blog/2013/11/09/textmate-2-basics/
[3]: http://blog.macromates.com/2013/2-0-status-and-faq/
[4]: http://blog.macromates.com/2013/2-0-status-and-faq/
