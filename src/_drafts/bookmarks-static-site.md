---
layout: post
title: Creating a static website for all my bookmarks
summary:
  To help me keep track of interesting links, I created a static website that keeps all my data locally. Why do I care about bookmarks, and how does my new site work?
tags:
  - bookmarking
  - static sites
index:
  feature: true
colors:
  css_light: "#0000ff"
  css_dark:  "#00ddff"
---
I'm storing more and more of my data [as static websites][static_sites], and about a year ago I switched to using a local, static site to manage my bookmarks.
It's replaced [Pinboard] as my way to track interesting links and cool web pages.
I save articles I've read, talks I've watched, fanfiction I've enjoyed.

{%
  picture
  filename="bookmarks/all_bookmarks.png"
  width="500"
  class="screenshot"
  alt="Screenshot of a web page titled ‘bookmarks’, and a list of three bookmarks below it. Each bookmark has a blue link as the title, a grey URL below the title, and some descriptive text below it."
%}

It’s taken hundreds of hours to get all my data and saved web pages into this new site, and I’ve learnt a lot about archiving and building the web.
This post is the first of a four-part series about my bookmarks, and I'll publish the rest of the series over the next three weeks.

[static_sites]: /2024/static-websites/
[Pinboard]: https://pinboard.in



<blockquote class="toc">
  <p>This article is the first in a four part bookmarking mini-series:</p>
  <ol>
    <li>
      <strong>Creating a static site for all my bookmarks</strong> (this article)
      <ul>
        <li><a href="#why_bookmark">Why do I bookmark?</a></li>
        <li><a href="#why_static">Why use a static website?</a></li>
        <li><a href="#how_it_looks">What does it look like?</a></li>
        <li><a href="#how_it_works">How does it work?</a></li>
      </ul>
    </li>
    <li>
      <a href="#"><strong>Creating a local archive of all my bookmarks</strong></a> (coming 12 May) – web archiving, automated vs manual, what I learnt about saving web pages.
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



<h2 id="why_bookmark">Why do I bookmark?</h2>

### I bookmark because I want to find links later

Keeping my own list of bookmarks means that I can always find old links.
If I have a vague memory of a web page, I'm more likely to find it in my bookmarks than in the vast ocean of the web.
Links rot, websites break, and a lot of what I read isn't indexed by Google.

This is particularly true for fannish creations.
A lot of fan artists deliberately publish in closed communities, so their work is only visible to like-minded fans, and not something that a casual Internet user might find.
If I'm looking for an exact story I read five years ago, I'm far more likely to find it in my bookmarks than by scouring the Internet.

Finding old web pages has always been hard, but the rise of generative AI has made it much harder.
Search results are full of AI slop, and people are trying to hide their content from scrapers.
Locking the web behind paywalls and registration screens protects it from scrapers, but also makes it [harder to find][open_access].

[open_access]: https://www.citationneeded.news/free-and-open-access-in-the-age-of-generative-ai/

### I bookmark to remember why I liked a link

I write notes on each bookmark I keep, so I remember why a particular link was fun or interesting.

For example, I saved [Erin Kissane's talk about building networks][kissane].
It's a 25 minute talk, or about 3,500 words.
Writing a short summary helps me remember what I thought the key points were, and why I thought it was worth saving.
I can review a one paragraph summary much faster than I can reread the entire page.

When I save fanfiction, I write notes on the plot or key moments.
Is this the story where they live happily ever after?
Or does this have a gut wrenching ending that needs a box of tissues?

These summaries could be farmed out to generative AI, but I much prefer writing the summaries myself.
I can phrase them in my own words, write down connections to other ideas, and write a more personal summary than I get from a machine.
And when I read those summaries later, I remember writing them, and it revives the memories of the original article or story.
It's slower, but I find it much more useful.

[kissane]: https://erinkissane.com/xoxo



---



<h2 id="why_static">Why use a static website?</h2>

I was a happy [Pinboard] customer for over a decade, but the site [feels abandoned][abandoned].
I've not had catastrophic errors, but I kept running into broken features or rough edges -- search timeouts, unreliable archiving, unexpected outages.
There does seem to be some renewed activity in the last few months, but it was too late -- I'd already moved away.

I briefly considered Pinboard alternatives like [Raindrop], [Pocket] and [Instapaper] -- but I'd still have to trust an online service.
I've been burned too many times by services being abandoned, and so I've gradually been moving the data I care about to [static websites] on my local machine.
It takes a bit of work to set up, but now I have more control and I'm not worried about it going away.

My needs are pretty simple – I just want a list of links, some basic filtering and search, and a saved copy of all my links.
I don't need social features or integrations, which made it easier to walk away from Pinboard.

I've been using static sites for all sorts of data, and I'm enjoying the flexibility and portability of vanilla HTML and JavaScript.
They need minimal maintenance and there's no lock-in, and I've made enough of them now that I can [create new ones][howto] pretty quickly.

[Raindrop]: https://raindrop.io
[Pocket]: https://getpocket.com/home
[Instapaper]: https://www.instapaper.com
[Pinboard]: https://pinboard.in
[static websites]: /2024/static-websites/
[howto]: /2025/mildly-dynamic-websites/
[abandoned]: https://ask.metafilter.com/368202/Is-Pinboardin-bookmarking-site-still-supported-software



---



<h2 id="how_it_looks">What does it look like?</h2>

The main page is a scrolling list of all my bookmarks.
This is a single page that shows every link, because my collection is small enough that I don't need pagination.

{%
  picture
  filename="bookmarks/all_bookmarks_small.png"
  width="400"
  class="screenshot"
  alt="Screenshot of a web page titled ‘bookmarks’, and a list of three bookmarks below it. Each bookmark has a blue link as the title, a grey URL below the title, and some descriptive text below it."
%}

Each bookmark has a title, a URL, my hand-written summary, and a list of tags.

If I'm looking for a specific bookmark, I can filter by tag or by author, or I can use my browser's in-page search feature.
I can sort by title, date saved, or "random" -- this is a fun way to find links I might have forgotten about.

Let's look at a single bookmark:

{%
  picture
  filename="bookmarks/single_bookmark.png"
  width="600"
  class="screenshot"
  alt="Close-up view of a single bookmark."
%}

The main title is blue and underlined, and the URL of the original page is shown below the title.
Call me old-fashioned, but I still care about URL design, I think it's cool to underline links, and I have nostalgia for #0000ff blue.

If I click the URL in grey, I go to the page live on the web.
But if I click the title, I go to a local snapshot of the page.
Because links can rot, and these are the links I care about most, I've saved a local copy of every page as a mini-website -- an HTML file and supporting assets.
The title link is to these local snapshots, because they're guaranteed to be present, and they work offline.

This is something I can only do because this is a personal tool.
If a commercial bookmarking website tried to direct users to their self-hosted snapshots rather than the original site, they'd be hit with a lawsuit about "stealing traffic".

Creating these archival copies took months, and I'll discuss it more in parts 2 and 3 of this series.



---



<h2 id="how_it_works">How does it work?</h2>

This is a static website building using the pattern I described in [How I create static websites for tiny archives].
I have my metadata in a JavaScript file, and a small viewer that renders the metadata as an HTML page I can view in my browser.

I'm not sharing the code because it's deeply personalised and tied to my specific bookmarks, but if you're interested, that tutorial is a good starting point.

Here's an example of what a bookmark looks like in the metadata file:

```
"https://notebook.drmaciver.com/posts/2020-02-22-11:37.html": {
  "title": "You should try bad things",
  "authors": [
    "David R. MacIver"
  ],
  "description": "If you only do things you know are good, eventually some of them will fall out of favour and you'll have an ever-shrinking pool of things.\r\n\r\nSome of the things you think will be bad will end up being good \u2013 trying them helps expand your pool.",
  "date_saved": "2024-12-03T07:29:10Z",
  "tags": [
    "self-improvement"
  ],
  "archive": {
    "path": "archive/n/notebook.drmaciver.com/you-should-try-bad-things.html",
    "asset_paths": [
      "archive/n/notebook.drmaciver.com/static/drmnotes.css",
      "archive/n/notebook.drmaciver.com/static/latex.css",
      "archive/n/notebook.drmaciver.com/static/pandoc.css",
      "archive/n/notebook.drmaciver.com/static/pygments.css",
      "archive/n/notebook.drmaciver.com/static/tufte.css"
    ],
    "saved_at": "2024-12-03T07:30:21Z"
  },
  "publication_year": "2020",
  "type": "article"
}
```

I started with the data model from the [Pinboard API], which in turn came from an older bookmarking site called [Delicious].
Over time, I've added my own fields.
Previously I was putting everything in the title and the tags, but now I can have dedicated fields for things like authors, word count, and fannish tropes.

The `archive` object is new – that's my local snapshot of a page.
The `path` points to the main HTML file for the snapshot, and then `asset_paths` is a list of any other files that get used in the webpage (CSS files, images, fonts and so on).
I have a Python script to checks that every archived file has been saved properly.

This is another advantage of writing my own bookmarking tool -- I know exactly what data I want to store, and I can design the schema to fit.

When I want to add a bookmark or make changes, I open the JSON in my text editor and make changes by hand.
I have a script that checks the file is properly formatted and the archive paths are all correct, and I track changes in Git.

Now you know what my new bookmarking site looks like, and how it works.
Over the next three weeks, I'll publish the remaining parts in this series.
In part 2, I'll explain how I created local snapshots of every web page.
In part 3, I'll tell you what that process taught me about building web pages.
And in part 4, I'll highlight some fun stuff I found as I went through my bookmarks.

If you'd like to know when those articles go live, [subscribe to my RSS feed or newsletter](/subscribe/)!

[How I create static websites for tiny archives]: /2025/mildly-dynamic-websites/
[Pinboard API]: https://pinboard.in/api/
[Delicious]: https://en.wikipedia.org/wiki/Delicious_(website)

