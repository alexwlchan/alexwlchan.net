---
layout: post
date: 2014-06-13 00:03:00 +0000
title: Some site updates
---

If you visit the site regularly, you'll have noticed that things have changed quite a lot recently.
I've been meaning to write about what I've done, but revision has been getting in the way.
Since my exams finished last week, I've finally been able to take time to write everything down.

<!-- summary -->

## The move to Pelican

The biggest visual change is the new design, which is tied to a big change in how the site is built.

The first version of this site was generated with [Octopress][oc], a static blogging engine written in Ruby.
I really liked Octopress, but it just wasn't for me.
I also don't really use Ruby, so my installation is frequently out-of-date or broken, which meant I had to fix that before posting to the site.

As a side project during exam revision, I decided to look at static blogging engines written in Python (which I use on a regular basis, so I always have a working installation).
I eventually settled on [Pelican][pel], which is fairly lightweight and suits my needs well.
As a bonus, it was able to import the Markdown files from my original posts, so everything from the first site carried over near seamlessly.

When I rewrote the site, I also tried to refresh the design.
I started with Giulio Fidente's [svbhack theme][svb], and then tweaked until I found a design I was happy with.
I made most of the text reader, removed the sidebar, and added this charming shade of red.
I think the new design is much cleaner and lighter than the previous site.

At the same time, I switched from using Heroku to using GitHub Pages for hosting the site.
I wasn't unhappy with Heroku; I just found it easier to set up Pelican on GitHub than try to reproduce my existing Heroku setup.
As a side effect, a copy of this site is now available as [a GitHub repo][awlc].

## Working DNS. Finally.

I prefer URLs that don't include the `www` prefix.
I don't have a good reason; I just think they look nicer.

So when I uprooted the entire site, I tried to drop the `www` prefix from my URLs, but the change didn't go smoothly.
I didn't configure my DNS records correctly, so for a long time `www.alexwlchan.net` URLs would simply fail to resolve.
I think I've finally fixed this mistake, so it shouldn't matter whether you include the `www` prefix or not.

## Google Analytics

I decided to install Google Analytics about a month ago, but I didn't include a privacy policy or any disclosure on this site.
That's a breach of their [Terms and Conditions][t&c] (section&nbsp;7), but it also feels dishonest.
Especially given the recent discussions about privacy in the context of mysterious Government agencies, I feel bad that I was collecting this information without any form of disclosure.
I'm sorry for the mistake.

I've written a [privacy policy][pp] for the site.
This is linked in the footer of every page, and also on the site's "About" page.

[oc]: http://octopress.org
[pel]: http://pelican.readthedocs.org/en/3.3.0/
[awlc]: https://github.com/alexwlchan/staticsite
[t&c]: http://www.google.co.uk/analytics/terms/us.html
[pp]: http://alexwlchan.net/privacy/
[svb]: https://github.com/giulivo/pelican-svbhack
