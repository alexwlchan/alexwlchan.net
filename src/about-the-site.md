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

The current version is back to Ruby and [Jekyll][jekyll], wrapped in Docker to simplify the build process.
What you see today is powered by:

*   [Jekyll][jekyll], for building the HTML
*   [Sass][sass], for building the CSS and stylesheets
*   [nginx][nginx], an HTTP server
*   [Docker][docker], which wraps the local build process and nginx on my server
*   [Azure Pipelines][azure], which builds and publishes the site
*   [Linode][linode], who provide the Linux server where I run nginx (referral link)
*   [Let's Encrypt][letsencrypt] for SSL/TLS certificates

and all the site source code is on [GitHub][github].

Between the Wayback Machine and my screenshots, I've put together a short visual history of what the site used to look like.
Feast your eyes on my evolving skills in mediocre web design.

[jekyll]: https://jekyllrb.com/
[sass]: https://sass-lang.com/
[nginx]: https://nginx.org/
[docker]: https://www.docker.com/
[azure]: https://azure.microsoft.com/en-us/services/devops/pipelines/
[linode]: https://www.linode.com/?r=ba2e6ce21e0c63952a7c74967ea0b96617bd44a3
[github]: https://github.com/alexwlchan/alexwlchan.net/
[letsencrypt]: https://letsencrypt.org

<style>
  img {
    border: 3px solid #ccc;
  }
</style>

## 2018–current: A bio on the homepage

I continue to tweak the styles, but the major themes are the same: Georgia for the font, red accents, that speckled border across the top of the page.

I finally ditched the blog list from the homepage, because it was difficult to get a sense of the site -- what you saw would vary based on what I'd written most recently, and if it was a really long post you might never see anything else!
I replaced the homepage with a bio and a profile picture, with links out to blog posts but not jumping straight into the content.

![](/images/site_bio_homepage.png)

I also added new code to tweak the accent colour and the stripe, so I can theme individual pages if it suits the content.
Here's a purple page:

![](/images/site_purplestripe.png)

## 2016: A speckled red header

I kept cutting the vertical height of the header -- on small phone screens, you'd pretty much only have a header when you loaded the page, and you wouldn't see anything else!

I also added the speckled background, which I've really liked as a bit of lightweight visual flare (barely 2KB).
It falls back to a solid red stripe if the image doesn't load.

![](/images/site_bloglist.png)

## Late 2014: The first red stripe

Unsatisfied with the bubbly menu in the previous design, I did another version of the site that added a red stripe across the top.
I've tweaked this design quite a bit since the first version --- the stripe became a less orangey red, I kept reducing the vertical height, and switched to a serif font --- but the basic idea has remained the same.

Sometime in 2015, I swapped out the sans serif font (this screenshot is Avenir) for a serif font (Georgia), which is the current font.

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
