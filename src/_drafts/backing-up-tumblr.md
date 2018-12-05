---
layout: post
title: A script for backing up Tumblr posts and likes
summary: Since Tumblr users are going on a mass deletion spree (helped by the Tumblr staff), some scripts to save content before it's too late.
tags: tumblr
link: https://github.com/alexwlchan/backup_tumblr
---

A few days ago, Tumblr announced some new content moderation policies that include the mass deletion of any posts deemed to contain "adult content".
(If you missed the news, the Verge has a [good summary](https://www.theverge.com/2018/12/3/18123752/tumblr-adult-content-porn-ban-date-explicit-changes-why-safe-mode).)

If my dashboard and Twitter feed are anything to go by, this is bad news for Tumblr.
Lots of people are getting [flagged for innocuous posts](http://the-earth-story.com/post/180769626996/flags), the timeline seems to be falling apart, and users are leaving in droves.
The new policies don't solve the site's problems (porn bots, spam, child grooming, among others), but it hurts their marginalised users.

For all its faults, Tumblr was home to communities of sex workers, queer kids, fan artists, people with disabilities -- and it gave many of them a positive, encouraging, empowering online space.
I'm sad that those are going away.

Some people are leaving the site and deleting their posts as they go (rather than waiting for Tumblr do it for them).
Totally understandable, but it leaves a hole in the Internet.
A lot of that content just isn't available anywhere else.

In theory you can export your posts with the official export tool, but I've heard mixed reports of its usefulness -- I suspect it's clogged up as lots of people try to leave.
In the meantime, I've posted [a couple of my scripts](https://github.com/alexwlchan/backup_tumblr) that I use for backing up my posts from Tumblr.
It includes posts and likes, saves the full API responses, and optionally includes the media files (photos, videos, and so on).

They're a bit scrappy -- not properly tested or documented -- but content is already being deleted by Tumblr and others, so getting it out quickly seemed more useful.
If you use Tumblr, you might want to give them a look.
