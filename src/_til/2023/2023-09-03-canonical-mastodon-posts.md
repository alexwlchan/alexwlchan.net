---
layout: til
date: 2023-09-03 22:39:29 +0100
title: Finding the original page for a post on Mastodon
summary: Following the logged-out 302 Redirect takes you to the original post.
tags:
  - mastodon
---
Let's suppose I'm browsing my Mastodon timeline.
Every post has a permalink to the copy of the post on my server.
For example:

```
https://social.alexwlchan.net/@b0rk@jvns.ca/111001878518404449
```

but the true permalink of this post is the one on the original server; in this case:

```
https://social.jvns.ca/@b0rk/111001876327556716
```

If I'm looking at the post in the Mastodon web app, I can get this URL with the "Open original page" or "Copy link to status" command.

{%
  picture
  filename="mastodon-copy-link.png"
  width="474"
  class="screenshot"
  alt="Screenshot of a Mastodon post with the menu open, showing the 'Copy link to status' command highlighted."
%}

What if I want to get that URL programatically?

At least on my server, trying to view my server-local permalink to the post when you're not logged in will redirect you to the original post.
This means we can find it by inspecting the redirect location:

```console
$ curl --head --write-out '%header{location}' 'https://social.alexwlchan.net/@b0rk@jvns.ca/111001878518404449'
https://social.jvns.ca/@b0rk/111001876327556716
```

This isn't true in general, and might depend on server config -- for example, trying this technique on `mastodon.social` redirects you to an interstitial page that asks you to confirm you really want to leave `mastodon.social`.

```console
$ curl --head --write-out '%header{location}' 'https://mastodon.social/@inthehands@hachyderm.io/112440744710114644'
https://mastodon.social/redirect/statuses/112440744710114644
```

It turns out there are some [security issues](https://shkspr.mobi/blog/2023/10/an-openish-redirect-on-mastodon/) related to redirects like this, so even on my server this technique might not last forever.

---

I was originally investigating this for my `;furl` text expansion macro that inserts a link to the URL of my frontmost browser tab.
I wanted a way to ensure Mastodon links always used the link to the original status, not my server's copy of it.
This worked as an initial fix, but if this is an issue in future I might need to look at using the Mastodon API.
