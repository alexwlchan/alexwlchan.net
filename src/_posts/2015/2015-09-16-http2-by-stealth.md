---
date: 2015-09-16 20:59:00 +0000
layout: post
slug: http2-by-stealth
summary: Apple has quietly adopted HTTP/2 in iOS 9 and El Capitan, and (almost) nobody
  noticed.
tags: os x, http/2
title: Apple quietly adopts HTTP/2
---

Amongst all the new features in iOS 9, I spotted one on Twitter that I hadn't seen before:

<null tweet="https://twitter.com/Lukasaoz/status/644243079445221376"/>

It turns out that Cory <a href="https://lukasa.co.uk/2015/06/HTTP2_Picks_Up_Steam_iOS9/">blogged about this</a> several months ago, but otherwise this change seems to have passed very quietly.

The status quo &ndash; HTTP/1.1 &ndash; is over fifteen years old.
The web has changed a lot since then, and decisions made for the web of 1997 just don't make sense today.
Enter HTTP/2: a new protocol intended to replace HTTP/1.1, with a design that's appropriate for the modern web.
It's been in the works for several years, and was finally published as an RFC in May.

I first heard of HTTP/2 in [Cory's talk at PyCon][pycon], and I thought it was an interesting technical idea.
He makes a compelling case for the benefits, but I didn't expect it to be adopted quickly.
Until lots of browers could use it, who would rush to adopt it server-side?

With iOS 9, that calculus has changed.

It turns out that Apple announced support for HTTP/2 all the way back in June, at WWDC: [*Networking with NSURLSession*][wwdc] (start at the 13 minute mark).
The same session introduced App Transport Security (HTTPS by default for all apps), and I suspect that overshadowed this announcement.
It doesn't help that I've found almost no mention of it [in Apple's developer docs][docs].

But the crux is this:

**As of iOS 9 and El Capitan, all NSURLSession requests can support HTTP/2.**
(And if you've been running the developer seeds, you've had it for a while.)

Apple have been using this themselves: remote access to HomeKit devices via iCloud all goes via HTTP/2.
And I wouldn't be surprised if they start using it to push out software updates, given that CDNs were explicitly called out as an HTTP/2 provider in that session.

Even assuming a very conservative adoption rate, there are now tens of millions of new clients that support HTTP/2.
That's got to push the needle on server-side adoption (and guess what I'm planning for next weekend!).

HTTP is a fundamental part of the web, and HTTP/2 is a key part of its future.
I'm incredibly pleased to see Apple driving it forward.

[pycon]: https://www.youtube.com/watch?v=ACXVyvm5eTc
[wwdc]: https://developer.apple.com/videos/wwdc/2015/?id=711
[docs]: https://developer.apple.com/search/?q=http%2F2
