---
layout: page
title: About the site
summary: How I build the site, the tech underneath it, and my history of questionable design decisions.
date_updated: 2025-06-13 22:01:39 +0100
---
I bought the domain name `alexwlchan.net` on 8th November 2012, and I've been writing here ever since.

I've always built this site using a [static site generator][ssgs].
I write my posts in [Markdown text files][markdown], then I have a tool that converts those inputs into a folder full of HTML files.
I upload that folder to a web server, and then you can browse them on the web.

Currently I build the site using [Jekyll][jekyll], and my web server is a virtual machine hosted by [Linode][linode] which is running [Caddy][caddy].
I use my own theme -- I wrote all the CSS and templates by hand.
The source code is [on GitHub][github], and changes to the site are automatically deployed with GitHub Actions.

I'm constantly making little tweaks and refinement to the site's appearance, and below you can see some of the past designs.
Looking back, what strikes me is how quickly I nailed the basic design.
By 2016, I had the layout I'm still using today -- a coloured header with a mosaic texture, tint colours throughout each page, and a vertical layout.

[ssgs]: https://en.wikipedia.org/wiki/Static_site_generator
[markdown]: https://daringfireball.net/projects/markdown/
[jekyll]: https://jekyllrb.com/
[caddy]: https://caddyserver.com
[linode]: https://www.linode.com/lp/refer/?r=ba2e6ce21e0c63952a7c74967ea0b96617bd44a3
[github]: https://github.com/alexwlchan/alexwlchan.net/

---

## Mid 2022 to present: The coming of cards

In 2022, I introduced cards to make articles look more visually interesting than a collection of text links.
This was part of [a design refresh](/2022/new-archive/) to make it easier for new visitors to find posts they might like in the backlog.
You can see how these cards first looked on the homepage:

{%
  picture
  filename="site_cards_on_the_homepage.jpg"
  alt="A homepage with three coloured cards linking to articles at the bottom of the page. The cards have a title, a picture, and a short description, plus a coloured border."
  width="478"
  class="screenshot"
%}

It took me a while to refine the design of the cards -- for example, switching to images with non-white backgrounds to give a clear gap between image and text, but the basic idea has stuck.

---

## 2018 to mid-2022: A homepage bio and custom colours

Until 2018, the homepage was a scrolling list of my recent posts.
This makes sense if you report on current affairs or news, but it doesn't make sense for me, and it made it difficult to find older writing.
If I'd just written a really long post, you might never see anything else!

I replaced the homepage with a bio and a profile picture, with links out to blog posts but not jumping straight into the content.

{%
  picture
  filename="site_bio_homepage.jpg"
  alt="A red stripe along the top of the site, with a large picture of a face on the right and a bio in the body of the page."
  images_subdir="about-the-site"
  width="478"
  class="screenshot"
%}

I also added a way to customise the tint colour of pages, for example, here's one in purple:

{%
  picture
  filename="site_purplestripe.png"
  alt="An article with a purple stripe across the top, and purple text in the title."
  images_subdir="about-the-site"
  width="478"
  class="screenshot"
%}

---

## 2016: The magic of mosaics

The design didn't change much, but I kept trying to reduce the vertical size of the header.
I like using small phones, and I wanted the header to be as small as possible, so you could see more of the main article on the initial page load.

This is when I added the mosaic background to headers, as a bit of lightweight visual interest.
I'm still using them on the site today!

{%
  picture
  filename="site_bloglist.png"
  alt="A red stripe with speckled squares at the top of the page, with an article below it."
  images_subdir="about-the-site"
  width="478"
  class="screenshot"
%}

---

## Late 2014: The first red stripe

This is the first time I wrote my own templates and CSS, rather than using somebody else's template.
I ditched the sidebars in favour of a bold red header at the top of the page.

{%
  picture
  filename="site_redstripe.png"
  alt="A tall reddish-orange strip with the name “alexwlchan” and a bio line, with an article below it."
  images_subdir="about-the-site"
  width="478"
  class="screenshot"
%}

Although I've made a lot of tweaks, this is still the same basic design I use today -- a brightly coloured header with a few links, a tint colour used through the page, and content presented vertically with no sidebars or horizontal elements.

The screenshot above looks a bit dated, but I can see the bones of the current design.

---

## Early 2014: A short-lived sidebar phase

The second new design switched to another new template, with some new fonts and a short-lived sidebar.
I've never been sure what to put in my sidebar -- it seems a waste of space not to put anything there, but I want it to be sparse so as not to distract from the content.

<figure style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 10px;">
  {%
    picture
    filename="site_redwhite2a.png"
    alt="A white background site with a sidebar on the left and an article in the main area."
    images_subdir="about-the-site"
    width="400"
    class="screenshot"
    style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
  %}
  {%
    picture
    filename="site_redwhite2b.png"
    alt="The same design, but with a slightly different font."
    images_subdir="about-the-site"
    width="400"
    class="screenshot"
    style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
  %}
</figure>

---

## 2013: A big name redesign

The first new design switched to a red-and-white theme which is very similar to the palette I'm still using.
This was based on [Lucas Lew's Whitespace theme](https://github.com/lucaslew/whitespace).

I wrote my name in very large text, which looks faintly ridiculous in hindsight.

{%
  picture
  filename="site_redwhite1.png"
  alt="The name “Alex Chan” in big red letters at the top, then an article below it."
  images_subdir="about-the-site"
  width="478"
  class="screenshot"
%}

---

## Late 2012: Original Octopress

The original site used a lightly modified version of the default [Octopress](https://octopress.org) theme.
It was in blue for a while, and I'm pretty sure it was in red too, but I didn't keep any screenshots.

{%
  picture
  filename="site_octopress.png"
  alt="The name “Alex Chan” at the top, set against a dark blue background, then an article below it."
  images_subdir="about-the-site"
  width="478"
  class="screenshot"
%}

[heroku]: https://www.heroku.com/
[ghp]: https://pages.github.com/
