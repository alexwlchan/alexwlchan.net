---
layout: page
title: About the site
summary: How I build the site, the tech underneath it, and my history of questionable design decisions.
---

This site has been through several incarnations.
It's always been a static site, but the choice of generator has changed several times.

The first version, which I posted in late 2012, was built with [Octopress][octopress].
Maintaining a working Ruby setup for Octopress was a lot of hassle, so a year or so later I switched to the Python-based [Pelican][pelican].
That worked fairly well, but [the AGPL and licensing issues][agpl] always loomed overhead.
In 2016, I experimented with writing my own site generator (called [Hot Chocolate][cocoa]), but I just spent a lot of time reinventing wheels.

[octopress]: http://octopress.org/
[pelican]: https://blog.getpelican.com/
[agpl]: https://github.com/getpelican/pelican/issues/1397
[cocoa]: https://pypi.org/project/hotchocolate/

The current version is back to Ruby and [Jekyll][jekyll], but wrapped in Docker to simplify the day-to-day build process.
What you see today is powered by:

*   [Jekyll][jekyll], for building the HTML
*   [Sass][sass], for building the CSS and stylesheets
*   [nginx][nginx], an HTTP server
*   [Cloudflare][cloudflare], a CDN/caching layer
*   [Docker][docker], which wraps the local build process and nginx on my server
*   [Travis CI][travis], which builds and publishes the site
*   [Linode][linode], who provide the Linux server where I run nginx (referral link)

and all the site source code is on [GitHub][github].

Between the Wayback Machine and my screenshots, I've put together a short visual history of what the site used to look like.
Feast your eyes on my evolving skills in mediocre web design.

[jekyll]: https://jekyllrb.com/
[sass]: https://sass-lang.com/
[nginx]: https://nginx.org/
[cloudflare]: https://www.cloudflare.com/
[docker]: https://www.docker.com/
[travis]: https://travis-ci.org/alexwlchan/alexwlchan.net
[linode]: https://www.linode.com/?r=ba2e6ce21e0c63952a7c74967ea0b96617bd44a3
[github]: https://github.com/alexwlchan/alexwlchan.net/

<style>
  img {
    border: 3px solid #ccc;
  }
</style>

## Current

This is what the current homepage looks like:

![](/images/site_current.png)

## Late 2014: The first red stripe

Unsatisfied with the bubbly menu in the previous design, I did another version of the site that added a red stripe across the top.
I've tweaked this design quite a bit since the first version --- the stripe became a less orangey red, I kept reducing the vertical height, and switched to a serif font --- but the basic idea has remained the same.

At some point I added the speckled background to the header, which I've really liked, but it falls back to a solid red stripe if the image doesn't load.

![](/images/site_redstripe.png)

## Early 2014: What is that sidebar?

The site went through another redesign and two font changes in 2014, as well as a sidebar that aged badly.
If I'd put anything more useful there it might have worked, but it just had the links that had been in the header.
This only lasted a few months before I moved the sidebar back into the header, and then redesigned the site again.

![](/images/site_redwhite2a.png)

![](/images/site_redwhite2b.png)

## 2013: A big name design

The first major redesign introduced the red-and-white that's been a common theme ever since, along with a name in the header that seems ridiculously large to me today.

![](/images/site_redwhite1.png)

## Late 2012: Octopress

The original site was a lightly modified version of the default Octopress theme, with a blue tint that didn't last.
I'm pretty sure I had a red version of this theme, but neither the Wayback Machine nor my screenshots provide any evidence that it existed.

![](/images/site_octopress.png)

[heroku]: https://www.heroku.com/
[ghp]: https://pages.github.com/
