---
layout: page
title: Privacy policy
date_updated: 2024-01-20 23:39:27 +0000
---
I collect some basic data about visits to my websites, to help me decide what to write about next.
I gather statistics in aggregate, and I don't collect any information about specific visitors.

For example, I can see that 100 people read a post, but I can't see (a) who those 100 people were nor (b) if you were one of them.

## What data I collect

Whenever you visit a page, I use a tracking pixel to record the following anonymised information:

*   The current date
*   The URL and title of the page you were looking at
*   The referrer, i.e. which page linked you to my website
*   The country you're in, which is guessed from your IP address
*   An anonymous session identifier, which I use to help count unique visitors (see below)
*   Whether you're a bot or crawler (this is a simple boolean based on your User-Agent, so I can separate humans from Google's search crawler)

Here's an example of how a visit would be recorded in my database:

```
date:      2024-03-18T20:38:16.894394
url:       https://alexwlchan.net/2024/step-step-step/
referrer:  https://www.linkedin.com/
title:     Monki Gras 2024: Step… Step… Step… – alexwlchan
country:   GB
is_bot:    False
```

I **don't** record your exact IP address or user agent, because they contain more detail than I need, and they'd make it easier for me to identify a specific person.
I don't want that!


## Anonymous session identifier

The session identifier is a tool to help me count unique visitors on the site.
To do this, I need to be able to correlate hits within the same visitor.
If I got three hits in quick succession, did they come from three people looking at one page each, or one person looking at three pages?

I create an anonymous session identifier which gets attached to each hit.
This is a randomly-assigned UUID that's attached to all requests coming from your (IP address, User-Agent) combination for the next 24 hours.
At the end of the day, that identifier expires and your next visit will be attached to a different session identifier.

This means that I can see that there was a person who looked at a particular set of pages on one day, but (a) I don't know who that person was and (b) I can't see what that person looked at the previous or next days.

## Third parties

The tracking pixel is served from my web server.
I don't share the information I get from it – that only lives on my web server and personal computers.

I don't use any third-party analytics frameworks like Google Analytics, Piwik, or Fathom.

This site is hosted on a mixture of Netlify and Linode.
They can see what pages you're visiting, and they have separate privacy policies.
([Netlify](https://www.netlify.com/privacy/); [Akamai](https://www.akamai.com/legal/privacy-statement), who own Linode.)

## Cookies

I don't set any.

## Page history

*   18 March 2024:
    Remove reference to screen width/height, which I no longer collect.
    Add an example of how a request get recorded in my database.
    Tweak a few bits of wording.
*   20 January 2024: Initial version of page. Add information about my new tracking pixel.
