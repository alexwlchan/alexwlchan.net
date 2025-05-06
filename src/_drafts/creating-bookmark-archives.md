---
layout: post
title: Creating a local archive of all my bookmarks
summary:
tags:
  - bookmarking
  - digital preservation
colors:
  css_light: "#0000ff"
  css_dark:  "#00ddff"
---
In [my previous post](/2025/bookmarks-static-site/), I described how I've created a static website for all my bookmarks.
A key part of this setup is that I have a local copy of every page that I've bookmarked.

My bookmarks are the links I really care about, so I want to keep my own copy that’s protected from deletion -- websites can easily break or go offline.
I want my own copy, saved locally, which I can know is safe.
I don't want to rely on a page being archived by a third-party service like Pinboard or the Wayback Machine.

In this second post, I'll talk about how I created a local copy of every link I've bookmarked, the tools I chose, and how I ensured the quality of my archive.

<blockquote class="toc">
  <p>This article is the second in a four part bookmarking mini-series:</p>
  <ol>
    <li>
      <a href="/2025/bookmarks-static-site/"><strong>Creating a static site for all my bookmarks</strong></a> – why do I bookmark, why use a static site, and how does it work.
    </li>
    <li>
      <strong>Creating a local archive of all my bookmarks</strong> (this article)
      <ul>
        <li><a href="#requirements">What do I want in a web page archive?</a></li>
        <li><a href="#manual_archiving">Why I chose a manual approach</a></li>
        <li><a href="#howto">How I create my local web archives</a></li>
      </ul>
    </li>
    <li>
      <a href="#"><strong>Learning how to make websites by reading two thousand web pages</strong></a> (coming 19 May) – everything I learnt from reading the source code of the web pages I saved.
    </li>
    <li>
      <a href="#"><strong>Some cool websites from my bookmark collection</strong></a> (coming 26 May) – some websites which are doing especially fun or clever things with the web.
    </li>
  </ol>
</blockquote>

<style>
  .toc {
    background: var(--background-color);
    border-color: var(--primary-color);
  }

  .toc ol > li:not(:last-child) {
    margin-bottom: 1em;
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>



---



<h2 id="requirements">What do I want in a web page archive?</h2>

It's worth describing my requirements, because I'm building a *personal* web archive -- something I'll maintain myself, tailored to my own needs.
I can also lean on my skills as a web developer to shape how it works.

This is quite different to what I'd do if I was in a professional or institutional setting.
There, the priorities are usually different: automation over manual effort, immutability over editability, and a strong focus on public-facing content.
You also can't assume everyone involved knows how to dig into HTML or browser dev tools.

### I want a high-quality copy of every web page I save

If the original page goes away, my archive should still be useful.
That means I need to keep the "essential" parts -- not just the text, but also any illustrations, images, or layout elements that are key to understand the page.

In the past, I've relied too heavily on automation, and ended up with incomplete archives: missing images, broken styles, or partial content.
This time, I'm aiming for a much higher-quality archive.

### I want the archive to live on my local computer

I don't want to rely on a third party service, which could break, change, or be shut down.

I learnt this the hard way with Pinboard.
I was paying for an [archiving account], which promised to keep an archived copy of all my bookmarks.
But in recent years it's become unreliable -- sometimes it would fail to archive a page, and sometimes it couldn't retrieve a supposedly saved page.

### It should be easy to save new pages

I save a couple of bookmarks a new week.
I want to keep this archive up-to-date, and I don't want it to become a chore.

### It should support private or paywalled pages

I read a lot of pages behind paywalls or login screens, which are invisible to public web archives like the Wayback Machine.
I still want to keep a local copy -- indeed, the fact that the pages are private makes it more important that I keep my own copy, because I may not  another.

### It should be possible to edit pages

This is something I discovered as I was creating my new archive.
Web pages contain a lot of junk that I don't care to preserve -- ads, tracking, pop-ups.
It's like saving clippings from a magazine: I want the article, not the ads wrapped around it.
I want to be able to trim what I save, and just keep the useful parts.

[archiving account]: https://pinboard.in/faq/#archiving



---



<h2 id="manual_archiving">Why I chose a manual approach</h2>

I'm a big fan of automated tools for archiving the web, and I've used them a lot over the years.

Tools like [ArchiveBox], [Webrecorder], and the [Wayback Machine] have preserved enormous chunks of the web -- pages that would otherwise be lost.
I paid for a Pinboard [archiving account] for a decade, and I search the Internet Archive at least once a week.
I've used tools like [wget], and last year I even wrote a command-line tool to [create Safari webarchives][safari_webarchives].
The size and scale of today's web archives are only possible because of automation.

But automation isn't a panacea -- it's a trade-off.
You trade speed for accuracy.
Nobody is reviewing pages as they're archived, so they can contains mistakes or be missing essential files.

When I reviewed my old Pinboard archive, I found a lot of broken pages and missing content.
These were web I really care about, and I thought I had them backed up, but that turned out to be a false sense of security.

People often say "a backup isn't a backup unless you test it".
What would it mean to test a backup of over two thousand web pages?
Reviewing every page by hand?
Opening each one in a web browser?
Checking they include the text and images I actually care about?

That would be ridiculous, right?

Right?

I don't need a general purpose web archiving tool -- I just need an archive of a particular set of pages.
Once I know I have a good snapshot on a pages, I don't need to save it again; I just need to keep that copy safe.
Create and checking an archive by hand takes time, but once it's done, it's low maintenance.

So I decided to create my archive manually.

### A static folder for every page

For every bookmark, I saved a static copy: a folder containing the HTML, stylesheets, images, and other linked files.
Each one is a self-contained "mini-website" that I can open in a browser, even if the original page disappears.

<figure style="width: 550px;">
  {%
    picture
    filename="bookmarks/mini_website.png"
    width="550"
    class="screenshot"
    alt="Screnshot of a folder containing an HTML page, and two folders with linked resources: images and static."
  %}
  <figcaption>
    The files for <a href="https://preshing.com/20110926/high-resolution-mandelbrot-in-obfuscated-python/">a single web page</a>, saved in a folder in my archive.
  </figcaption>
</figure>

Each page lives in its own folder.
I flatten the structure of each website into top-level folders like <code>images</code> and <code>static</code>, which keeps things simple and readable.
I don’t care about the exact URL paths from the original site.

This is the same approach I'm using for the bookmarks site itself, leaning on standards-based web technology to create something simple, durable, and easo to maintain.
For every page, I open it in my web browser and verify that everything loads correctly.

Let's go through the process in more detail.

[ArchiveBox]: https://archivebox.io/
[Webrecorder]: https://webrecorder.net/
[Wayback Machine]: https://web.archive.org/
[archiving account]: https://pinboard.in/faq/#archiving
[wget]: https://www.gnu.org/software/wget/manual/wget.html#Recursive-Download
[safari_webarchives]: http://localhost:5757/2024/creating-a-safari-webarchive/



---



<h2 id="howto">How I create my local web archives</h2>

### Saving a single web page

I start by saving the HTML file, usually using the "Save As" button my web browser.

Then I open that file in a web browser and my text editor.
Using the browser's developer tools, I look for supporting resources that I need to save locally -- stylesheets, fonts, images.
I download any missing files, edit the HTML in my text editor to point at the local copy, then reload the page in the browser to see the result.
I keep going until I have a self-contained, offline copy of the page.

Most of my time in the developer tools is spent in two tabs.

**Network** show me what resources the page is loading.
Are they being served from my local disk, or fetched from the Internet?
The goal is that *everything* comes from disk.

<figure style="width: 600px;">
  {%
    picture
    filename="bookmarks/network_tab.png"
    width="600"
    class="screenshot"
    alt="The network tab in my browser developer tools, which has a list of files loaded by the page, and the domain they were loaded from. A lot of these files were loaded from remote servers."
  %}
  <figcaption>
    This HTML file is making a lot of external network requests – I have more work to do!
  </figcaption>
</figure>

**Console** tells me about errors loading the page -- some image that can't be found, or a JavaScript file that didn't load properly.
A wall of red means I've missed something, like a font or image I haven't downloaded yet.
My goal is to get to zero errors.

<figure style="width: 600px;">
  {%
    picture
    filename="bookmarks/console_errors.png"
    width="600"
    class="screenshot"
    alt="The console tab in my browser developer tools, which has a lot of messages highlighted in red about resources that weren't loaded properly."
  %}
  <figcaption>
    So much red!
  </figcaption>
</figure>

As I'm editing the page, I remove stuff I don't care about (ads, banners, tracking) and update references to things I'm keeping (like changing the `src` on `<img>` tags).
I spent a lot of time reading and editing HTML by hand.

Once I've downloaded everything the page needs and eliminated external requests, I have a self-contained local copy.

### Templates for repeatedly-bookmarked sites

For big, complex websites that I bookmark often -- like Medium, Wired, or the New York Times -- I've created simple HTML templates.
I drop in the text and images, but I don't need to unpick the site's HTML every time.
These templates save me a lot of effort.

<figure style="width: 600px;">
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 0.5em;">
    {%
      picture
      filename="bookmarks/nytimes_theirs.png"
      width="300"
      class="screenshot"
      style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
    %}
    {%
      picture
      filename="bookmarks/nytimes_mine.png"
      width="300"
      class="screenshot"
      style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
    %}
  </div>
  <figcaption>
    You can tell which one is the <a href="https://www.nytimes.com/2016/03/27/opinion/sunday/my-mothers-garden.html">real article</a>, because you have to click through two dialogs and scroll past an ad before you see any text.
  </figcaption>
</figure>

This approach was inspired by AO3 (the Archive of Our Own), a popular fanfiction site.
They offer [downloadable versions](https://archiveofourown.org/faq/downloading-fanworks?language_id=en) of every story in multiple formats, and they believe in it so strongly that individual authors *can't* disable downloads of their work -- though they can restrict visibility.

An HTML download from AO3 looks different to the styled version you'd see browsing the web:

<figure style="width: 600px;">
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 0.5em;">
    {%
      picture
      filename="bookmarks/ao3_theirs.png"
      width="300"
      class="screenshot"
      style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
    %}
    {%
      picture
      filename="bookmarks/ao3_mine.png"
      width="300"
      class="screenshot"
      style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
    %}
  </div>
</figure>

That unstyled HTML file may not look the same, but it's still a meaningful backup.
It has the story, which is what I really care about.
That helped me realise I could do something similar for other sites: **I want to preserve the content, not the container.**

### Backfilling my existing bookmarks

When I decided I wanted to a lo-fi collection of static web archives, I already had partial collections from several sources -- Pinboard, the Wayback Machine, and some local backups.

It took almost a year to go through and migrate those into the new structure: fixing broken pages, downloading missing files, deleting ads and tracking scripts.
Now I have a collection where I've checked every bookmark, and I know I have a complete set of local copies.

There's only one bookmark that seems conclusively lost -- a review of *Rogue One* on Dreamwidth, where the only surviving capture is a content warning interstitial.

I consider this a big success, but it's also a reminder of how fragmented our internet archives are.
Many of my archived pages are "franken-archives" -- stitched together from multiple sources, combining pieces that were saved years apart.

### How I backup the backups

Once I have a website saved as static files on my local machine, those files get backed up like everything else.

I use [Time Machine] and [Carbon Copy Cloner] to back up to a pair of external SSDs, and [Backblaze] to create a cloud backup that lives somewhere other than my house.

[Time Machine]: https://en.wikipedia.org/wiki/Time_Machine_(macOS)
[Carbon Copy Cloner]: https://bombich.com/
[Backblaze]: https://secure.backblaze.com/r/01h8yj



---



## What I learnt about archiving the web

### Preserving the content, not the container

### Lots of the web is built on now-defunct services

### Links rot faster than web pages

### Lazy loading is a headache for preservation

### There's no clearly-defined boundary of what to collect

### So many websites are a bloated mess



---



## Should you do this?


---

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