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

One thing that struck me is how the Bit List treats the content and interface of online services as two separate concerns.
Most preservation efforts have focused on saving the *content* -- the photos, videos, and text that we upload to the web.
We don't have as many records of the *interfaces* -- the "look and feel" of these sites.
But if you only save one and not the other, you're losing a lot of important context about how we used those services, and how their design influenced the content.

---

Reading DPC Bit List

> * **The Bit List splits out the interfaces and data in online services as separate concerns.** Data Lifeboat addresses one but not the other; we aren’t doing anything to save the “look and feel” of Flickr.com. Preserving the interface is a super interesting question for another time, because there is no “one” Flickr interface; it's changing all the time as the company tweak things, add new features, fix bugs, and so on.

P21:

> Without the interfaces and underlying software that enables social media platforms, it will be impossible to preserve the look and feel and even meaning of a large portion of content that depends on particular functionality or interface to be accurately or authentically interpreted, including for evidential uses, art works, design research, and historical / qualitative research. The loss of these interfaces (or lack of any indication of robust documentation by platforms) means a significant gap in the cultural heritage of many communities and even entire nations. For example, some content creators on YouTube may lose access to their content and accounts due to copyright infringement claims or reports of inappropriate content, which may or may not be supportable. The risk of loss is higher if the content is not stored anywhere else. Though some mitigation methods are available through the platform, this issue may only affect a small number of accounts.
>
> Some of the content/iterations of these are likely preserved to an extent within existing web archives but not as targeted collection efforts. As we've seen with myspace and other platforms where the platform producers decide to remove content or shut down rather quickly, it can be too late if this content has not been preserved already.
>
> The authenticity of displaying social media content from 2014 through modern interfaces is questionable, and without recording the interface at the time, it is not currently possible to recreate older interfaces. You'd think the platform owners would have the older versions saved, but these are not available at the moment, and it would be worth engaging in a conversation about making them available to cultural heritage institutions for display purposes.

obvious example that springs to mind is TikTok
the vertical swiping has changed how we watch videos, and the sort of videos that are made

preserving the videos without that context will make it harder for people to understand what's going on
(I associate vertical swiping with TikTok, yet the word "swipe" doesn't appear in the Wkipedia page – or any otjher mention of vertcial video or desc of UI)


ChatGPT

> TikTok did not invent vertical swiping, but it certainly popularized the format for content consumption on mobile devices, particularly for video content. Vertical swiping as a navigation gesture has been around in mobile interfaces for a while, being used in various applications and operating systems to scroll through pages, lists, and other content.
>
> However, TikTok, which started gaining international traction around 2017-2018, utilized vertical swiping in a novel way as the primary interaction method for moving between videos. This user interface design proved highly effective for keeping users engaged and making it easy for them to consume a continuous stream of video content. This approach has since been adopted and adapted by many other social media and content platforms, making vertical swiping a standard for browsing video content on mobile apps.

https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.932805/full

> In the context of TikTok, it had a simple operating system. The interaction was designed for immersive experiences and aimed to keep users in an extremely passive state to accept the recommended videos. Users only needed to swipe up the screen with low effort to glance at short videos, therefore, indulging TikTok and extending the usage time unconsciously (Zhao, 2021). Besides, the convergence of functions (such as integrated music, video, social, etc.) made TikTok more attractive. Users are swallowed by the fun of watching or editing short videos and even lost track of time (Liang, 2021).

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