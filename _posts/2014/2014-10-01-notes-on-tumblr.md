---
date: 2014-10-01 18:34:00 +0000
layout: post
tags: tumblr
title: Notes on Tumblr
---

The most popular thing I've ever written is my site for [finding untagged Tumblr posts][futp]. I have a few small changes, a new way to filter posts, and some other thoughts on using Tumblr.

<!-- summary -->

I'll start with the small stuff:

* I tweaked the CSS to look slightly better on mobile browsers. Specifically, the input for typing in your hostname no longer flows off the edge of the screen.
* I discovered the `autofocus` attribute, and thought I could put it to good use.
* Bug fixes in the JavaScript.

Then there's a new filter tool, under "Do you have lots of posts?". You can choose whether to include reblogs, or just show posts that you wrote. This wasn't my idea; it came from a tweet:

{% tweet https://twitter.com/A5HRAJ/status/516449552102993920 %}

and after initially misunderstanding what they meant, I put something together pretty quickly. I'm not particularly keen on adding more options like this, because I don't want it to be too complicated: if you want really granular control, just play around with the API yourself.

But Ash's tweet got me thinking about something else: at the bottom of a Tumblr post, there are three kinds of note: likes, reblogs, and reblogs with commentary. The latter are the most interesting to me, but they're also buried under everything else. Is there a good way to find all the commentary?

My first thought was the API, but that doesn't work: the API will only return the first 50&nbsp;notes on a post, and there's no way to get any more. Inspecting the "Show more notes" button at the bottom of a page reveals a private notes API, but it has a seemingly random key that I don't have. Also, I feel a little hesitant to start using undocumented APIs.

Maybe I could use a page scraper, and just automate pressing "Show more notes"? Nope, because that's forbidden by the [Tumblr Terms of Service] [tos] (under "Limitations on Automated Use"):

> You may not, without express prior written permission, do any of the following while accessing or using the Services: […] scrape the Services, and particularly scrape Content (as defined below) from the Services.

So in the end, I settled for a simpler solution: in the notes section at the bottom of a post, just hide anything which isn't a reblog with commentary. This comes down to a single line of CSS:

```css
ol.notes li.without_commentary { display: none !important; }
```

I have that in my custom CSS file, and now I only see the commentary on a post. It's only a small tweak, but I like it.

[futp]: http://finduntaggedtumblrposts.com/
[tos]: https://www.tumblr.com/policy/en/terms-of-service
