---
layout: post
title: Creating a local archive of all my bookmarks
summary:
tags:
  - bookmarking
  - digital preservation
---
In my previous post, I described how I’ve created a static website for all my bookmarks. A key part of this setup is that I have a local copy of every page I’ve bookmarked.

Websites break or go offline, and these are the web pages I really care about, so I want to keep my own copy that’s protected from deletion. I don’t want to rely on a page it being saved by a Pinboard archiving account or the Wayback Machine – I want my own copy, which I can know is safe.

(( mention static websites ))

## Preserve the content, not the container

I was inspired by downloads on AO3, a popular fanfiction website. They allow you to [download anything in the archive](https://archiveofourown.org/faq/downloading-fanworks?language_id=en) in several different formats, and they believe in it so strongly that individual authors can’t disable downloads of their work (although they can restrict visibility).

When you download a work from AO3, you get a single HTML file that looks quite different to how it looks in the browser:

{comparison}

I’m very happy with that HTML file as a backup – I still have all the words of the story, which is what I really care about.

I was thinking about this at the same time as I wrote {Using static websites}. What if I created a micro-website for each web page I archived – an HTML file with supporting CSS, JavaScript and image files that just sits in a folder? So that’s what I ended up doing.

## Automated scraping vs manual creation

I’m a big fan of automated tools for archiving the web – tools like ArchiveBox, Web Recorder, and the Wayback Machine have allowed the preservation of enormous chunks of the web, pages that would otherwise be lost. I paid for a Pinboard archiving account for a decade, and I probably look for a page in the Internet Archive at least once a week. I’ve used tools like wget, and last year I wrote a command-line tool to automate the creation of Safari webarchives. The size and value of our large web archives is entirely due to automation.

But automation isn’t a panacea – it’s a trade-off. You trade speed for accuracy – archived pages aren’t looked at the point of saving, so they may have mistakes or missing files. When I reviewed my Pinboard archive, I sometimes found gaps and broken pages. These were web pages I really cared about, and I thought I had a backup, but it was false hope.

A common saying is “a backup isn’t a backup unless you test it” – what would it mean to test a web archive of 2,500 pages? Would it mean reviewing every archived page by hand? Opening it and checking it has the text and images I care about? That would be ridiculous, right?

Would it?

I’m not interested in building a general-purpose web archiving tool – I only care about a (relatively) short list of particular pages. Once I know I have a good snapshot of that page, I don’t need to do it again – I just need to keep those files around.

So that’s what I did.

## How I did it

I started with my existing archive, which was cobbled together from a collection of automated tools, like Pinboard and Safari webarchiver.

I’ve unpack that into files on disk – an HTML file and supporting resources – then open it in my web browser. I spent a lot of time looking in two tabs:

* The "network" tab would show me if a web page was making any external requests, a clue that I needed to save more files to my archive
* The "console" tab would show me any errors, to show me if a web page was trying to load any resources that I didn’t have saved yet

I kept downloading files or editing the HTML file until I had a "clean" archive – a file that had everything I thought was worth saving, loading everything from my local disk and making no external requests. This meant removing stuff I didn't care about (like ads and tracking) and changing links to the stuff I did (like changing `<img>` tags to point to a local file rather than a server). I spent a lot of time reading and writing HTML.

When I save new bookmarks today, I start by saving the page source as an HTML file, then I repeat the process – look for external resources being loaded, save them locally, update the page to fetch the file from the disk.

For large and complex websites that came up repeatedly, I created my own HTML templates that I could drop content into – somewhere to put the words and pictures, but without keeping the entire page. These sites include Medium, Tumblr, and the New York Times.

This took me about a year, doing a few pages a day – and now I have a complete, local archive of (almost) every web page I care about, and I know that every page has a high-quality, useful snapshot.

I built this collection from a variety sources, including live pages, the Wayback Machine, and my Pinboard archiving account. There’s only one page that seems conclusively lost – a review of *Rogue One* whose only preserved copy is a content warning interstitial. I consider that a big success, but it’s also a sign of how fragmented our Internet archives are – some pages I had to cobble together with a whole mixture of sources.

## What I learnt about archiving the web

### Lots of the web is built on now-defunct services

Link rot is a big part of the web, and I saw a lot of it on web pages that relied on third-party services that no longer exist, like:

* Photo sharing services, some of which I’d heard of (Twitpic or Yfrog) and others that were new to me (like phto.ch)
* Link redirection services, both URL shorteners and sponsored redirects
* Social media sharing buttons and embeds

The main web page is there, but some of the resources it relies on are just broken.

One particularly insidious flavour of breakage I saw is when the service still exists, but the content has changed. Here’s one example, where an image on LiveJournal has been replaced with an “18+ warning”:

{before/after comparison}

This is harder for automated crawlers to detect – it’s returning a response, it’s just the wrong one. This is the sort of thing I was trying to catch by looking at every web page with my yes.

I deliberately build websites with minimal third-party dependencies to avoid this sort of breakage, and seeing the number of once-reliable services that have vanished makes me feel better about that.

### Links rot faster than web pages

I was quite disappointed by the number of web pages that had stayed up, but the URLs had changed without redirects.

This was particularly common on large news websites. I saved a link sometime in 2015, and the URL returns a 404 – but if I search for the headline, I find the story available on their site at a completely different URL.

I care about maintaining redirects because I think URLs are meaningful, but this also hurts website owners. This makes the back catalogue less visible, because it breaks any incoming URLs, and most people will assume it’s just deleted, and not spend the time to find the new URL.

### Lazy loading is a headache for backups

If you want lazy loaded images on the web today, you can use `<img>` with `loading="lazy>`, but I found a lot of DIY implementations that predate that attribute being widely supported.

For example, a common pattern is to load a low-res image by default, then use JavaScript to replace it with a high-res image later. I want the high-res image for my archive, but it wasn’t always captured by automated tools – sometimes I had to go digging around to find the proper image.

Another pattern I found is JavaScript pages that start with a style that blocks most of the page – `opacity: 0` or `overflow: hidden` – and then remove that style once the page loaded. This is fine if the JavaScript works correctly, but it often left me with a blank page when archived. I had to remove all those styles.

A lot of this feels like an over-reliance on custom JavaScript, and a failure to think about {progressive enhancement}. It works when everything loads correctly, but makes for brittle web pages. I feel good about my reluctance to use client-side JavaScript unless I absolutely have to.

### There’s no clearly-defined boundary of what to collect

One thing I found myself doing several times was grabbing linked resources, but it wasn’t always clear what to get.

For example, I was saving [Molly White’s talk about fighting for our web](https://www.citationneeded.news/fighting-for-our-web/), which includes an embedded YouTube video. I consider the video of her actually giving the talk to be a key part of the page, so I want to download it alongside the web page – but “download all embeds and links” would be an expensive rule, because those files can be very large. I made decisions about what to download on a case-by-case basis.

Another example: I have some bookmarks which are commentary on scientific papers, and they link to the original paper. I saved a copy of the PDF (and changed the page link to point to the archived version), but I don’t want to save everything that’s linked from a web page.

### So many websites are a bloated mess

I deleted so many things that were loaded by my saved web pages, but I’m not interested in saving, including ads, tracking, and cookie notices. This makes the saved web pages nicer to read, and reduces my storage cost – web pages routinely got 10–20× smaller when I stripped out the junk.

My “favourite” was a Squarespace site that loaded over 25MB of JavaScript to render a 400 word essay with no pictures.

After deleting the 200th copy of Google Analytics from my local archive, I decided to see how many copies of it exist in the Wayback Machine – [over 11 million](https://web.archive.org/web/20240000000000*/https://ssl.google-analytics.com/ga.js)!

## Should you do this?

How you create web archives is a tradeoff between speed and quality. Automated tools can gather a lot of pages very quickly, but there may be gaps or broken pages in the archive. Doing it manually is much slower and requires much more confidence with HTML, CSS and JavaScript, but then you know you've got everything you think is worth saving.

It took me hundreds of hours to create my local web archive, and now I have a collection of 2,500 saved web pages in a long-term format, with all their key resources, and which I have checked for quality. I'm very glad to have this, but it's difficult to recommend anybody follow in my footsteps. It's a big time commitment!

As I started doing this, I discovered this wasn’t a pure slog – by reading hundreds of websites, I was learning a lot about how websites are built. In the {final articles in this series}, I'll share everything I learnt about making websites.