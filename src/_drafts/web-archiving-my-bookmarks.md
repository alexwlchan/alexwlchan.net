---
layout: post
title: Building a personal archive of the web, the slow way
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
In [my previous post](/2025/bookmarks-static-site/), I described how I've created a static website to manage my bookmarks.
A key part of this setup is that I have a local archive of every page that I've bookmarked.

My bookmarks are the links I really care about, so I want to keep my own copy that’s protected from deletion or loss -- websites can easily break or go offline.
I want my own copy, which I control and know is safe.
I don't want to rely on a page being archived by an online service like Pinboard or the Wayback Machine.

In this second post, I'll talk about how I created a local copy of every link I've bookmarked, why I chose a manual approach, and how I ensured the quality of my archive.

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
        <li>
          <a href="#what_it_looks_like">What does my web archive look like?</a>
          <ul>
            <li><a href="#static_folders">A static folder for every page</a></li>
            <li><a href="#warc_or_wacz">Why not WARC or WACZ?</a></li>
          </ul>
        </li>
        <li>
          <a href="#howto">How do I save a local copy of each web page?</a>
          <ul>
            <li><a href="#saving_one_page">Saving a single web page by hand</a></li>
            <li><a href="#deleting_the_junk">Deleting all the junk</a></li>
            <li><a href="#templates">Using templates for repeatedly-bookmarked sites</a></li>
            <li><a href="#backfilling">Backfilling my existing bookmarks</a></li>
            <li><a href="#backups">Backing up the backups</a></li>
          </ul>
        </li>
        <li>
          <a href="#why_not_automation">Why not use automated tools?</a>
        </li>
        <li>
          <a href="#what_i_learnt">What I learnt about archiving the web</a>
          <ul>
            <li><a href="#defunct_services">Lots of the web is built on now-defunct services</a></li>
            <li><a href="#link_rot">Links rot faster than web pages</a></li>
            <li><a href="#lazy_loading">Images are becoming more efficient, but harder to preserve</a></li>
            <li><a href="#boundary">There’s no clearly-defined boundary of what to collect</a></li>
          </ul>
        </li>
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

  .toc ol > li > ul > li > ul {
    list-style-type: circle;
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>



---



<h2 id="requirements">What do I want in a web page archive?</h2>

I'm building a *personal* web archive -- it's just for me, and I'll maintain it myself.
It's not a public resource, and nobody else will be working on it.
I can shape it to my needs, and I can lean on my skills as a web developer when I build it.

This is quite different to what I'd do if I was in a professional or institutional setting.
There, the priorities are different: automation over manual effort, immutability over editability, and a strong focus on content that can be shared or made public.

### I want a high-quality copy of every web page I save

If the original page goes away, I want my archived copy to be a good substitute.
It should include text, images, styles, and anything else that's key to understanding the page.

Many web archives focus on volume over quality.
They'd rather save partial copies of a lot of web pages, rather than complete copies of a few web pages.
I'm the opposite -- I'm saving a fairly small number of web pages, so I want each saved page to be a complete copy.

### I want the archive to live on my computer

I don't want to rely on an online service which could break, change, or be shut down.

I learnt this the hard way with Pinboard.
I was paying for an [archiving account], which promised to save a copy of all my bookmarks.
But in recent years it's become unreliable -- sometimes it would fail to archive a page, and sometimes I couldn't retrieve a supposedly saved page.

### It should be easy to save new pages

I save a couple of bookmarks a week.
I want to keep this archive up-to-date, and I don't want adding new pages to be a chore.

### It should support private or paywalled pages

I read a lot of pages which aren't on the public web, stuff behind paywalls or login screens.
I want to include these in my web archive.

Many web archives only save public content -- because they can't access private content to save, and they couldn't share if it they did.
For example, pages behind login screens aren't captured in the Wayback Machine.
This makes it even more important that I keep my own copy of private pages, because I may not find another.

### It should be possible to edit pages

Web pages contain a lot of junk that I don't care about preserving -- ads, tracking, pop-ups, and more.
I want to cut all that stuff out, and just keep the useful parts.

It's like saving clippings from a magazine: I want the article, not the ads wrapped around it.

[archiving account]: https://pinboard.in/faq/#archiving



---



<h2 id="what_it_looks_like">What does my web archive look like?</h2>

I decided to treat my archived bookmarks like the bookmarks site itself: as static files, saved in folders on my local filesystem.

<h3 id="static_folders">A static folder for every page</h3>

For every bookmark, I have a folder containing the HTML, stylesheets, images, and other linked files.
Each folder is a self-contained "mini-website".
If I want to look at a saved page, I can just open the HTML file in my web browser.

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

Any time the HTML file refers to an external file, I've changed it to fetch the file from the local folder rather than the original website.
For example, the original HTML might have an `<img>` tag that loads an image from `https://preshing.com/~img/poster-wall.jpg`, but in my local copy I'd change the `<img>` tag to load the image from `images/poster-wall.jpg`.

I like this approach because it's using open, standards-based web technology to create something simple, durable and easy to maintain.

<h3 id="warc_or_wacz">Why not WARC or WACZ?</h3>

Many institutions store their web archives in the [WARC] or [WACZ] formats, which are file formats specifically designed to store preserved web pages.

These files contain the saved page, and information about how the archive was created.
This might include the HTTP headers, the IP address, or the name and version of the software that was used.
This extra information helps researchers understand the history of this archive.

You can only open WARC or WACZ files with specialist "playback" software, or by unpacking the files from the archive.
Both file formats are open standards, so you could also write your own software to read them -- archives saved this way aren't trapped in a proprietary format.

In my personal archive, I don't need the extra context, and I don't want to rely on a limited set of tools for browsing my archive.
I prefer the flexibility of files and folders -- I can open them in any web browser, and use whatever tools I like.

[WARC]: https://en.wikipedia.org/wiki/WARC_(file_format)
[WACZ]: https://specs.webrecorder.net/wacz/1.1.1/



---



<h2 id="howto">How do I save a local copy of each web page?</h2>

I'm saving web pages by hand.
I save every page individually, then I check it looks good -- that I've saved all the external resources like images and stylesheets.

This manual inspection gives me the peace of mind to know that I really have saved each web page, and that it's a high quality copy.
I'm not going to open a page in two years time only to discover that I'm missing a key image or illustration.

Let's go through that process in more detail.

<h3 id="saving_one_page">Saving a single web page by hand</h3>

I start by saving the HTML file, using the "Save As" button in my web browser.

Then I open that file in a web browser and my text editor.
Using the browser's developer tools, I look for supporting files that I need to save locally -- stylesheets, fonts, images.
I download the missing files, edit the HTML in my text editor to point at the local copy, then reload the page in the browser to see the result.
I keep going until I have a self-contained, offline copy of the page.

Most of my time in the developer tools is spent in two tabs.

**Network** show me what files the page is loading.
Are they being served from my local disk, or fetched from the Internet?
My goal is that everything comes from my disk.

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

As I'm editing the page, I remove stuff I don't care about (ads, banners, tracking) and update references to external files I'm downloading (like changing the `src` on `<img>` tags).
I spend a lot of time reading and editing HTML by hand.

Once I've downloaded everything the page needs and eliminated external requests, I have a self-contained local copy.

<h3 id="deleting_the_junk">Deleting all the junk</h3>

Deleting the junk from web pages makes them smaller and faster to load, and pages often shrank by 10--20&times; after I removed all the junk.
My "favourite" was a Squarespace site that loaded over 25MB of JavaScript to render a 400-word essay with no images.

The junk I deleted includes:

*   **Ads.**
    So many ads.
    I found one especially aggressive plugin that inserted an advertising `<div>` between every single paragraph.

*   **Banners for time-sensitive events.**
    News tickers, announcements, limited-time promotions, and in one case, a museum's bank holiday opening hours.

*   **Inline links to related content.**
    There are too many articles where, every few paragraphs, you get a promo for a different article.
    I find this quite distracting, especially as I'm already reading the site!
    I deleted all those, so my saved articles are just the text.

*   **Cookie notices, analytics, tracking, and other services for gathering "consent".**
    These are large and completely unnecessary to me -- I don't care what tracking tools a web page was using.
    They're a complete waste of space in my personal archive.

While I was editing the page in my text editor, I'd look for `<script>` and `<iframe>` elements -- good indicators of external junk I could remove.
This didn't just shrink the page; it also removed external dependencies that might break in future.

This sort of editing only works because this is a personal archive, not an institutional one.
Institutions tend to prioritise provenance and immutability -- making sure pages are preserved exactly as they were, or keeping detailed records when there are changes.
That helps avoid personal bias creeping into the archive, and builds trust in what's being kept.

I haven’t kept detailed records of what I deleted, because I'm not preserving history for an institution or the public.
I'm preserving the web for me.

<h3 id="templates">Using templates for repeatedly-bookmarked sites</h3>

For big, complex websites that I bookmark often -- like Medium, Wired, or the New York Times -- I've created simple HTML templates.

When I want to save a new page, I discard the original HTML, and I just drop the text and images into the template.
It's a lot faster than unpicking the site's HTML every time, and I'm saving the content of the article, which is what I really care about.

<figure style="width: 600px;">
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 0.5em;">
    {%
      picture
      filename="bookmarks/nytimes_theirs.png"
      width="300"
      class="screenshot"
      style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
      alt="Screenshot of an article on the New York Times website. You can only see a headline – most of the page is taken up by an ad and a cookie banner."
    %}
    {%
      picture
      filename="bookmarks/nytimes_mine.png"
      width="300"
      class="screenshot"
      style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
      alt="Screenshot of the same article saved in my archive. You can see the main illustration, the headline, and two paragraphs of the article."
    %}
  </div>
  <figcaption>
    You can tell which one is the <a href="https://www.nytimes.com/2016/03/27/opinion/sunday/my-mothers-garden.html">real article</a>, because you have to click through two dialogs and scroll past an ad before you see any text.
  </figcaption>
</figure>

I was inspired by AO3 (the Archive of Our Own), a popular fanfiction site.
They offer [downloadable versions](https://archiveofourown.org/faq/downloading-fanworks?language_id=en) of every story in multiple formats, and they believe in it so strongly that *everything* published on their site can be downloaded.
Authors don't get to opt out.

An HTML download from AO3 looks different to the styled version you'd see browsing the web:

<figure style="width: 600px;">
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 0.5em;">
    {%
      picture
      filename="bookmarks/ao3_theirs.png"
      width="300"
      class="screenshot"
      style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
      alt="Screenshot of a story ‘The Jacket Bar’ on AO3. There are styles and colours, and a red AO3 site header at the top fo the page."
    %}
    {%
      picture
      filename="bookmarks/ao3_mine.png"
      width="300"
      class="screenshot"
      style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
      alt="Screenshot of the same story, as an HTML download. It’s an unstyled HTML page, with Times New Roman font and default blue links."
    %}
  </div>
</figure>

This difference is only cosmetic -- both files contain the full text of the story, which is what I really care about.
I don't care about saving a visual snapshot of exactly what AO3 looked like that day.

Most sites don't offer a plain HTML download of their content, but I know enough HTML and CSS to create my own templates.
For these sites I save often, it's made it much faster to save new pages.

<h3 id="backfilling">Backfilling my existing bookmarks</h3>

When I decided to build a new web archive by hand, I already had partial collections from several sources -- Pinboard, the Wayback Machine, and some local backups.

It took almost a year to migrate them into the new structure: fixing broken pages, downloading missing files, deleting ads and tracking scripts.
Now I have a collection where I've checked every bookmark, and I know I have a complete set of local copies.

There's only one bookmark that seems conclusively lost -- a review of *Rogue One* on Dreamwidth, where the only capture I can find is a content warning interstitial.

I consider this a big success, but it's also a reminder of how fragmented our internet archives are.
Many of the pages in my new archive are "franken-archives" -- stitched together from multiple sources, combining files that were saved years apart.

<h3 id="backups">Backing up the backups</h3>

Once I have a website saved as a folder, that folder gets backed up like all my other files.

I use [Time Machine] and [Carbon Copy Cloner] to back up to a pair of external SSDs, and [Backblaze] to create a cloud backup that lives outside my house.

[Time Machine]: https://en.wikipedia.org/wiki/Time_Machine_(macOS)
[Carbon Copy Cloner]: https://bombich.com/
[Backblaze]: https://secure.backblaze.com/r/01h8yj



---



<h2 id="why_not_automation">Why not use automated tools?</h2>

I'm a big fan of automated tools for archiving the web, I think they're an essential part of web preservation, and I've used many of them.

Tools like [ArchiveBox], [Webrecorder], and the [Wayback Machine] have preserved enormous chunks of the web -- pages that would otherwise be lost.
I paid for a Pinboard [archiving account] for a decade, and I search the Internet Archive at least once a week.
I've used command-line tools like [wget], and last year I wrote my own tool to [create Safari webarchives][safari_webarchives].
The size and scale of today's web archives are only possible because of automation.

But automation isn't a panacea, it's a trade-off.
You're giving up accuracy for speed and volume.
If nobody is reviewing pages as they're archived, it's more likely that they'll contain mistakes or be missing essential files.

When I reviewed my old Pinboard archive, I found a lot of pages that were missing, broken, or incomplete.
These were web pages I really care about, and I thought I had them backed up, but that turned out to be a false sense of security.
I've found this sort of mistake whenever I've relied on automated tools to archive the web.

That's why I decided to create my archive manually -- it's slower, but it gives me the comfort of knowing that I have a good copy of every page.

[ArchiveBox]: https://archivebox.io/
[Webrecorder]: https://webrecorder.net/
[Wayback Machine]: https://web.archive.org/
[archiving account]: https://pinboard.in/faq/#archiving
[wget]: https://www.gnu.org/software/wget/manual/wget.html#Recursive-Download
[safari_webarchives]: /2024/creating-a-safari-webarchive/



---



<h2 id="what_i_learnt">What I learnt about archiving the web</h2>

<h3 id="defunct_services">Lots of the web is built on now-defunct services</h3>

Link rot is everywhere on the web, and I found many web pages that rely on third-party services that no longer exist, like:

*   Photo sharing sites -- some I'd heard of (Twitpic, Yfrog), others that were new to me (phto.ch)
*   Link redirection services -- URL shorteners and sponsored redirects
*   Social media sharing buttons and embeds

For many of my bookmarks, if you load the live site, the main page loads, but key resources like images and scripts are broken or missing.

One particularly insidious kind of breakage is when the service still exists, but the content has changed.
Here's an example: a screenshot from an iTunes tutorial on LiveJournal that's been replaced with an "18+ warning":

<figure style="width: calc(450px);">
  <div style="display: grid; grid-template-columns: auto auto; grid-gap: 0.5em; align-items: center;">
    {%
      picture
      filename="bookmarks/001akef1.png"
      width="78"
      class="screenshot"
      alt="Screenshot of a text box in the iTunes UI, where you can enter a year."
    %}
    {%
      picture
      filename="bookmarks/122942_original.png"
      width="300"
      alt="A warning from LiveJournal that this image is “18+”."
    %}
  </div>
</figure>

This kind of failure is hard to detect automatically -- the server returns a valid response, just not the one you want.
That's why I wanted to look at every web page with my eyes, and not rely on a computer to tell me it was saved correctly.

<h3 id="link_rot">Links rot faster than web pages</h3>

I was surprised by how many web pages still exist, but the original URLs no longer work, especially on large news sites.
Many of my old bookmarks now return a 404, but if I search for the headline, I find the story at a completely different URL.

I find this frustrating and disappointing.
Whenever I've restructured this site, I always set up redirects because I'm an old-school web nerd and I [think URLs are cool][urls] -- but redirects aren't just about making me feel good.
Keeping links alive makes your back catalogue more visible, and makes pages easier to find -- without them, most people who encounter a broken link will assume the page was deleted, and won't dig further.

[urls]: https://www.w3.org/Provider/Style/URI.html

<h3 id="lazy_loading">Images are becoming more efficient, but harder to preserve</h3>

Web developers have several techniques they can use to serve images efficiently.
These are a big win for the web overall, but the complexity makes web pages harder to preserve.

[*Lazy loading*][lazy_loading] is a technique where a web page doesn't load images or resources until they're needed -- for example, not loading an image at the bottom of an article until you scroll down.

Modern lazy loading is easy with [`<img loading="lazy">`][img_attr], but there are lots of sites that were built before that attribute was widely-supported.
They have their own code for lazy loading, and every site behaves a bit differently.
For example, a page might load a low-res image first, then swap it out for a high-res version with JavaScript.
But automated tools can't always run that JavaScript, so they only capture the low-res image.

The [*`<picture>` tag*][picture_tag] allows pages to specify multiple versions of an image.
Here are two examples:

*   A page could send a high-res image to laptops and tablets, and a low-res images to phones.
    This is more efficient; you're not sending an unnecessarily large image to a small screen.
*   A page could send different images depending on your colour scheme.
    You could see a graph on a white background if you use light mode, or on a black background if you use dark mode.

If you preserve this page, which images should you get?
All of them?
Just one?
If so, which one?
For my personal archive, I just saved the highest resolution copy of each image, but I'm not sure that's the best answer in every case.

On the modern web, pages may not look the same for everyone -- different people can see different things.
When you're preserving a page, you need to decide which version of it you want to save.

[lazy_loading]: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Lazy_loading
[img_attr]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img#loading
[picture_tag]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/picture

<h3 id="boundary">There’s no clearly-defined boundary of what to collect</h3>

Several times I found myself unsure of how much to archive.
Here are two examples:

*   Molly White's talk [*Fighting for our web*][fighting] includes an embedded YouTube video.
    I think the video is a key part of the page, so I wanted to download it -- but “download all embeds and links” would be a very expensive rule.
*   I've bookmarked blog posts that comment on scientific papers.
    I saved a local copy of the blog post and a PDF of the original paper, but I didn't try to download everything the post links to.

I made decisions about what to download on a case-by-case basis.
There's no hard rule -- it depends on the content and the context.

[fighting]: https://www.citationneeded.news/fighting-for-our-web/



---



<h2 id="conclusion">Should you do this?</h2>

Creating a web archive is a tradeoff between speed and quality.
Automated tools are fast but imperfect.
Manual archiving is slow, picky work that demands comfort with HTML, CSS, and JavaScript -- but it gives you the confidence that you've saved what matters.

It took me hundreds of hours to build my archive by hand.
Now I have over 2000 web pages saved in a stable format, and the comfort of knowing that I have a good copy of every page.
I'm very glad to have done it, but it's such a time commitment that I can't recommend that everybody do this.

Instead, I'd suggest you look at automated tools.
For most people, they're a better balance of cost and reward.

As I was building my archive, and reading all these web pages, I learnt a lot about how it's built.
In part 3 of this series, I'll share what I learnt about making better websites by trying to save them.

If you'd like to know when that article goes live, [subscribe to my RSS feed or newsletter](/subscribe/)!
