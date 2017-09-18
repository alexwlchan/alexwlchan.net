---
date: 2017-07-18 08:30:00 +0000
layout: post
slug: soundcloud-backups
title: Backing up content from SoundCloud
---

In the last week or so, SoundCloud have been [looking pretty fragile][layoffs].
They closed two of their offices (firing about 40% of their staff), and given they've been in financial difficulties for several years, you might wonder if SoundCloud is long for this world.

If you're a SoundCloud user, you might want to back up anything you've already uploaded.

I don't have anything on SoundCloud myself, but there's quite a lot of content from [Wellcome Collection][wc_sound].
When this news was shared in our internal Slack, I decided to pre-emptively download everything on the Collection's account – back up now, ask questions later.
(I was glad to hear that we already had local copies of all the important data.
Still, better safe than sorry.)

It sounds like the Internet Archive [are going after SoundCloud][ia], but sucking down 2.5PB of data is a tall order, even for them.
I thought I'd write up what I did for the Wellcome account, in case anybody else wants an extra copy of their files.

I started by installing [youtube-dl][ydl], a command-line tool for backing up video and audio from a whole bunch of sites -- including SoundCloud.
It's an incredibly handy program to keep around.
You can install it [in many ways][install], but I prefer to use pip:

```console
$ pip install youtube-dl
```

Then, downloading the Collection's SoundCloud account was a single command:

```console
$ youtube-dl --write-thumbnail --write-info-json "https://soundcloud.com/wellcomecollection"
```

youtube-dl is smart enough to recognise this as a user page, and downloads all the tracks uploaded by Wellcome.
Replace `wellcomecollection` with your username to get your own content.
For each track, it downloads an audio file, a thumbnail, and a blob of metadata.

For good measure, I then copied everything to an Amazon S3 bucket.

This probably won't work as well for content that's private or copyright-restricted, but if all you have is a public account, you might want to consider doing this sooner, not later.

[layoffs]: https://arstechnica.com/business/2017/07/soundcloud-cuts-nearly-half-of-its-staff-in-order-to-stay-afloat/
[wc_sound]: https://soundcloud.com/wellcomecollection
[ia]: http://archiveteam.org/index.php?title=SoundCloud
[ydl]: https://rg3.github.io/youtube-dl/
[install]: https://rg3.github.io/youtube-dl/download.html
