---
layout: til
title: WordPress URLs that get hammered by spammers
date: 2024-01-12 10:31:11 +00:00
tags:
  - wordpress
---
At the Flickr Foundation, we run our WordPress site behind a reverse proxy.
This causes the underlying WordPress instance to see all traffic as coming from the proxy server, including spam.

When the site has received too much spam, you get an error when you try to log into WordPress:

> You have exceeded the login limit. Please wait a few minutes and try again.

This is some sort of spam protection on the underlying WordPress instance, but it's quite annoying for legitimate users!

I added protection to a couple of URLs to stem the flow of spam requests going to the underlying instance:

*   `/wp-login.php` – the WordPress login page.
*   `/xml-rpc.php` – this endpoint is used by the WordPress mobile apps, apparently

After dropping spam requests for these URLs at the proxy server rather than forwarding it to the WordPress instance, we haven't seen the "exceeded the login limit" error again.
I think this means we're no longer tripping the spam protection.
