---
layout: page
title: Privacy policy
date_updated: 2024-03-18 20:53:56 +0000
nav_section: contact
---
**tl;dr: I don't do anything weird or creepy with your data.**

Here's what I collect:

*   Some basic, anonymised information about visits to my website
*   Your email address, if you subscribe to my email newsletter

## Visits to my website

When you visit a page, I use a [tracking pixel](https://en.wikipedia.org/wiki/Spy_pixel) to record the following values:

*   The current date
*   The URL and title of the page you were looking at
*   The referrer, i.e. which page linked you to my website
*   The country you're in (which is guessed from your IP address)
*   Whether you're a bot or crawler (this is a simple boolean based on your User-Agent, so I can separate humans from Google's search crawler)

Here's an example of how a visit might be recorded in my database:

```
date:      2024-03-18T20:38:16.894394
url:       https://alexwlchan.net/2024/step-step-step/
referrer:  https://www.linkedin.com/
title:     Monki Gras 2024: Step… Step… Step… – alexwlchan
country:   GB
is_bot:    False
```

I gather statistics in aggregate, and I deliberately don't collect any information that might allow me to identify specific visitors.
For example, I could see that 100 people read a post, but I can't see (a) who those 100 people were nor (b) if you were one of them.

In particular, I never record your exact IP address or User-Agent header.
They might make it possible to identify a specific person or their browsing habits, and I don't want that.

### Third parties

The tracking pixel is served from my web server.
I don't share any of the information I get from it – that only lives on my web server and my personal computers.

I don't use any analytics frameworks that share data with other companies (e.g. Google Analytics, Piwik, or Fathom).

The site is hosted on Netlify.
They can see what pages you're visiting, and they have [their own privacy policy](https://www.netlify.com/privacy/).

The web server with the tracking pixel is hosted on Linode.
They can see that you've hitting the tracking pixel, but nothing more detailed (they could work out you visited my site, but not which page).
Linode is owned by Akamai, who have [their own privacy policy](https://www.akamai.com/legal/privacy-statement).

## Email newsletter

I run an email newsletter which is powered by Buttondown.

If you want to receive my newsletter, you have to give me your email address.
I only use that email address to send out newsletters, and nothing else.
I only share your email address with Buttondown, because they need it to send the newsletters on my behalf.

If you don't want to receive the newsletter any more, you can unsubscribe whenever you like.

Buttondown have [their own privacy policy](https://buttondown.com/legal/privacy) which describes how they use your data.

## Cookies

I don't set any.

## Page history

*   5 October 2024: Simplify the text, and add a section on my email newsletter. 
*   18 March 2024:
    Remove reference to screen width/height, which I no longer collect.
    Add an example of how a request get recorded in my database.
    Clarify how Linode/Netlify are involved.
    Tweak a few bits of wording.
*   20 January 2024: Initial version of page. Add information about my new tracking pixel.
