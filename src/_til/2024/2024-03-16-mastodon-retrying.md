---
layout: til
date: 2024-03-16 08:39:19 +0000
title: How much will Mastodon instances try to re-send messages?
tags:
  - mastodon
---
Simon Willison had some DNS issues which meant his personal Mastodon instance (which is similar to my Masto.host setup) was knocked offline for a day or so.
He was [wondering whether](https://fedi.simonwillison.net/@simon/112100279854237102) this would cause a flood of traffic when it came back online:

{% mastodon "https://fedi.simonwillison.net/@simon/112100279854237102" %}

And there were a couple of replies to his post, explaining what would happen, including a link to the relevant part of the Mastodon codebase -- if a job fails, it gets retried with an exponential delay.

{% mastodon "https://shakedown.social/@clifff/112100294144816566" %}

and

{% mastodon "https://flipboard.social/@JsonCulverhouse/112101163947801880" %}
