---
layout: post
date: 2024-04-23 08:16:35 +0000
title: Taking regular screenshots of my website
summary: |
  A screenshot a day keeps the bit rot at bay.
tags:
  - screenshots
  - digital preservation
colors:
  index_light: "#3d3d36"
  index_dark:  "#d4d5d2"
---

A few weeks ago I was reading the [<abbr title="Digital Preservation Coalition">DPC</abbr> Bit List][bitlist], an inventory of digital materials and the risks associated with their long-term preservation.
What formats need urgent attention before they're lost forever, what mediums are already being well-preserved, and so on.
For example, Adobe Flash animations are "practically extinct", while emails are merely "endangered".

Something that struck me is how the Bit List treats the content and interface of online services as two separate concerns.
Most preservation efforts focus on saving the *content* -- the photos, videos, and text that we upload to the web.
We don't have as many records of the *interfaces* -- the "look and feel" of these sites.
But if you only save one and not the other, you're losing a lot of important context about how we use those sites, and the influence of their designs.

One present-day example is TikTok.
It popularised the use of vertical swiping to move between videos, and that design makes it easy for users to watch a continuous stream of content.
It's very effective at keeping people in the app, and it's been copied by lots of other services.
Although it seems well-known and obvious to us today, it'll be easy to forget the novelty and impact of this idea as social media continues to evolve.

This user interface is behind concerns about the addictive nature of TikTok, because it requires minimal effort to stay in the app and watch another video.
It's also affected how videos are made, because creators need to capture your attention quickly before you swipe to watch something else.
Popular videos on TikTok look different to those on YouTube, on television, or in cinema.

You can't understand TikTok or its effect on the world without understanding this interface.
Watching a single TikTok video in an isolated player isn't the same as experiencing it in the app.

This distinction between content and interfaces got me thinking about how you preserve user interfaces.
One challenge is that most user interfaces don't have a single version.
Designs are constantly changing as companies add features, fix bugs, and try to find new ways to get more of our attention.
Even if you put aside the technical issues, we can only really preserve snapshots of how a service looked at a particular point in time.

One way to create these snapshots is with [screenshots or screen recordings][screenshots].
I think they represent a good tradeoff of effort and preservation value.
A static screenshot isn't as complete as a fully interactive, working copy of a thing, but it's much easier to create, to preserve, and to access later.
It records the look, if not the feel.

I was mulling over this for a while, and I had an idea.
I like having a set of screenshots as a visual history of the stuff I've worked on (including this site), but I'm not very good at remembering to create them.
I just finished a bunch of design tweaking on this site, and I completely forgot to take a screenshot of what it looked like before I started making changes.

Computers are pretty good at doing things on a repetitive schedule -- wouldn't it be nice if I could automate taking these screenshots?
What if a computer took a screenshot of my website every month?
Or every week?
Or every day?

[bitlist]: https://www.dpconline.org/digipres/champion-digital-preservation/bit-list
[screenshots]: /2022/screenshots/

---

I already had a vague idea of how to take screenshots programatically.
At my last job we used [Playwright] as a way to do end-to-end testing of our websites.
Playwright is a library for automating web browsers -- for example, you can use it to open a website in Chromium, click buttons, check the page loads correctly, and so on.

It can also take a screenshot of a web page, like so:

```console
$ npm install playwright
$ npx playwright install chromium
$ npx playwright screenshot --full-page "alexwlchan.net" "screenshot.png"
```

This installs Playwright, then opens my website in Chromium and takes a screenshot of the page.
The `--full-page` flag ensures the image contains the entire scrollable page, as if you had a tall screen and could fit the whole page in view without scrolling.

Once I knew how to take a screenshot once, I wanted to do it on a regular schedule, and save those images somewhere.
There are lots of ways to run code on a schedule; I decided to use [GitHub Actions] because it's what I'm familiar with.

My code for taking scheduled screenshots is entirely contained in a single GitHub Actions workflow.
It's in a file called [`.github/workflows/take_screenshots.yml`](https://github.com/alexwlchan/scheduled-screenshots/blob/a5c836cfcc6a3729fe53db97b34d116949fba377/.github/workflows/take_screenshots.yml), and it's only 79 lines:

```yaml
{% raw %}name: Take screenshots

on:
  push:
    branches:
      - main

  schedule:
    - cron: '7 7 * * 1'  # Every Monday at 7:07am UTC

jobs:
  take-screenshots:
    runs-on: macos-latest

    strategy:
      matrix:
        include:
          - url: alexwlchan.net
            filename_prefix: alexwlchan.net
          - url: books.alexwlchan.net
            filename_prefix: books

      # Setting max-parallel ensures that these jobs will run in serial,
      # not parallel, so we don't have conflicting tasks trying to
      # push new commits.
      max-parallel: 1

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

        with:
          # Check out the latest version of main, which may not be the
          # commit that triggered this event -- jobs in this workflow will
          # push new commits and update main, and we want each job to
          # get the latest code from main.
          ref: main

          # Make sure we don't download the existing screenshots as part
          # of this process -- this Action is strictly append-only, so
          # don't waste limited LFS bandwidth on it.
          lfs: false

      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install Playwright and browser
        run: |
          npm install playwright
          npx playwright install chromium

      - name: Take screenshot
        run: |
          today=$(date +"%Y-%m-%d")
          screenshot_path="screenshots/${{ matrix.filename_prefix }}.$today.png"

          # Make these variables available to subsequent steps
          # See https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-environment-variable
          echo "today=$today" >> "$GITHUB_ENV"
          echo "screenshot_path=$screenshot_path" >> "$GITHUB_ENV"

          mkdir -p "$(dirname "$screenshot_path")"

          # If there's already a screenshot for today, don't
          # bother overwriting it.
          if [[ -f "$screenshot_path" ]]; then exit 0; fi

          npx playwright screenshot \
            --full-page \
            --wait-for-timeout 10000 \
            "${{ matrix.url }}" "$screenshot_path"

      - name: Push changes to GitHub
        run: |
          git add "$screenshot_path"
          git commit -m "Add screenshot for ${{ matrix.url }} for $today" || exit 0
          git push origin main{% endraw %}
```

This runs once a week on Monday mornings -- I don't update my websites that often, so I don't need more frequent screenshots.

It installs Playwright, and uses it to take screenshots of two websites: `alexwlchan.net` (this site) and `books.alexwlchan.net` (my book tracker).
The images are saved in a folder called `screenshots`, and the filenames include both the name of the site and the date taken, e.g. `alexwlchan.net.2024-04-22.png` or `books.2024-03-21.png`.

If I want to get screenshots of a different website, I can add to the list in the `matrix` section.

I had to add a timeout to Playwright (`--wait-for-timeout 10000`) to ensure it downloads all the images correctly.
Before I added that option, I'd sometimes get screenshots with holes where the images hadn't loaded in time.

Once the screenshot has been created, it gets committed to Git and pushed to GitHub.
I had to tweak the [GITHUB_TOKEN permissions] to allow GitHub Actions to push commits to my repo.
This is inspired by Simon Willison's ["git scraping" technique][git_scraping], but I'm tracking images rather than text.

Because PNG files can get quite big and I have a lot of them, I decided to use [Git Large File Storage (LFS)][git_lfs] with this repo -- vanilla Git can struggle with large binary files.
This is my first time using Git LFS, and it was pleasantly easy to set up following the [Getting Started guide](https://git-lfs.com/):

```console
$ brew install git-lfs
$ git lfs install

$ cd ~/repos/scheduled-screenshots

$ git lfs track "*.png"
$ git add .gitattributes
$ git commit -m "Add .gitattributes file to store PNG images in Git LFS"
```

And that's what it took to set up scheduled screenshots.
If you want to see the code in a repo, or see the growing collection of screenshots, the GitHub repo is [alexwlchan/scheduled-screenshots].

[Playwright]: https://playwright.dev/
[GitHub Actions]: https://github.com/features/actions
[git_lfs]: https://git-lfs.com/
[alexwlchan/scheduled-screenshots]: https://github.com/alexwlchan/scheduled-screenshots
[git_scraping]: https://simonwillison.net/2020/Oct/9/git-scraping/
[GITHUB_TOKEN permissions]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-default-github_token-permissions

---

This is great for creating new screenshots, but what about everything that came before?
This site is nearly 12 years old, and it'd be nice for that to be reflected in the visual record.

I dove into the Wayback Machine to backfill the old screenshots.
My site isn't indexed that often -- on average about once a month -- but I can fill in some of the gaps this way.
First I used the Wayback Machine's [CDX Server API][cdx] to get a list of captures, then I [used Playwright] to take screenshots.
I had to adjust the timeouts to make sure everything loaded correctly, but I got them all to work eventually, and I got a hundred or so historical screenshots.

I was surprised by was how many issues I found.
There were 116 captures of [my book tracker], and of those 13 were clearly broken -- the CSS or images hadn't been saved, and so the page was unstyled or had gaps where the images were meant to go.

A further 7 were broken in subtle ways, where the HTML and CSS didn't match.
For example, I found one HTML capture [from 2021] that's loading CSS from 2024.
The Wayback Machine shows you a working page, but it's a hallucination -- that's not what the page looked like in 2021.
(The rounded corners are a dead giveaway -- I didn't add those until 2022.)

I love the Wayback Machine and I think it's a great service, but you shouldn't rely on it to preserve your website.
I'm glad these captures exist exist, but they're a bit shaky as a preservation record.
If there's a website you care about, make sure you have your own system that saves the stuff you think is important -- don’t just rely on the Wayback Machine.

[from 2021]: https://web.archive.org/web/20210625222812/https://books.alexwlchan.net/
[cdx]: /til/2024/get-a-list-of-captures-from-the-wayback-machine/
[used Playwright]: /til/2024/take-a-wayback-machine-screenshot/
[my book tracker]: https://books.alexwlchan.net/

---

{%
  picture
  filename="scheduled-screenshots.png"
  width="750"
  alt="A graphic showing multiple screenshots arranged into a stack, as if they were in a timeline – older screenshots towards the back, newer screenshots towards the front"
%}

My scheduled screenshots are now up and running, and every Monday I'll get a new image to record the visual history of this site.

If you want to set up something similar for your websites, here are the steps:

1.  Create a new GitHub repository
2.  Create a new file `.github/workflows/take_screenshots.yml` with the contents of the YAML file earlier in this post
3.  Give [write access] to the GITHUB_TOKEN used by GitHub Actions, so it can push to your repo
3.  Change the list of URLs/filename prefixes in the `matrix` block for the websites you want to screenshot

The best time to start taking regular screenshots of my website was when I registered the domain name.
The second best time is now.

[write access]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-default-github_token-permissions
