---
layout: post
title: Taking scheduled screenshots of my website
summary: |
  A screenshot a day keeps the bit rot at bay.
tags:
  - screenshots
  - digital-preservation
colors:
  index_light: "#3d3d36"
  index_dark:  "#d4d5d2"
---

A few weeks ago I was reading the [DPC Bit List][bitlist], an inventory of digital materials and the risks associated with their long-term preservation.
What formats need urgent attention before they're lost forever, what mediums are already being well-preserved, that sort of thing.
For example, Adobe Flash animations are "practically extinct", while emails are merely "endangered".

[bitlist]: https://www.dpconline.org/digipres/champion-digital-preservation/bit-list

Something that struck me is how the Bit List treats the content and interface of online services as two separate concerns.
Most preservation efforts have focused on saving the *content* -- the photos, videos, and text that we upload to the web.
We don't have as many records of the *interfaces* -- the "look and feel" of these sites.
But if you only save one and not the other, you're losing a lot of important context about how we used those sites, and how their design influenced the content.

One example that springs to mind is TikTok.
It popularised the use of vertical swiping to move between videos, and that design makes it easy for users to watch a continuous stream of videos.
It's very effective at keeping people in the app, and it's been copied by lots of other services.

This user interface is behind concerns about the addictive nature of TikTok, because it requires minimal effort to stay in the app and watch another video.
It's also affected how videos are made, because creators need to capture your attention quickly before you swipe to watch something else.
Popular videos on TikTok look different to those on YouTube, on television, or in cinema.

You can't understand TikTok or its effect on the world without understanding this interface.

But preserving the interface of an app or website is hard, and there are no good options.

---


Ideally you'd preserve a working copy of an app, but that's really hard -- you'd have to emulate the computing environment that the app runs in, including any remote services that it relies on.
And then you have to decide what version you're preserving.
Interfaces are constantly changing as companies tweak things, add new features, try to find ways to get even more of our attention.
There is no "one" interface

Preserving static files is comparatively easy and well-understood, and

---

Preserving the interface is a super interesting question for another time, because there is no “one” Flickr interface; it's changing all the time as the company tweak things, add new features, fix bugs, and so on.


---

How to save look and feel?
It's hard!

One way is screenshots
Wrote about this a few years ago
Good tradeoff of effort and benefit
A static screenshot or screen recording isn't as good as a fully working copy of the software, but it's much easier to make and preserve

A PNG screenshot can be opened on pretty much any modern computing device
Environments for emulating old software are much harder to build, maintain and run

at the same time as I was reading this, was doing some design work on this website
I don't tend to do "big bang" redesigns here, more gradual tweaks and improvements
wasn't until I was done that I realised I'd forgotten to take before/after screenshots
oops

lightbulb moment

time for automation!
what if you took a screenshot of a website every day?
or eevry week?

---

I had a vague idea of how to take screenshots programatically; use Playwright
headless browser for testing
used for automated tests at previous job

can take a single screenshot:

```console
$ npm install playwright-chrome
$ npx playwright screenshot --full-page "alexwlchan.net" "screenshot.png"
```

next need to run that on a schedule

https://simonwillison.net/2020/Oct/9/git-scraping/

> We already have a great tool for efficiently tracking changes to text over time: Git. And GitHub Actions (and other CI systems) make it easy to create a scraper that runs every few minutes, records the current state of a resource and records changes to that resource over time in the commit history.

basic technique fits in a single GitHub Actions workflow:
if you wanted to customise, only need to change two env vars

```yaml
name: Take screenshot

on:
  schedule:
    - cron: '7 7 * * 1'  # Every Monday at 7:07am UTC

jobs:
  take-screenshot:
    runs-on: macos-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Take screenshot
        run: |
          npm install playwright-chrome
          
          today=$(date +"%Y-%m-%d")
          screenshot_path="screenshots/$SCREENSHOT_NAME.$today.png"
          
          mkdir -p "$(dirname "$screenshot_path")"
          
          npx playwright screenshot --full-page "$URL" "$screenshot_path"

          git add --all
          git commit -m "Add screenshots for $today" || exit 0
          git push origin main
        env:
          URL: alexwlchan.net
          SCREENSHOT_NAME: alexwlchan.net
```

pretty compact!

run once a week is a good fit for me -- this site doesn't change that often and avoids the size of the repo exploding

I run a slightly modified version of this backing up two websites (my main site and my book tracker) in scheduled-screenshots repo on GitHub.

template GitHub repo

---

great for new screenshots, what about old ones?

decided to dive into Wayback Machine to backfill
this site isn't enormously popular so isn't indexed that often

cf my site (148 captures of homepage between April 2013 and today)
and front page of nytimes.com (228 snapshots yesterday alone)

get list of captures / take screenshot

surprising how many holes there were
of 116 captures of my book tracker:

* 13 were obviously broken – the CSS or images hadn't been saved, so the page is broken
* 7 are broken in subtle ways -- for reasons I don't fully understand, archived HTML + modern CSS

wow!
Wayback machine is great, but no substitute for proper archiving of content

https://twitter.com/dannybirchall/status/1628700356484952066 (23 Feb 2023):

> "It's in the wayback machine" is an excuse to cover the most basic dereliction of duty in looking after an organisation's history and legacy.

but I backfilled as best I could

---

where to get code?
and template repo?