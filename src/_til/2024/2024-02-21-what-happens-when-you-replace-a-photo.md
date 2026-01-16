---
layout: til
date: 2024-02-21 12:33:15 +00:00
date_updated: 2024-06-25 23:32:55 +01:00
title: What happens when you replace a photo on Flickr?
tags:
  - flickr
---
You can [replace a photo on Flickr][replace].

When you replace a photo, you preserve the photo ID, but the secret changes.

Here's an example from [one of my photos](https://www.flickr.com/photos/alexwlchan/53513831787/), using the flickr.photos.getInfo API:

```diff
 <photo
   id="53513831787"
-  secret="49d244ae7e"
+  secret="da94cf8d63"
   server="65535"
   farm="66"
   dateuploaded="1707315985"
   isfavorite="0"
   license="0"
   safety_level="0"
   rotation="0"
-  originalsecret="9a2c4750ea"
+  originalsecret="1152023310"
   originalformat="png"
   views="2"
   media="photo"
 >
```

Note that this also bumps the `lastupdate` attribute in the `<dates>` element, e.g.:

```diff
 <dates
   posted="1707315985"
   taken="2024-02-07 06:26:16"
   takengranularity="0"
   takenunknown="1"
-  lastupdate="1708517912"  // 2024-02-21T12:18:32
+  lastupdate="1708518493"  // 2024-02-21T12:28:13
 />
```

That attribute is bumped for any change to the photo, not just replacement.

I don't know if there's a reliable way to detect replaced photos in the API.
I can't find any way to detect it in the UI (not even the `lastupdate` date).

When I first tested this, I made all the replacements within a few minutes of each other.
I went back and replaced this photo for a fourth time, several months later -- the "date posted" value remains the same as ever.

Open questions:

* When you replace a photo, how long do the existing JPEGs hang around?

[replace]: https://www.flickrhelp.com/hc/en-us/articles/4404058489108-Replace-a-photo-in-Flickr#:~:text=Click%20on%20your%20photo%20to,Choose%20your%20replacement%20image.
