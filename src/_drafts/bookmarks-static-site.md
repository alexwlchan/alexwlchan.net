---
layout: post
title: Creating a static website for all my bookmarks
summary:
tags:
  - bookmarking
  - static sites
---
I'm storing more and more of my data [as static websites][static_sites], and about a year ago I switched to using a local, static site to manage my bookmarks.
It's replaced [Pinboard] as my way to track interesting links and cool web pages.

{{screenshot}}

It’s taken hundreds of hours to get all my data and saved web pages into this new site, and I’ve learnt a lot about archiving and building the web.
This post is the first of a four-part series about my bookmarks, explaining how this site worked.

1.  Creating a static website for all my bookmarks
2.  Creating a local archive of all my bookmarks
3.  Learning how to make websites by reading two thousand web pages
4.  Some cool websites from my bookmark collection

[static_sites]: /2024/static-websites/
[Pinboard]: https://pinboard.in

## Why do I bookmark?

I bookmark because I want to be able to find links later.

Having my own list is easier than trying to find a remembered web page on the entire Internet – web pages rot, links break, and a lot of the pages I read aren’t indexed by Google. (Paywalled content and fanfiction are the two big examples.)

My bookmarks are also a place to write down notes on why I thought a particular link was interesting.

((Expand? Example?))

## Why use a static website?

I was a happy [Pinboard] customer for over a decade, but the site feels a bit abandoned. I’ve not had catastrophic errors, but I kept running into broken features or rough edges – search timeouts, unreliable archiving, unexpected outages. There does seem to be some renewed activity in the last few months, but it was too late – I’d been looking for an exit route, and I’ve already moved to a static site.

I can write my own static bookmarks site because my needs are pretty simple – I just want a list of links, some basic filtering and search, and a saved copy of all my links. Pinboard has a lot of social features and external integrations that I never used, so I don’t miss them with my local site.

I’ve been using static sites for all sorts of data, and I’m enjoying the flexibility and portability of vanilla HTML and JavaScript. They need minimal maintenance and there’s no lock-in, and I’ve made enough of them that I can create new ones pretty quickly.

## A guided tour

The main page is a scrolling list of all my bookmarks. This is a single page that shows every link – I have about 2,500 bookmarks, which is sufficiently small that it fits on a single page. Each bookmark has a title, a URL, a short description that I wrote, and a list of tags.

{screenshot}

If I’m looking for a specific bookmark, I can filter by tag, multiple tags, or I can use my browser’s in-page search feature. I can sort by title, date saved, or “random” – this is a fun way to find links I might have forgotten about.

Let's look at a single bookmark:

{screenshot}

Links are blue, underlined and URLs are visible. Call me old-fashioned, but I still care about URL design, I think underlined links are cool, and I have nostalgia for blue links.

Clicking the URL takes me to the original page live on the web, but clicking the title takes me to a local snapshot of the page. Because links can rot, and these are the links I care about most, I’ve saved a local copy of every page as a mini-website – an HTML file and supporting assets. The main link is to these local snapshots first because they’re guaranteed to be present, and they work offline.

{comparison screenshot}

This is something I can only do because this is a personal tool – if a commercial bookmarking website tried to direct traffic to their self-hosted snapshots rather than the original site, they’d be hit with a lawsuit about “stealing traffic”.

Creating these archival copies took hundreds of hours, and I’ll discuss it more in parts 2 and 3 of this series.

## How it works

This is a static website building using the pattern I described in {making websites}

I'm not going to share the code for this site, because it’s scrappy, poorly-documented, and heavily intertwined with the bookmarks themselves. If you want to build something like this yourself, reading my tutorial will be more helpful.

This is the model I’m using to store the bookmarks in the metadata file:

```json
{
    "url": "https://www.recurse.com/social-rules",
    "title": "Recurse Center\u2019s Social Rules",
    "description": "A good set of rules for a learning environment, with more specifics than just \u201cbe nice to each other\u201d. In particular: <blockquote><p>The social rules are:</p><ul><li>No well-actually\u2019s</li><li>No feigned surprise</li><li>No backseat driving</li><li>No subtle -isms</li></blockquote>",
    "date_saved": "2025-03-03T01:26:08Z",
    "tags": ["interpersonal skills"],
    "archive": {
      "path": "archive/r/recurse.com/social-rules.html",
      "asset_paths": [
        "archive/r/recurse.com/static/bem_public-5bce60dd565cb02c926cda010e6601bc70d8377272fc005c0c8a475a24a20ca1.css",
        "archive/r/recurse.com/static/fontawesome-webfont-32595182c018a4d09f6ad3ec4350a7df1a7c38c30b75249c2cb3bd3a41f50325.woff2",
        "archive/r/recurse.com/static/kmKhZrc3Hgbbcjq75U4uslyuy4kn0qNcWxEQDO-Wyrs.woff2",
        "archive/r/recurse.com/static/kmKnZrc3Hgbbcjq75U4uslyuy4kn0qNZaxMaC82U.woff2",
        "archive/r/recurse.com/static/libre_baskerville.css",
        "archive/r/recurse.com/static/public-4a842b53badb4112f57f76c827e2485b0ca9606bfffea0564f626edbfbea88e2.js"
      ],
      "saved_at": "2025-03-03T01:30:23Z"
    }
```

Most of the model is based on how my bookmarks were described in the Pinboard API, which in turn came from an even older site called Delicious. I’ve considered breaking out some of the data into separate fields (say, publication year), but for now I want to keep it simple!

The `archive` object is new – that’s my local snapshot of a page. The `path` is the HTML file at the root of the snapshot, and then `asset_paths` is a list of any other files that get used in the webpage (CSS files, images, fonts and so on). Then I can check that every saved file is associated with at least one bookmark.

When I want to add a bookmark or make changes, I open the JSON in my text editor and make changes by hand. I have a script that checks the file is properly formatted and the archive paths are all correct, and I track changes to the metadata file in Git.

Now you know how my new bookmarking site works. In part 2, I’ll explain how I created local snapshots of nearly 2,500 web pages. In part 3, I’ll tell you everything I learnt about building web pages from building that archive.