---
layout: post
title: How I built a personal archive of the web
summary: |
  How I built a web archive by hand, the tradeoffs between manual and automated archiving, and what I learnt about preserving the web.
tags:
  - bookmarking
  - digital preservation
index:
  feature: true
colors:
  css_light: "#0000ff"
  css_dark:  "#00ddff"
  index_light: "#2f2f2f"
  index_dark:  "#66b8e8"
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
        <li><a href="#deleting_the_junk">Creating a junk-free web archive</a></li>
        <li><a href="#what_i_learnt">What I learnt about archiving the web</a></li>
        <li><a href="#conclusion">Should you do this?</a></li>
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

  .toc ol > li > ul {
    list-style-type: disc;
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



<h2 id="deleting_the_junk">Creating a junk-free web archive</h2>

As I was saving web pages, I deleted all the stuff I didn’t care about.
This made the saved copies smaller and easier to read, and pages often shrank by 10--20&times; after I removed all the junk.

My "favourite" was a Squarespace site that loaded over 25MB of JavaScript to render a 400-word essay with no images.

The junk I deleted includes:

*   **Ads.**
    So many ads.
    I found one especially aggressive plugin inserted an advertising `<div>` between every single paragraph.

*   **Banners for time-sensitive events.**
    News tickers, announcements, limited-time promotions, and in one case, a museum's bank holiday opening hours.

*   **Inline links to related content.**
    There's an annoying trend in online publications where every few paragraphs you get a promo for a different article.
    I'm already reading -- stop trying to distract me!
    I deleted all those, so now saved articles are just the text, as the author intended.

*   **Cookie notices, analytics, tracking, and other services for gathering "consent".**
    These are large and completely unnecessary to me -- I care about the content of a web page, not what it was tracking about me.

    After deleting the 200th copy of Google Analytics from my archive, I got curious and checked how many times it's been saved in the Wayback Machine.
    [Over 11 million copies](https://web.archive.org/web/20240000000000*/https://ssl.google-analytics.com/ga.js)!

While I was editing the page in my text editor, I'd look for `<script>` and `<iframe>` elements -- good indicators of external junk I could remove.
This didn't just shrink the page; it also removed external dependencies that might break in future.
That makes the archive easier to preserve.

This sort of editing only works because this is a *personal* archive, not an *institutional* one.
Public archives prioritise provenance and immutability -- making sure the original files are preserved exactly as they were, or keeping detailed records when there are changes.
That helps avoid personal bias creeping into the archive, and builds trust in what's being kept.

I haven’t kept detailed records of what I deleted, because I'm not preserving history for the public.
I'm preserving the web for me.



---



<h2 id="what_i_learnt">What I learnt about archiving the web</h2>

### Lots of the web is built on now-defunct services

Link rot is everywhere on the web, and I saw a lot of it on web pages that relied on third-party services that no longer exist, like:

*   Photo sharing services -- some I'd heard of (Twitpic, Yfrog) and others that were new to me (like phto.ch)
*   Link redirection services -- both URL shorteners and sponsored redirects
*   Social media sharing buttons and embeds

The main page loads, but key resources like images and scripts are broken or missing.

One particularly insidious kind of breakage is when the service still exists, but the content has changed.
Here's an example: a screenshot from an iTunes tutorial on LiveJournal that's been replaced with an "18+ warning":

<figure style="width: calc(450px);">
  <div style="display: grid; grid-template-columns: auto auto; grid-gap: 0.5em; align-items: center;">
    {%
      picture
      filename="bookmarks/001akef1.png"
      width="78"
      class="screenshot"
    %}
    {%
      picture
      filename="bookmarks/122942_original.png"
      width="300"
    %}
  </div>
  <figcaption>
    A modern day horror story: a computer user interface that wasn't designed for touch screens.
  </figcaption>
</figure>

This kind of failure is harder for automated crawlers to detect -- the server returns a valid response, just not the one you expect.
This is the sort of thing I was trying to catch by looking at every web page with my eyes.

I deliberately build websites with minimal third-party dependencies to avoid this sort of breakage -- and seeing how many once-reliable services have vanished makes me feel even better about that decision.

### Links rot faster than web pages

I was surprised by how many web pages still exist, but the original URLs no longer work -- especially on large news sites.
A link I saved in 2015 might now return a 404, but if I search the headline, I'll often find the story at a completely different URL.

I find this frustrating and disappointing.
Whenever I've restructured this site, I always set up redirects because I'm an old-school web nerd and I [think URLs are cool][urls] -- but redirects aren't just about making me feel good.
Keeping links alive makes your back catalogue more visible, and makes pages easier to find -- without them, most people who encounter a broken link will assume the article was deleted, and won't dig further.

[urls]: https://www.w3.org/Provider/Style/URI.html

### Lazy loading is a headache for backups

Modern lazy loading is easy with [`<img loading="lazy">`][lazy_loading], but I found a lot of DIY implementations that predate that attribute.

A common pattern: load a low-res image first, then swap it out for a high-res version with JavaScript.
But those high-res images weren't always captured by automated tools -- sometimes I had to go digging.

Another common pattern: a page that starts with a style like `opacity: 0` or `overflow: hidden`, and then runs JavaScript to remove those styles once the page has loaded.
But if that script breaks, the archive page is just… blank.
I had to remove all those styles manually.

This feels like an over-reliance on custom JavaScript, and a failure to think about [progressive enhancement] -- the idea that a site should work even if JavaScript doesn’t.
It's fragile design, and I feel good about my own reluctance to use client-side JS unless I absolutely have to.

[lazy_loading]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img#loading
[progressive enhancement]: https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement

### There’s no clearly-defined boundary of what to collect

Several times I found myself unsure of how much to archive.

For example: Molly White's talk [*Fighting for our web*][fighting] includes an embedded YouTube video.
I think the video is a key part of the page, so I wanted to download it -- but “download all embeds and links” would be a very expensive rule.

Another example: I've bookmarked blog posts that comment on scientific papers.
I saved a local copy of the blog post and a PDF of the original paper, but I didn't try to download everything the post links to.

I made decisions about what to download on a case-by-case basis.
There's no hard rule -- it depends on the content and the context.

[fighting]: https://www.citationneeded.news/fighting-for-our-web/



---



<h2 id="conclusion">Should you do this?</h2>

Creating a web archive is always a tradeoff between speed and quality.
Automated tools are fast but imperfect.
Manual archiving is slow, picky work that demands comfort with HTML, CSS, and JavaScript -- but it gives you the confident that you've saved what matters.

It took me hundreds of hours to build my archive.
Now I have over 2000 web pages saved in a stable format, with the key resources intact and quality-checked by hand.
That's no small achievement -- and I'm very glad to have it -- but I won't pretend I can recommend the process.
It was a big time commitment.

And yet, I found something unexpected in the process.
By archiving all these pages, I wasn't just saving the web -- I was learning how it's built.
Reading hundreds of sites taught me lessons about semantic HTML, modern CSS, and other web technologies.

In part 3 of this series, I'll share what I learnt about making better websites by trying to save them.

If you'd like to know when that article goes live, [subscribe to my RSS feed or newsletter](/subscribe/)!
