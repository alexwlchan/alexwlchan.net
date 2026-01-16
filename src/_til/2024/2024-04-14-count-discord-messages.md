---
layout: til
date: 2024-04-14 23:10:28 +01:00
title: How to count how many Discord messages were sent on a given day
summary: |
  Using the `During` filter gives me a count of how many messages were being sent.
tags:
  - discord
---
On a particular chatty evening in the Mincemeat Discord (Oliviers 2024), I was idly curious how many messages were being sent.
I worked out a way to do this with Discord's search: use [the `During:` filter](https://support.discord.com/hc/en-us/articles/115000468588-Using-Search) and look at the result count:

{%
  picture
  filename="discord_during.png"
  width="333"
  class="screenshot"
  alt="Screenshot of the Discord search with a 'during' filter applied, and a result count just below it – 7,786 results. Chatty!"
%}

This can be combined with other filters if you want to see e.g. how many messages were sent in a particular channel.

One thing I noticed is when the server was moving quickly, these counts could occasionally fall behind – which I could usually see in the search results, whether the "latest" message in the search results was actually the latest message.
I assume this is because my requests were being split across a couple of different search nodes, and they weren't always able to stay perfectly consistent.
