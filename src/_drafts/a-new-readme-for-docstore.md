---
layout: post
title: A new README for docstore, my tool for organising scanned paperwork
summary:
link: https://github.com/alexwlchan/docstore
tags: productivity
---

I've written previously about how I [scan and organise my paperwork](/2019/11/my-scanning-setup/).
I have a paper-feed scanner to scan my paperwork as PDFs, and then I wrote a piece of software called *docstore* to store and organise the PDFs.
docstore is built around the idea of [keyword tagging](https://en.wikipedia.org/wiki/Tag_(metadata)), because that's a system I find works well for me.

I used to run docstore on a publicly accessible web server, so I could get to it from anywhere.
I could upload documents when I was at the office, and download them when I was away from home.

Since I'm spending most of my time at home right now, I've switched to running it locally instead.
It's just as convenient, but there's less risk of somebody stealing the files from my server.
Since my paperwork has a lot of private information (including my address, medical data and bank account details), it would be a disaster if it got leaked.

<img src="/images/2020/docstore_v2_1x.png" srcset="/images/2020/docstore_v2_1x.png 1x, /images/2020/docstore_v2_2x.png 2x, /images/2020/docstore_v2_3x.png 3x" alt="Screenshot of docstore." style="max-width: 500px; border: 1px solid #A6A6A6">

I've recently done a complete rewrite.
Part of it was fixing mistakes in the original version, part of it was taking advantage of the fact that I'm running locally.
I used to run it on a Linux server; now I'm running it on macOS.
That means that, for example, I can [use Quick Look to create thumbnails](/2020/09/using-qlmanage-to-create-thumbnails-on-macos/).

I don't expect that anybody apart from me will want to use docstore, because it's very specific to my personal context -- but the ideas might be useful elsewhere.

I've written a new README that explains how it works, some of the ideas I used while building it, and the libraries and tools I used.
If you like reading my technical blog posts, you might find this README interesting too.
