---
date: 2013-05-11 12:26:00 +0000
layout: post
slug: rss-podcasts-tumblr
summary: A barely advertised feature of Tumblr that lets you get an RSS feed of external
  audio posts.
tags: podcasts tumblr
title: Podcast feeds on Tumblr
---

On [episode&nbsp;12][atp12] of the [Accidental Tech Podcast][atp], Marco, Casey and John were discussing podcasts. They were comparing them to blogging, the way more people wanted to have their own podcast, and how the tools for making your own podcast compare to those for making your own blog. A little over an hour in, Marco mentioned a useful Easter egg in Tumblr for podcasters.

Marco was the co-founder and lead developer at Tumblr for about three and a half years. Every so often, he drops a nugget like this on one of his podcasts, telling you about an undocumented feature of Tumblr that turns out to be really useful. Since I haven't read this one mentioned anywhere else, I decided to break it out into a nice, Google-searchable blog post.

Skip to the 1&nbsp;hr 3&nbsp;min mark for the relevant segment. Marco:

> Tumblr also supports podcast hosting if you host the files elsewhere. I believe if you go to any Tumblr site /podcast, or maybe /podcast/RSS, it will give you an iTunes compatible podcast feed of any audio posts that are externally hosted.

I went to have a play, and this feature still works. You want the first, rather than the second, extension. Adding `/podcast` to a Tumblr site gives you an RSS feed for the podcast. If you a Tumblr site under your own domain name, then adding `/podcast` to that works just as well.

Handy!

<!-- summary -->

**A disclaimer:** I haven't tested any of this extensively, and I don't know anybody at Tumblr who'd be able to explain exactly how this feature works, but I thought it was useful enough to share with other people.

## Notes

I tested this in iTunes, Instacast and Reeder, and all three seemed to load the file without problems. Show notes seem to come from the text included in the post.

For reasons that aren't immediately obvious, loading the feed in Chrome throws up the following error:

> This XML file does not appear to have any style information associated with it. The document tree is shown below.

In this case, Chrome doesn't pass the RSS feed out to a feed reading application, such as Reeder. However, copying and pasting the URL seems to work just fine.

Indeed, this Chrome bug seems to occur in lots (all?) of Tumblr's RSS feeds. However, all of the feeds I've tried parse correctly for me, so I'm not sure how much of a problem it is.

On the subject of RSS feeds, here are two more handy tips:

<ul>
<li><p>If you add <code>/tagged/mygreattag</code> to a Tumblr URL, then you get all of the posts from that Tumblr site that have been tagged with "mygreattag". I find that pretty useful.</p>

<p>For example, <a href="http://natgeofound.tumblr.com/tagged/africa">http://natgeofound.tumblr.com/tagged/africa</a> takes you to all the posts on the <a href="http://natgeofound.tumblr.com/">National Geographic</a> Tumblr site with the tag "Africa". (There are some really stunning photos on that site. Definitely worth checking out.)</p></li>
<li>You can then add <code>/rss</code> to that URL to get a nice RSS feed of all the posts with that tag.</li>
</ul>

Some Googling showed up this second tip as another way to get podcast RSS feeds from Tumblr: tag all your episodes with "podcast", then get the RSS feed associated with that tag. I haven't tried that myself, so I don't know how it compares to the method above, but it's always nice to have options.

[atp]: http://atp.fm/
[atp12]: http://atp.fm/episodes/12-accidental-server-hardware
