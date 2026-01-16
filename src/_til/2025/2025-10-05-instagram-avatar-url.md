---
layout: til
title: Get the avatar URL for an Instagram page
summary: Use `gallery-dl --get-urls "https://www.instagram.com/{page_name}/avatar".`
date: 2025-10-05 14:53:42 +01:00
tags:
  - gallery-dl
  - instagram
---
I wanted a programmatic way to get avatar URLs for Instagram pages, and it turns out this is supported in gallery-dl.
The trick is to add `/avatar` to the end of the URL -- this doesn't resolve on `instagram.com`, but it tells gallery-dl that you want the avatar URL.

For example:

```console
$ gallery-dl --get-urls 'https://www.instagram.com/alexwlchan/avatar'
https://instagram.flhr1-1.fna.fbcdn.net/v/t51.2885-19/319337386_1…
```

The result is a long URL with a bunch of query parameters; it looks like it's signed and the URL will only last a short time.
I haven't tested how long it remains valid for.

Note that this avatar isn't the highest-resolution available -- for example, my avatar is 700&times;700 pixels in my web browser, but gallery-dl only finds an avatar that's 320&times;320 pixels.
That's fine for my project, but may be unsuitable if you're displaying the images at large size.
