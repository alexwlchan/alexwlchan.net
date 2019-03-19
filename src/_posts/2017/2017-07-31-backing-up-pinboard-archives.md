---
layout: post
date: 2017-07-31 19:47:00 +0000
summary: A Rust utility for saving local copies of my full-page archives from Pinboard.
tags: rust pinboard
title: Backing up full-page archives from Pinboard
category: Programming and code
---

Several years ago, I blogged about [a Python script][python] I'd written to back up my Pinboard bookmarks.
I've been using Pinboard since then -- a brief homebrew solution aside -- and recently, I wanted to turn my attention to my archival account.

[python]: /2013/03/pinboard-backups

As well as storing a list of pages you've saved, you can pay [a small annual fee][upgrade] and Pinboard will save a complete copy of the pages you bookmark.
This helps keep your bookmarks useful in the face of link rot -- when pages change, or even disappear completely.
Pages break surprisingly quickly -- Maciej did [some informal research][link_rot] on link rot a few years back, and even that post itself has now broken.
Around 15% of my bookmarks no longer go anywhere useful.

[upgrade]: https://pinboard.in/upgrade/
[link_rot]: http://web.archive.org/web/20170707013231/https://blog.pinboard.in/2011/05/remembrance_of_links_past/

Once a page is archived, it appears with a small grey checkmark next to the link -- so you easily view the archived page if the original goes away.

<figure style="max-width: 388px;">
  <img src="/images/2017/pinboard_archive.png">
</figure>

I've paid for the extra archiving for years, and having these complete backups of my bookmarks is great -- but they only live on Pinboard.
What if Pinboard gets acquired, or Maciej wipes the servers and runs off to Mexico?
I really want a local backup of all these full-page copies.

<!-- summary -->

In the archival account of your Pinboard settings, you can ask for a backup download:

<figure style="max-width: 628px;">
  <img src="/images/2017/archive_backup.png">
</figure>

But in practice, when it says "an hour", I've found it takes days or weeks to materialise, if at all.
(I think there's a manual step in the process, so somebody at Pinboard&nbsp;HQ has to be available.)
But the archives are all available when I'm logged in to Pinboard, so maybe I could download them from there?

I've written a small Rust utility that downloads all the archived pages from an account.
You can find the source code and installation instructions [on GitHub][github].
It's a bit janky and poorly commented -- but it basically works.

[github]: https://github.com/alexwlchan/backup-pinboard

In a nutshell: it logs on to Pinboard, gets a list of all your archive pages by scraping the site, then downloads local copies of each page.
It does incremental backups, only fetching pages which are new or changed since the last run.
This means the first attempt takes quite a while to run (about an hour for my 3000&nbsp;bookmarks), but subsequent runs are pretty fast.

It's long enough that I don't have time to write a complete breakdown, but here are a few things that were technically interesting:

*   I've been using more Rust for small projects like this because the tooling is *so* good.
    Cargo makes it easy to build and install a project on a new machine.
    If I used Python, I'd have to muck around with versions and virtualenvs and pip -- nothing I haven't done before, but a small annoyance that it's nice to avoid.
    Even though I'm slower at writing code in Rust, the experience is so much nicer.

*   One big frustration with Rust is the small number of third-party libraries.
    I really missed [Beautiful Soup][soup], an HTML parsing library for Python.
    I couldn't find an equivalent Rust library, so I just parsed the Pinboard HTML with regular expressions.
    [Generally unwise][html], but the Pinboard page layout changes very infrequently (if ever), so I reckon I'm safe in this case.

*   Rust *does* have a port of [docopt][docopt], which is a fantastic library in any language.
    I don't know how argument parsing in Rust works, and I don't need to.
    I wrote the help string, defined a struct for the arguments, and the heavy lifting was done for me.

*   The Pinboard archiver grabs all the assets for a page -- images, CSS, JavaScript, and so on -- and it would be nice to copy those locally.
    For this part, I turned to [wget][wget].

    Back when I was briefly running my own Pinboard clone, I discovered that wget has a lot of nice options for saving pages -- including the `--page-requisites` flag, which downloads the supporting assets.
    (I can't be sure, but I'd be unsurprised if Pinboard uses wget.)

    I'm invoking wget by shelling out with `std::process::Command`, which probably isn't ideal.
    If I had more time, I might investigate binding to libwget, and pulling it into the binary -- but I've already wasted plenty of time shaving this yak.

[soup]: https://www.crummy.com/software/BeautifulSoup/
[html]: https://stackoverflow.com/a/1732454/1558022
[wget]: https://www.gnu.org/software/wget/
[docopt]: http://docopt.org/

Now I've got this working, I have it running as a cron job on my home Mac.
Voila: a local copy of my Pinboard archives, which then get passed around my other backup systems.
I'm not so fussed about exactly where they go once they're local -- I just don't want the only copy of them to be on Pinboard.
