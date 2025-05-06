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

Tools like [ArchiveBox], [Webrecorder], and the [Wayback Machine] have preserved enormous chunks of the web, pages that would otherwise be lost.
I paid for a Pinboard [archiving account] for a decade, and I look for a page in the Internet Archive at least once a week.
I've used tools like [wget], and last year I wrote a command-line tool to [create Safari webarchives][safari_webarchives].
The size and scale of our existing web archives is entirely due to automation.

But automation isn't a panacea, it's a trade-off.
You trade speed for accuracy -- nobody is reviewing pages when they're archived, so they may have mistakes or missing files.

When I reviewed my Pinboard archive, I found a lot of gaps and broken pages.
These were web pages I really care about, and I thought I had a backup, but it was false sense of security.

People often say "a backup isn't a backup unless you test it".
What would it mean to test a backup of over two thousand web pages--reviewing every page by hand?
Opening each one in a web browser?
Checking for the text and images I actually care about?

That would be ridiculous, right?

Right?

I don't need a general purpose web archiving tool; I only care about creating an archive of a particular set of pages.
Once I know I have a good snapshot on a pages, I don't need to save it again -- I just need to keep that copy safe.
It would take a long time to create and review an archive by hand, but once it's done, it won't need much maintenance.

So I decided to create my archive manually.

I saved a static copy of every bookmark -- a folder with the HTML, stylesheets, images, and other linked resources.
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
    I flatten the structure of each website into a couple of top-level folders like <code>images</code> and <code>static</code>, to keep the archive simple and readable.
    I don’t care about the exact URLs used on the original site.
  </figcaption>
</figure>

This is the same approach I'm using for the bookmarks site itself, leaning on standards-based web technology to create something simple, reliable ,and likely to last.
For every page, I'd open it in my web browser and visually verify that everything saved correctly.

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

I start by saving an HTML file.
I usually use the "Save As" button my web browser.

I open each file in my web browser and my text editor, then I use the developer tools to look for supporting resources that I should save.
I save additional files and make changes in my text editor, then I reload the page in my browser and check the result.
I gradually iterate towards my desired result -- a self-contained, offline copy of the original web page.

When I'm in my browser's developer tools, I spend most of my time in tabs:

The *network* tab tells me about the resources the page is requesting -- is it loading files from my local disk, or a remote server?
The goal is that everything should be coming from a local disk.

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

The *console* tab tells me about errors loading the page -- a lot of red is usually a sign that there's a supporting resource I haven't saved yet.
The goal is to get to no errors.

For example, here's the console for an HTML file where I have yet to archive the fonts or images:

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

I keep downloading files or editing the HTML file until I have a self-contained, local copy of the page with all the supporting resources.
Everything is being loaded from my local disk, and the HTML page is making no external requests.

That means removing stuff I don't care about (like ads and tracking) and changing links to stuff I am keeping (like editing the `src` attribute of `<img>` tags).
I spent a lot of time reading and writing HTML.

### Templates for repeatedly-bookmarked sites

For large and complex websites that I bookmark regularly, I've created my own HTML templates that I can add content into.
I can copy/paste the words and pictures, but I don't need to unpick the complex HTML every time I want to save the page.
This includes sites like Medium, Tumblr, and the New York Times.

[[ comparison ]]

I was inspired by downloads on AO3, a popular fanfiction website.
They allow you to [download anything on the site](https://archiveofourown.org/faq/downloading-fanworks?language_id=en) in several different formats, and they believe in it so strongly that individual authors can't disable downloads of their work (although they can restrict visibility).

An HTML file downloaded from AO3 looks quite different to how it looks in the browser:

{comparison}

But I'm very happy with that HTML file as a backup -- it has all the words of the story, which is what I really care about.
I realised I could create similar templates for other sites.
**I'm preserving the content, not the container.**

### Backfilling my existing bookmarks

When I decided I wanted to a low-fi collection of static website archives, I already had partial collections from several sources, including Pinboard the Wayback Machine.
It took almost a year to go through and migrated those old pages to the new structure -- fixing errors,


---

This took me about a year, doing a few pages a day – and now I have a complete, local archive of (almost) every web page I care about, and I know that every page has a high-quality, useful snapshot.

I built this collection from a variety sources, including live pages, the Wayback Machine, and my Pinboard archiving account. There’s only one page that seems conclusively lost – a review of *Rogue One* whose only preserved copy is a content warning interstitial. I consider that a big success, but it’s also a sign of how fragmented our Internet archives are – some pages I had to cobble together with a whole mixture of sources.


### What do I want?


### Automated scraping vs manual creation





---



## How I created my web archives



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