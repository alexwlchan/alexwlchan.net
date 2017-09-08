---
date: 2016-04-16 14:32:00 +0000
layout: post
slug: hiding-the-youtube-search-bar
summary: "I\u2019ve adapted my bookmarklet for tidying up Google Maps to hide the\
  \ YouTube search bar."
tags: javascript,
title: Hiding the YouTube search bar
---

This morning, I got an email from Sam, asking if I had a way to cover up the persistent YouTube search bar:

<img src="/images/2016/youtube-search.png" style="border: 1px solid #ddd;">

Three years ago, I wrote a bookmarklet [for cleaning up the worst of the Google Maps interface](/2013/08/google-maps/), and we can adapt this to clean up YouTube as well.
Unlike that post, this is one I'm likely to use myself.
(Writing the Maps bookmarklet was a fun exercise in JavaScript, but I almost always use Google Maps on my phone, so I was never as annoyed by the clutter on the desktop version.)

If we do "Inspect Element" on a YouTube page, we can find the element that contains this search box: `<div id="yt-masthead-container">`.
So we want to toggle the visibility of this element.
Since it's only one item, we can write a much smaller JavaScript snippet for toggling the visibility:

```javascript
var search_bar = document.getElementById("yt-masthead-container");

// Check if it's already hidden
var hidden = (window.getComputedStyle(search_bar)).getPropertyValue("display");

// Set the visibility based on the opposite of the current state
void(search_bar.style.display = (hidden == "none" ? "" : "none"));
```

To use this code, drag this link to your bookmarks bar:
<p><center><h1><a href="javascript:var%20search_bar%20=%20document.getElementById(%22yt-masthead-container%22);var%20hidden%20=%20(window.getComputedStyle(search_bar)).getPropertyValue(%22display%22);search_bar.style.display%20=%20(hidden%20==%20%22none%22%20?%20%22%22%20:%20%22none%22);console.log(%22%22);">Toggle the YouTube search bar</a></h1></center></p>
Simply click it once to make the bar disappear, and click it again to bring it all back.

Something that wasn't in my original Google Maps bookmarklet is that `void()` call.
It turns out that if a bookmarklet returns a value, it's [supposed to replace the current page with that value](http://web.archive.org/web/20080210094153/http://www.subsimple.com/bookmarklets/rules.asp).
Which strikes me as bizarre, but that's what Chrome does, so it broke the page.
(Safari doesn't – not sure if that's a bug or a feature.)
The void function prevents that from happening.

This isn't perfect – content below the bar doesn't reflow to take up the available space – but the bar no longer hangs over content as you scroll.
I think I'll find this useful when I'm pressed for space on small screens.
It's a bit more screen real-estate I can reclaim.
Thanks for the idea, Sam!
