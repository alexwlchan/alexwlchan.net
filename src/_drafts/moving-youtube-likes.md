---
layout: post
title: Moving my YouTube Likes from one account to another
summary: Some experimenting with the YouTube API to merge two accounts into one.
tags: 
  - python
  - youtube
colors:
  index_light: "#ff0000"
---
I used to have two YouTube accounts, and I wanted to consolidate them into one.

* Why did I have two accounts?
  * Trans/gender stuff before I came out
  * Didn't want videos about trans stuff appearing in sidebar
  * e.g. logged in at work to stream music

* Within YouTube, three sources of data:
  * Subscriptions
  * Watch Later
  * Likes
  Subs + WL could move manually
  
  Of those, only Likes are significant – about 1500 likes in the account I was ditching, don't want to move manually, no builtin way to do this

* Time to play with the YouTube API!
  I've tried this a couple of times and bounced off, never really had a good use for it, so didn't stick with it. Now I do!

* First: authentication
  How to get API keys? How to store securely?
  Here's my function

* Okay, now let's use API
  Liked videos!
  There's a code snippet for this, gr9
  
* One more: like and unlike videos
  Good prog abstraction
  https://notebook.drmaciver.com/posts/2024-01-13-08:28.html
  not about code duplociation, but readability
  
  because look, nwo I can write
  
* Running the code in practice
  YouTube API has quotas -- 10000 quota units
  each like/unlike costs 100 units, so I can do <100 videos a day
  the quota resets at midnight PST = 8am in UK

  also ran into a few issues where videos had "ratings disabled"
  wonder if related to disabling *counts*?
  dunno
  only a handful of videos, so migrated manually
  
project is now wrapped up so I can throw code away -- but ability to interact with youtube is interested, and might pick it up again someday