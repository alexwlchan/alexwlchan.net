---
date: 2014-06-13 07:50:00 +0000
layout: post
tags: tumblr
title: Finding untagged posts on Tumblr, redux
---

One of the most popular posts on this site is <a href="http://alexwlchan.net/2013/08/untagged-tumblr-posts/">Finding untagged posts on Tumblr</a>, but it's not exactly... friendly.
Asking people to download a script and register an API key can look sufficiently daunting that a lot of people probably don't try.

I wanted a simple turnkey solution.
My idea was that people could go to a website, type in their Tumblr URL and click a single button to get a list of all your untagged posts.
And now, that exists:

<center>**<http://finduntaggedtumblrposts.com/>**</center>

If you go to that URL, then you should get a nice list of all your untagged posts.
I hope it's useful.

If you find any bugs, or a page it doesn't seem to work for, then please [get in touch](http://alexwlchan.net/about/).

<!-- summary -->

## The legal stuff

I'm not affiliated with nor endorsed by Tumblr themselves; I just wrote this because I thought it would be useful, and my existing solution was crummy.

I don't keep a list of URLs looked up with the site, but I do use Google Analytics to track basic information about visitors.
Full details are in the [privacy policy](http://finduntaggedtumblrposts.com/privacy/).

## The technical stuff

Functionally, the site does exactly the same as the original Python script, but I'm using JavaScript instead, so that all the heavy lifting can be done locally in the user's browser.

About a year ago, I did some work experience with the <a href="http://www.maths.cam.ac.uk/about/community/cmep/">Cambridge Maths Education Project</a>, or CMEP for short.
I was working on a small web app called <a href="http://nrich.maths.org/mathmoApp/#/mathmo">Mathmo</a>, which is an interactive problem generator for A-level Maths.
Mathmo is written with the AngularJS framework, and since that was the last time I did any serious JavaScript, I used the same framework here (although this is obviously much simpler than Mathmo).

All of the source code is in [a GitHub repo](https://github.com/alexwlchan/untagged-tumblr-posts), and the site itself is hosted (like this one) with GitHub Pages.
