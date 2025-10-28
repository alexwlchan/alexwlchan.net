---
layout: post
title: Why can't my iPhone play that video?
summary: The answer involves the AV1 video codec, Apple's chips, and several new web APIs I learnt along the way.
tags:
  - web development
  - video
---
I [download a lot of videos][downloads], but recently I discovered that some of those videos won't play on my iPhone.
If I try to open the videos or embed them in a webpage, I get a broken video player:

{%
  picture
  filename="broken-video.png"}
  width="400"
  class="screenshot dark_aware"
  alt="A black box with a play triangle in the middle, and a line striking it out."
%}

These same videos play fine on my Mac -- it's just my iPhone that has issues.
The answer involves the AV1 video codec, Apple's chips, and several new web APIs I learnt along the way.

[downloads]: /2025/yt-dlp-wrapper/

{% table_of_contents %}

## My iPhone is too old for the AV1 video codec

Doing some research online gave me the answer quickly: the broken videos use the [AV1 codec], which isn't supported on my iPhone.
AV1 is a modern video codec that's designed to be very efficient and royalty free, but it's only been recently supported on Apple devices.

I have an iPhone 13 mini with an A15 processor.
My iPhone doesn't have hardware decoding support for AV1 videos -- that only came with the iPhone 15 Pro and the A17 Pro.
This support was included in all subsequent chips, including the M4 Pro in my Mac Mini.

It's theoretically possible for Apple to decode AV1 in software, but they haven't.
According to Roger Pantos, who works on Apple's media streaming team, [there are no plans][mailing_list] to provide software decoding for AV1 video.
This means that if your chip doesn't have this support, you're out of luck.

I wanted to see if I could have worked this out myself.
I couldn't find any references or documentation for Apple's video codec support -- so failing that, is there some query or check I could run on my devices?

[AV1 codec]: https://en.wikipedia.org/wiki/Av1
[mailing_list]: https://mailarchive.ietf.org/arch/msg/hls-interest/yGhxnphS6jYWmHHa14BZMk2sB8o/
[hls]: https://en.wikipedia.org/wiki/HTTP_Live_Streaming

## Checking compatibility with web APIs

I've found a couple of APIs I can use that tell me my browser can play a particular video.
These APIs are used by video streaming sites to make sure they send you the correct video.
For example, YouTube can work out that my iPhone doesn't support AV1 video, so they'll stream me a video that uses a different codec.

### Getting the MIME type and bitrate for the video

The APIs I found require a [MIME type][mime_type] and bitrate for the video.

A MIME type can be something simple like `video/mp4` or `image/jpeg`, but it can also include information about the video codec.
The codec string for AV1 is quite complicated, and includes many parts.
If you want more detail, read the [AV1 codecs docs on MDN][av1_codec] or the [Codecs Parameter String section][av1_spec] of the AV1 spec.

We can get the key information about the unplayable video using `ffprobe`:

{% code lang="shell" %}
ffprobe -v error -select_streams v:0 \
    -show_entries stream=codec_name,profile,level,bits_per_raw_sample \
    -of default=noprint_wrappers=1 "input.mp4"
# codec_name=av1
# profile=Main
# level=8
# bits_per_raw_sample=N/A
{% endcode %}

The AV1 codec template is `av01.P.LLT.DD`, which we construct as follows:

*   `P` = profile number, and "Main" means `0`
*   `LL` = a two-digit level number, so `08`
*   `Tier` = the tier indicator, which can be Main or High.
    I think the "High" tier is for professional workflows, so let's assume my video is Main or `M`.
*   `DD = the two-digit bit depth, so `08`.

This gives us the MIME type for the unplayable video:

```
video/mp4; codecs=av01.0.08M.08
```

I also got the MIME type for an H.264 video which does play on my iPhone:

```
video/mp4; codecs=avc1.640028
```

By swapping out the argument to `-show_entries`, we can also use ffprobe to get the resolution, frame rate, and bit rate:

{% code lang="shell" %}
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,bit_rate,r_frame_rate \
  -of default=noprint_wrappers=1:nokey=0 "input.mp4"
# width=1920
# height=1080
# r_frame_rate=24000/1001
# bit_rate=1088190
{% endcode %}

Now we have this information, let's pass it to some browser APIs.

[mime_type]: https://developer.mozilla.org/en-US/docs/Glossary/MIME_type
[av1_codec]: https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/codecs_parameter#av1
[av1_spec]: https://aomediacodec.github.io/av1-isobmff/#codecsparam

### HTMLMediaElement: `canPlayType()`

The [`video.canPlayType()` method][canPlayType] on HTMLMediaElement takes a MIME type, and tells you whether a browser is likely able to play that media.
Note the word "likely": possible responses are "probably", "maybe" and "no".

Here's an example using the MIME type of my AV1 video:

{% code lang="javascript" names="0:video" %}
const video = document.createElement("video");
video.canPlayType("video/mp4; codecs=av01.0.08M.08");
{% endcode %}

Let's run this with few different values, and compare the results:

<style>
  table.results {
    width: 100%;
    border: var(--border-width) var(--border-style) var(--block-border-color);
    border-radius: var(--border-radius);
    background-color: var(--block-background);
    padding: var(--default-padding);
  }

  tbody:not(:last-of-type) tr:last-child > th,
  tbody:not(:last-of-type) tr:last-child > td {
    padding-bottom: 10px;
    border-bottom: 2px solid var(--block-border-color);
  }

  tbody:not(:first-child) tr:first-child th,
  tbody:not(:first-child) tr:first-child td {
    padding-top: 10px;
  }

  table.results pre {
    border:  none;
    padding: 0;
    margin: 0;
  }
</style>

<table class="results">
  <tr>
    <th>MIME type</th>
    <th>iPhone</th>
    <th>Mac</th>
  </tr>
  <tbody><tr>
    <td>
      AV1 video<br/>
      <code>video/mp4; codecs=av01.0.08M.08</code>
    </td>
    <td><code>""</code> (= “no”)</td>
    <td><code>"probably"</code></td>
  </tr></tbody>
  <tbody><tr>
    <td>
      H.264 video<br/>
      <code>video/mp4; codecs=avc1.640028</code>
    </td>
    <td><code>"probably"</code></td>
    <td><code>"probably"</code></td>
  </tr></tbody>
  <tbody><tr>
    <td>
      Generic MP4<br/>
      <code>video/mp4</code>
    </td>
    <td><code>"maybe"</code></td>
    <td><code>"maybe"</code></td>
  </tr></tbody>
  <tbody><tr>
    <td>
      Made-up format<br/>
      <code>video/mp4000</code>
    </td>
    <td><code>""</code> (= “no”)</td>
    <td><code>""</code> (= “no”)</td>
  </tr></tbody>
</table>

This confirms the issue: my iPhone can't play AV1 videos, while my Mac can.

The generic MP4 is a clue about why this API returns a "likely" result, not something more certain.
The MIME type doesn't contain enough information about whether a video will be playable.

[canPlayType]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/canPlayType

### MediaCapabilities: `decodingInfo()`

For a more nuanced answer, we can use the [`decodingInfo()` method][decodingInfo] in the `MediaCapabilities` API.
You pass detailed information about the video, including the MIME type and resolution, and it tells you whether the video can be played -- and more than that, whether the video can be played in a smooth and power-efficient way.

Here's an example of how you use it:

```javascript
await navigator.mediaCapabilities.decodingInfo({
  type: "file",
  video: {
    contentType: "video/mp4; codecs=av01.0.08M.08",
    width:     1920,
    height:    1080,
    bitrate:   1088190,
    framerate: 24
  }
});
// {powerEfficient: false,
//  smooth: false,
//  supported: false,
//  supportedConfiguration: Object}
```

Let's try this with two videos:

<table class="results">
  <tbody>
    <tr>
      <th colspan="2">AV1 video</th>
    </tr>
    <tr>
      <td>Video config</td>
      <td><pre><code>{
  contentType: "video/mp4; codecs=av01.0.08M.08",
  width:     1920,
  height:    1080,
  bitrate:   1088190,
  framerate: 24
}</code></pre></td>
    </tr>
    <tr>
      <td>iPhone</td>
      <td>not supported</td>
    </tr>
    <tr>
      <td>Mac</td>
      <td>supported, smooth, power efficient</td>
    </tr>
  </tbody>

  <tbody>
    <tr>
      <th colspan="2">H.264 video</th>
    </tr>
    <tr>
      <td>Video config</td>
      <td><pre><code>{
  contentType: "video/mp4; codecs=avc1.640028",
  width:     1440,
  height:    1080,
  bitrate:   1660976,
  framerate: 24
}</code></pre></td>
    </tr>
    <tr>
      <td>iPhone</td>
      <td>supported, smooth, power efficient</td>
    </tr>
    <tr>
      <td>Mac</td>
      <td>supported, smooth, power efficient</td>
    </tr>
  </tbody>
</table>

This re-confirms our theory that my iPhone's lack of AV1 support is the issue.

It's worth noting that this is still a heuristic, not a guarantee.
I plugged some really large numbers into this API, and my iPhone claims it could play a trillion-pixel H.264 encoded video in a smooth and power efficient way.
I know Apple's hardware is good, but it's not that good.

[decodingInfo]: https://developer.mozilla.org/en-US/docs/Web/API/MediaCapabilities/decodingInfo

## What am I going to do about this?

This is only an issue because I have a single video file, it's encoded with AV1, and I have a slightly older iPhone.
Commercial streaming services like YouTube, Vimeo and TikTok don't have this problem because they store videos with multiple codecs, and use browser APIs to determine the right version to send you.

Apple would like me to buy a new iPhone, but that's overkill for this problem.
That will happen eventually, but not today.

In the meantime, I'm going to convert any AV1 encoded videos to a codec that my iPhone can play, and change my [downloader script][downloader_script] to do the same to any future downloads.
Before I understood the problem, I was playing whack-a-mole with broken videos.
Now I know that AV1 encoding is the issue, I can find and fix all of these videos in one go.

[downloader_script]: /2025/yt-dlp-wrapper/
