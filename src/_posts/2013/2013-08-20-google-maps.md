---
layout: post
date: 2013-08-20 10:47:00 +0000
summary: A bookmarklet to hide some of the UI chrome in the new design of Google Maps.
tags: javascript
title: Cleaning up Google Maps
category: Programming and code
---

Earlier this morning, Fraser Speirs was bemoaning the design of the new Google&nbsp;Maps:

{% tweet https://twitter.com/fraserspeirs/status/369736232546631680 %}

I decided to take him at his word, and spent an hour or so finding a way to de-clutter the interface. I've written a short bookmarklet which toggles the offending elements (the search box, and the other map overlays).

Drag this bookmark to your bookmarks bar:
<p><center><h1><a href="javascript:var%20ids%20=%20[%22omnibox%22,%20%22cards%22,%20%22welcome%22];var%20classes%20=%20[%22widget-viewcard%22,%20%22widget-zoom%22,%20%22watermark%22];var%20hidden%20=%20(window.getComputedStyle(document.getElementById(ids[0]))).getPropertyValue(%22display%22);if%20(hidden%20!==%20%22none%22)%20{var%20disp%20=%20%22none%22;}%20else%20{var%20disp%20=%20%22%22;}for%20(var%20i%20=%200;%20i%20<%20ids.length;%20i++)%20{document.getElementById(ids[i]).style.display%20=%20disp;}for%20(var%20i%20=%200;%20i%20<%20classes.length;%20i++)%20{var%20div%20=%20document.getElementsByClassName(classes[i]);for%20(var%20j%20=%200;%20j%20<%20div.length;%20j++)%20{div[j].style.display%20=%20disp;}}">Toggle Google Maps</a></h1></center></p>
Simply click it once to make everything disappear, and click it again to bring it all back.

I've tested it on the latest versions of Safari and Chrome on OS X. It should work in any modern browser, but I don't guarantee that it will work for you.

<!-- summary -->

## How it works

Since Google Maps is a web app, adding a `display: none` attribute to the offending elements is enough to make them vanish, and then we just need a list of classes and ids for the corresponding elements. Here it is:

* `omnibox` (id) is the search box that appears in the top left-hand corner. If you just want to target the directions box below it, you can use `cards` (class).
* `welcome` (id) is the “Help & Feedback” button in the top right-hand corner.
* `widget-viewcard` (class) is everything along the bottom of the map, such as the minimap preview, and the list of highlights.
* `widget-zoom` (class) is the +/- buttons in the bottom right-hand corner. Many people use a scroll wheel or trackpad to zoom in and out, so these aren't really necessary.
* `watermark` (class) is the Google watermark at the bottom of the map.

So the following CSS is all we need:

```css
#omnibox #welcome .widget-viewcard .widget-zoom .watermark {
	display: none;
}
```

However, that might not be exactly what we want. The search box is a useful feature; we just don't want it all the time. What we really want is a toggle: we can use the search box when we need to, and hide it once we're done. The following JavaScript is sufficient:

```javascript
var ids = ["omnibox", "cards", "welcome"];
var classes = ["widget-viewcard", "widget-zoom", "watermark"];
var hidden = (window.getComputedStyle(document.getElementById(ids[0]))).getPropertyValue("display");

if (hidden !== "none") {
  var disp = "none";
} else {
  var disp = "";
}

for (var i = 0; i < ids.length; i++) {
  document.getElementById(ids[i]).style.display = disp;
}

for (var i = 0; i < classes.length; i++) {
  var div = document.getElementsByClassName(classes[i]);
  for (var j = 0; j < div.length; j++) {
    div[j].style.display = disp;
  }
}
```

We can then bind this to a bookmarklet, and make that our toggle. (John Gruber's [JavaScript bookmarklet builder](http://daringfireball.net/2007/03/javascript_bookmarklet_builder) made this very easy.)

It's a fairly simple script. The list of elements to toggle is specified in lines 2 and&nbsp;3, and line 4 checks if the first element in the `ids` list is already hidden. This is used to determine whether to hide or unhide the elements. Then we loop through all of the elements with matching ids or classes, and set the appropriate `display` attribute.

Of course, there's nothing about any of this which is unique to Google Maps. You could use exactly the same bookmarklet to toggle elements on any website, if you gave it the appropriate list of elements. (Comments, for example.)

In an ideal world, I'd wake up tomorrow to find that Google had made this obsolete by adding their own toggle to Maps, but this should act as a stopgap until they do. If nothing else, it was a fun way to spend an hour.
