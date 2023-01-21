---
layout: post
date: 2020-10-12 06:52:55 +0000
title: A new README for docstore, my tool for organising scanned paperwork
summary: Although I don't expect anyone to use it directly, there might be some interesting ideas that could apply elsewhere.
link: https://github.com/alexwlchan/docstore
tags: productivity
colors:
  index_light: "#7a2342"
  index_dark:  "#e5bcc9"
---

I've written previously about how I [scan and organise my paperwork]({% post_url 2019/2019-11-27-my-scanning-setup %}).
I have a paper-feed scanner to scan my paperwork as PDFs, and then I wrote a piece of software called *docstore* to store and organise the PDFs.
docstore is built around the idea of [keyword tagging](https://en.wikipedia.org/wiki/Tag_(metadata)), because that's a system I find works well for me.

I used to run docstore on a publicly accessible web server, so I could get to it from anywhere.
(Behind a password login, of course.)
I could upload documents when I was at the office, and download them when I was away from home.

Since I'm spending most of my time at home right now, I've switched to running it locally instead.
It's just as convenient, but there's less risk of somebody stealing the files from my server.
Since my paperwork has a lot of private information (including my address, health records and bank account details), it would be a disaster if it got leaked.

{%
  picture
  filename="docstore_v2.png"
  alt="Screenshot of docstore."
  visible_width="500px"
  class="screenshot"
%}

I've recently done a complete rewrite.
Part of it was fixing mistakes in the original version, part of it was taking advantage of the fact that I'm running locally.
I used to run it on a Linux server; now I'm running it on macOS.
That means that, for example, I can [use Quick Look to create thumbnails]({% post_url 2020/2020-09-26-using-qlmanage-to-create-thumbnails-on-macos %}).

I don't expect that anybody apart from me will want to use docstore, because it's very specific to my personal context -- but the ideas might be useful elsewhere.

I've written [a new README](https://github.com/alexwlchan/docstore) that explains how it works, some of the ideas I used while building it, and the libraries and tools I used.
If you like reading my technical blog posts, you might find this README interesting too.
