---
layout: post
title: Avoiding the automatic redirect on Tumblr posts
tags: tumblr
summary: I see an intermittent 303 Redirect when trying to navigate to a Tumblr 'permalink'; changing the User-Agent seems to fix it.
theme:
  minipost: true
---

Recently I've noticed Tumblr being much more aggressive about redirecting me to the dashboard.

I often save permalinks to read later, but when I try to follow them I get a 303 redirect, and I'm bounced back to my dashboard.
(I think it's trying to redirect me to the Tumblr app, but I'm often in a desktop browser, and there isn't a desktop Tumblr app.)

It doesn't happen consistently, which makes it even more infuriating.

The best workaround I've found is to change my User-Agent.
If I pretend to be Googlebot when I'm browsing Tumblr [*Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)*], I skip being shown any privacy policies or being sent to my dashboard.
