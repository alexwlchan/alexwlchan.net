---
layout: til
date: 2024-02-21 12:33:15 +0000
title: What happens when you replace a photo?
tags:
  - flickr
---
You can [replace a photo on Flickr][replace].

When you replace a photo, you preserve the photo ID, but the secret changes.

Here's an example from one of my photos, using the flickr.photos.getInfo API:

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

[replace]: https://www.flickrhelp.com/hc/en-us/articles/4404058489108-Replace-a-photo-in-Flickr#:~:text=Click%20on%20your%20photo%20to,Choose%20your%20replacement%20image.
