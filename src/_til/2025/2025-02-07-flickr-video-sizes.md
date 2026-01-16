---
layout: til
title: What does Flickr return in the `flickr.photo.getSizes` API for videos?
date: 2025-02-07 11:54:45 +00:00
summary: |
  The video's owner will get the URL to the original video file as "Video Original", otherwise you should look for the largest video size.
tags:
  - flickr
---
Flickr's help page about [downloading content][help] mentions some limitations on downloading video:

> When downloading a video that another member has uploaded, the largest file size will be 1080p 30fps. Only the video owner will be able to download the original file size.

I'm writing some code to download videos from Flickr, so I wanted to see how this looks in practice.

Here's the XML response when you call the `getSizes` API as an **anonymous user** -- that is, just using an API key.
Notice you get an `Original` size which is a high-resolution image, and some video files, but not the original:

```
<?xml version="1.0" encoding="utf-8"?>
<rsp stat="ok">
<sizes canblog="0" canprint="0" candownload="1">
  <size label="Square" width="75" height="75" source="https://live.staticflickr.com/1234/1234567890_61a9486355_s.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/sq/" media="photo"/>
  <size label="Large Square" width="150" height="150" source="https://live.staticflickr.com/1234/1234567890_61a9486355_q.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/q/" media="photo"/>
  <size label="Thumbnail" width="100" height="56" source="https://live.staticflickr.com/1234/1234567890_61a9486355_t.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/t/" media="photo"/>
  <size label="Small" width="240" height="135" source="https://live.staticflickr.com/1234/1234567890_61a9486355_m.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/s/" media="photo"/>
  <size label="Small 320" width="320" height="180" source="https://live.staticflickr.com/1234/1234567890_61a9486355_n.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/n/" media="photo"/>
  <size label="Small 400" width="400" height="225" source="https://live.staticflickr.com/1234/1234567890_61a9486355_w.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/w/" media="photo"/>
  <size label="Medium" width="500" height="281" source="https://live.staticflickr.com/1234/1234567890_61a9486355.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/m/" media="photo"/>
  <size label="Medium 640" width="640" height="360" source="https://live.staticflickr.com/1234/1234567890_61a9486355_z.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/z/" media="photo"/>
  <size label="Medium 800" width="800" height="450" source="https://live.staticflickr.com/1234/1234567890_61a9486355_c.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/c/" media="photo"/>
  <size label="Large" width="1024" height="576" source="https://live.staticflickr.com/1234/1234567890_61a9486355_b.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/l/" media="photo"/>
  <size label="Original" width="1280" height="720" source="https://live.staticflickr.com/1234/1234567890_71616f79eb_o.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/o/" media="photo"/>
  <size label="Video Player" width="640" height="360" source="https://www.flickr.com/apps/video/stewart.swf?v=1234567890&amp;photo_id=1234567890&amp;photo_secret=61a9486355" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
  <size label="720p" width="1280" height="720" source="https://www.flickr.com/photos/example/1234567890/play/720p/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
  <size label="appletv" width="" height="" source="https://www.flickr.com/photos/example/1234567890/play/appletv/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
  <size label="700" width="" height="" source="https://www.flickr.com/photos/example/1234567890/play/700/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
  <size label="360p" width="640" height="360" source="https://www.flickr.com/photos/example/1234567890/play/360p/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
  <size label="iphone_wifi" width="" height="" source="https://www.flickr.com/photos/example/1234567890/play/iphone_wifi/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
  <size label="288p" width="512" height="288" source="https://www.flickr.com/photos/example/1234567890/play/288p/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video"/>
</sizes>
</rsp>
```

And here's the same video, but this time calling the API with OAuth authentication as the video owner.
Notice that there's a new `Video Original` size:

<pre><code>&lt;?xml version="1.0" encoding="utf-8" ?&gt;
&lt;rsp stat="ok"&gt;
&lt;sizes canblog="1" canprint="0" candownload="1"&gt;
  &lt;size label="Square" width="75" height="75" source="https://live.staticflickr.com/1234/1234567890_61a9486355_s.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/sq/" media="photo" /&gt;
  &lt;size label="Large Square" width="150" height="150" source="https://live.staticflickr.com/1234/1234567890_61a9486355_q.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/q/" media="photo" /&gt;
  &lt;size label="Thumbnail" width="100" height="56" source="https://live.staticflickr.com/1234/1234567890_61a9486355_t.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/t/" media="photo" /&gt;
  &lt;size label="Small" width="240" height="135" source="https://live.staticflickr.com/1234/1234567890_61a9486355_m.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/s/" media="photo" /&gt;
  &lt;size label="Small 320" width="320" height="180" source="https://live.staticflickr.com/1234/1234567890_61a9486355_n.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/n/" media="photo" /&gt;
  &lt;size label="Small 400" width="400" height="225" source="https://live.staticflickr.com/1234/1234567890_61a9486355_w.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/w/" media="photo" /&gt;
  &lt;size label="Medium" width="500" height="281" source="https://live.staticflickr.com/1234/1234567890_61a9486355.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/m/" media="photo" /&gt;
  &lt;size label="Medium 640" width="640" height="360" source="https://live.staticflickr.com/1234/1234567890_61a9486355_z.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/z/" media="photo" /&gt;
  &lt;size label="Medium 800" width="800" height="450" source="https://live.staticflickr.com/1234/1234567890_61a9486355_c.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/c/" media="photo" /&gt;
  &lt;size label="Large" width="1024" height="576" source="https://live.staticflickr.com/1234/1234567890_61a9486355_b.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/l/" media="photo" /&gt;
  &lt;size label="Original" width="1280" height="720" source="https://live.staticflickr.com/1234/1234567890_71616f79eb_o.jpg" url="https://www.flickr.com/photos/example/1234567890/sizes/o/" media="photo" /&gt;
  &lt;size label="Video Player" width="640" height="360" source="https://www.flickr.com/apps/video/stewart.swf?v=1234567890&amp;photo_id=1234567890&amp;photo_secret=61a9486355" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
  <strong>&lt;size label="Video Original" width="1280" height="720" source="https://www.flickr.com/photos/example/1234567890/play/orig/71616f79eb/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;</strong>
  &lt;size label="720p" width="1280" height="720" source="https://www.flickr.com/photos/example/1234567890/play/720p/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
  &lt;size label="appletv" width="" height="" source="https://www.flickr.com/photos/example/1234567890/play/appletv/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
  &lt;size label="700" width="" height="" source="https://www.flickr.com/photos/example/1234567890/play/700/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
  &lt;size label="360p" width="640" height="360" source="https://www.flickr.com/photos/example/1234567890/play/360p/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
  &lt;size label="iphone_wifi" width="" height="" source="https://www.flickr.com/photos/example/1234567890/play/iphone_wifi/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
  &lt;size label="288p" width="512" height="288" source="https://www.flickr.com/photos/example/1234567890/play/288p/61a9486355/" url="https://www.flickr.com/photos/example/1234567890/" media="video" /&gt;
&lt;/sizes&gt;
&lt;/rsp&gt;</code></pre>

[help]: https://www.flickrhelp.com/hc/en-us/articles/4404079675156-Downloading-content-from-Flickr
