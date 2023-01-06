---
layout: page
title: About the site
summary: How I build the site, the tech underneath it, and my history of questionable design decisions.
---

This site has been through several incarnations.
It's always been a static site, but the choice of generator has changed several times.

The first version, which I posted in late 2012, was built with [Octopress][octopress].
Maintaining a working Ruby setup for Octopress was a lot of hassle, so a year or so later I switched to the Python-based [Pelican][pelican].
That worked fairly well, but [the AGPL and licensing question][agpl] always made me a bit nervous.
In 2016, I experimented with writing my own site generator (called [Hot Chocolate][cocoa]), but I just spent a lot of time reinventing wheels.

[octopress]: http://octopress.org/
[pelican]: https://blog.getpelican.com/
[agpl]: https://github.com/getpelican/pelican/issues/1397
[cocoa]: https://pypi.org/project/hotchocolate/

The current version is back to Ruby and [Jekyll][jekyll], wrapped in Docker to simplify the build process.
What you see today is powered by:

*   [Jekyll][jekyll], for building the HTML
*   [Sass][sass], for building the CSS and stylesheets
*   [Docker][docker], which wraps the local build process
*   [GitHub Actions][github_actions], which builds and deploys the site
*   [Netlify], which hosts the site

and all the site source code is on [GitHub][github].

I'm also using some icons from [the Noun Project][noun], used with a [NounPro subscription][subscriptions].

Between the Wayback Machine and my screenshots, I've put together a short visual history of what the site used to look like.
Feast your eyes on my evolving skills in web design.

[jekyll]: https://jekyllrb.com/
[sass]: https://sass-lang.com/
[docker]: https://www.docker.com/
[github_actions]: https://github.com/features/actions
[github]: https://github.com/alexwlchan/alexwlchan.net/
[Netlify]: https://www.netlify.com
[noun]: https://thenounproject.com
[subscriptions]: https://thenounproject.com/pricing/

## Mid 2022 to present: Cards for browsing the archive

Most of the design is the same as in 2018, barring minor tweaks to spacing and text styles.
I did add cards to the homepage to link to blog posts, as part of [a design refresh](/2022/06/new-archive/) to make it easier for new visitors to find posts they might like in the backlog.

I also used this design on the "best of" posts page, because at nearly 350&nbsp;posts it was impossible for anybody who wasn't me to navigate the archive.

{%
  picture
  filename="site_cards_on_the_homepage.jpg"
  alt="A homepage with three coloured cards linking to articles at the bottom of the page. The cards have a title, a picture, and a short description, plus a coloured border."
  parent="/images"
  visible_width="532px"
  class="screenshot"
%}

## 2018 to mid-2022: A bio on the homepage

I continue to tweak the styles, but the major themes are the same: Georgia for the font, red accents, that speckled border across the top of the page.

I finally ditched the blog list from the homepage, because it was difficult to get a sense of the site -- what you saw would vary based on what I'd written most recently, and if it was a really long post you might never see anything else!
I replaced the homepage with a bio and a profile picture, with links out to blog posts but not jumping straight into the content.

{%
  picture
  filename="site_bio_homepage.jpg"
  alt="A red stripe along the top of the site, with a large picture of a face on the right and a bio in the body of the page."
  parent="/images"
  visible_width="600px"
  class="screenshot"
%}

I also added new code to tweak the accent colour and the stripe, so I can theme individual pages if it suits the content.
Here's a purple page:

{%
  picture
  filename="site_purplestripe.png"
  alt="An article with a purple stripe across the top, and purple text in the title."
  parent="/images"
  visible_width="600px"
  class="screenshot"
%}

## 2016: A speckled red header

I kept cutting the vertical height of the header -- on small phone screens, you'd pretty much only have a header when you loaded the page, and you wouldn't see anything else!

I also added the speckled background, which I've really liked as a bit of lightweight visual flare (barely 2KB).
It falls back to a solid red stripe if the image doesn't load.

{%
  picture
  filename="site_bloglist.png"
  alt="A red stripe with speckled squares at the top of the page, with an article below it."
  parent="/images"
  visible_width="600px"
  class="screenshot"
%}

## Late 2014: The first red stripe

Unsatisfied with the bubbly menu in the previous design, I did another version of the site that added a red stripe across the top.
I've tweaked this design quite a bit since the first version --- the stripe became a less orangey red, I kept reducing the vertical height, and switched to a serif font --- but the basic idea has remained the same.

Sometime in 2015, I swapped out the sans serif font (this screenshot is Avenir) for a serif font (Georgia), which is the current font.

{%
  picture
  filename="site_redstripe.png"
  alt="A tall reddish-orange strip with the name “alexwlchan” and a bio line, with an article below it."
  parent="/images"
  visible_width="600px"
  class="screenshot"
%}

## Early 2014: What is that sidebar?

The site went through another redesign and two font changes in 2014, as well as a sidebar that aged badly.
If I'd put anything more useful there it might have worked, but it just had the links that had been in the header.
This only lasted a few months before I moved the sidebar back into the header, and then redesigned the site again.

{%
  picture
  filename="site_redwhite2a.png"
  alt="A white background site with a sidebar on the left and an article in the main area."
  parent="/images"
  visible_width="539px"
  class="screenshot"
%}

{%
  picture
  filename="site_redwhite2b.png"
  alt="The same design, but with a slightly different font."
  parent="/images"
  visible_width="539px"
  class="screenshot"
%}

## 2013: A big name design

The first major redesign introduced the red-and-white that's been a common theme ever since, along with a name in the header that seems ridiculously large to me today.

{%
  picture
  filename="site_redwhite1.png"
  alt="The name “Alex Chan” in big red letters at the top, then an article below it."
  parent="/images"
  visible_width="478px"
  class="screenshot"
%}

## Late 2012: Octopress

The original site was a lightly modified version of the default Octopress theme, with a blue tint that didn't last.
I'm pretty sure I had a red version of this theme, but neither the Wayback Machine nor my screenshots provide any evidence that it existed.

{%
  picture
  filename="site_octopress.png"
  alt="The name “Alex Chan” at the top, set against a dark blue background, then an article below it."
  parent="/images"
  visible_width="478px"
  class="screenshot"
%}

[heroku]: https://www.heroku.com/
[ghp]: https://pages.github.com/
