---
layout: post
title: style-updates-2025
summary:
tags:
  - blogging about blogging
colors:
  css_light: "#d01c11"
  css_dark:  "#ff4242"
---

As well as changing the way I [organise my writing][not_all_equal], last year I made a bunch of cosmetic improvements to this site.

I design everything on this site myself, and I write the CSS by hand -- I don't use any third-party styles or frameworks.
I don't have any design training, and I don't do design professionally, so I use this site as a place to learn and practice my design skills.
It's a continual work-in-progress, but I'd like to think it's improving over time.

I design this site for readers.
I write long, prose-heavy posts with the occasional illustration or diagram, so I want something that will be comfortable to read and look good on a wide variety of browsers and devices.
I get a lot of that "for free" by using semantic HTML and the default styles, with just a handful of tweaks -- most of my CSS is just cosmetic.

Let's go through some of the changes.

[not_all_equal]: /2024/not-all-posts/

## Cleaning up the link styles

This is what links used to look like:

<figure class="screenshot" style="width: 387px;">
  {%
    picture
    filename="old_links_light.png"
    width="387"
    class="dark_aware"
    style="border-top-left-radius: calc(var(--border-radius) - 2px); border-top-right-radius: calc(var(--border-radius) - 2px)"
    alt="A collection of four underlined links on a white background. The unvisited links are bright red, while the visited links are a darker red. The hovered links have a partially transparent red background."
  %}
  {%
    picture
    filename="old_links_dark.png"
    width="387"
    class="dark_aware"
    style="border-bottom-left-radius: calc(var(--border-radius) - 2px); border-bottom-right-radius: calc(var(--border-radius) - 2px)"
    alt="A collection of four underlined links on a black background. The unvisited links are bright red, while the visited links are a lighter pink. The hovered links have a barely visible transparent red background."
  %}
</figure>

Every page has a tint colour, and then I was deriving various versions of that to use to style different links -- a darker shade for visited links, a lighter shade for visited links in dark mode, and a background that appears on hover.

I'm generating these extra shades programatically, and I was so proud of getting that code working that I didn't stop to think whether it was a good idea.

In hindsight, I see several issues.
The different shades diluted the tint colour, and I don't think their meaning was especially obvious.
How many readers ever worked it out?
And the hover styles are actively unhelpful -- just as you hover over a link you're interested in, I'm making it harder to read!
(At least in light mode -- in dark mode, the hover style is barely legible.)

One thing I noticed is that for certain tint colours, the visited colour was barely distinguishable from the text colour.
So I decided to lean into that in the new link styles:

<figure class="screenshot" style="width: 387px;">
  {%
    picture
    filename="new_links_light.png"
    width="387"
    class="dark_aware"
    style="border-top-left-radius: calc(var(--border-radius) - 2px); border-top-right-radius: calc(var(--border-radius) - 2px)"
    alt="A collection of four underlined links on a white background. The unvisited links are bright red, while the visited links are black. The hovered links have a thicker underline."
  %}
  {%
    picture
    filename="new_links_dark.png"
    width="387"
    class="dark_aware"
    style="border-bottom-left-radius: calc(var(--border-radius) - 2px); border-bottom-right-radius: calc(var(--border-radius) - 2px)"
    alt="A collection of four underlined links on a black background. The unvisited links are bright red, while the visited links are white. The hovered links have a thicker underline."
  %}
</figure>

This new set of styles feels more coherent.
I'm only using one shade of the tint colour, and I think the meaning is a bit clearer -- only new-to-you links will get the pop of colour to stand out from the rest of the text.
I'm happy to rely on underlines for the links you've already visited.
And the thicker underline means you can still see what you're hovering over, but the link text remains readable.

## Swapping out the font

I swapped out the font, replacing [Georgia] with [Charter].
The difference is subtle, so I'd be surprised if anyone noticed:

<figure style="width: 634px;">
  <div class="screenshot" style="width: 634px;">
    {%
      picture
      filename="font_georgia.png"
      width="634"
      style="border-top-left-radius: calc(var(--border-radius) - 2px); border-top-right-radius: calc(var(--border-radius) - 2px); border-bottom: var(--border-width) var(--border-style) var(--screenshot-border-color)"
      alt="A collection of four underlined links on a white background. The unvisited links are bright red, while the visited links are black. The hovered links have a thicker underline."
    %}
    {%
      picture
      filename="font_charter.png"
      width="634"
      style="border-bottom-left-radius: calc(var(--border-radius) - 2px); border-bottom-right-radius: calc(var(--border-radius) - 2px)"
      alt="A collection of four underlined links on a black background. The unvisited links are bright red, while the visited links are white. The hovered links have a thicker underline."
    %}
  </div>
  <figcaption style="text-align: center;">
    Above: Georgia. Below: Charter.
  </figcaption>
</figure>

I've always used [web safe fonts] for this site -- the fonts that are built into web browsers, and don't need to be downloaded first.
I've played with custom fonts from time to time, but there's no font I like more enough to justify the hassle of loading a custom font.

I still like Georgia, but I felt it was showing its age a little -- it was designed in 1993 to look good on low-resolution screens, but looks a little chunky on modern displays.
I think Charter looks nicer on high-resolution screens, but if you don't have it installed then I fall back to Georgia.

[Georgia]: https://en.wikipedia.org/wiki/Georgia_(typeface)
[Charter]: https://en.wikipedia.org/wiki/Bitstream_Charter
[web safe fonts]: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Text_styling/Fundamentals#web_safe_fonts

---

# Blocks - blcokquote and pre

Another place where I went overboard with colour variations is code blocks and blockquotes

Blocks = two more shades
-> syntax highlighting is hard to read

Colour draws your attention, so it should mean something
A link says "click here"
A heading says "look here"
What does a blockquote or code snippet say? Just part of the text

Let's dial it in, replace with shades of grey already used on page for meta/hr tags -- more coherent palette
And easier to read

While I'm here, let's talk about margins
Double indent -- from text, and from block
Do want *an* indent to offset from main text, but double-indent looks weird
Want nice crisp lines for everything

Realised this was an issue when I had `blockquote > pre` which had a quadruple indent!
Ridiculous
And looks bad on narrow screens, poor use of space

Let's ditch that left indent

This isn't only roundrect on the site -- also use it for cards on /articles and tag pages
Why different border widths/radii?
I designed cards separately, didn't reuse any styles
Let's redo, gives site a more coherent feel

# action bar

for a while now have wanted some sort of "action bar"
common actions, e.g. reply or subscribe
and a place to link to related or follow-up posts

inspired by Louie Mantia
https://lmnt.me/blog/gulf-of-mexico.html

but couldn't think of design
page was too busy
too much going on

removing colours from blocks -- let's reuse the design of cards
which are very much "click here to do something else"
and so now those are here

can see example on using static websites for tiny archives

not sure if I want it to be variable height to include extra text,
or fixed height and put "see more" elsewhere

i'm mostly sceptical of "read more" -- often just a list of articles with no explanation of *why*
so will be doing organic, human-written text for each
not just a list but why you should read

## onwards

this site should be fun, infused with personality
site has been a place to learn, sometimes gone too far

fashion


