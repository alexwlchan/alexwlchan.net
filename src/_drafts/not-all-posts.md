---
layout: post
title: Not all blog posts are created equal
summary:
tags:
index:
  feature: true
---
For a while now, something has felt off about this site.
I was struggling to write even when I had ideas; I was reluctant to publish stuff that was perfectly good; I felt embarrassed if anybody said they'd looked at the site.
I've been struggling with this feeling for a while, but I think I've finally solved it.

At the start of this year, I changed how I think about my writing.
I used to think of everything I wrote as a "post", but now I have two distinct categories: articles and "today I learned".

Labelling these categories has helped me see the difference between the two types of post.
This affects how I write them, and I think my writing has improved as a result -- plus I'm doing more of it.
(I've published as many posts in 2024 as the prior three years *combined*.)
I've also tweaked the visual design, so I can highlight the writing I'm most proud of.

I wanted to live with these changes for a while before I wrote about them, so I'd know how well they actually work.
Now the year is over, I can call this experiment a success.
Let's go through what I've changed.

## what i'm writing?

two types of article

let's go through visual history of how they've appeared on site

---

## Start by simply scrolling

I created this site in 2012 using a static site framework called Octopress
chronological ordering
homepage dropped you on my latest article, go backwards by scrolling through
if you wanted to go back further, had to paginate

[[screenshot]]

alexwlchan.net.2013-09-22.png / forgot i had "read more" buttons in default octopress theme, which made this more usable

alexwlchan.net.2016-04-19.png

https://web.archive.org/web/20130821221620/http://www.alexwlchan.net/

you'd see whatever the last thing i wrote was, whether or not it was the best thing I'd written

not an issue
i was mostly writing for practice and didn't have much of an audience
a lot of programming, tied to specific tools or frameworks
i was already using specific titles, which are great for search, but no stuff in my archive

(also good for SEO imo -- gets people to click)

## Look! A list of links

default octopress also came with archives page, list of links
archives essentially invisible to humans
feels more like a book

Screenshot 2024-12-19 at 23.16.03

As I kept writing, started to get articles I'd want to refer back to
Hard to do in infinite scrolling!
I added a proper landing page and a list of links
Still very chronologically focused, e.g. had per-year and per-month headings

[[screenshot]]

Entire index fits on one page!
I really like this -- imo anything on "page 2" might as well not exist
So much less likely to be seen

And relying on specific titles to help you know what to read
Weirdly this made the programming posts more prominent
Because titles easieer to understand in a list; broad posts get lost

recent posts were list on homepage

julia evans has an excellent site with a similar "list of links"
and added a star to denote her favorites
I have a distinct memory of her tweeting about thsi change, but I can't find it now (mayeb I imagine it? mandela effect)

[[screenshot]]

Screenshot 2024-12-19 at 23.17.07

I copied her topic-based nav with a pixel heart
but didn't last long -- non-obvious what it was, not prominent enough
julia's been doing for eight years

cargo culting
useful lesson: don't copy ideas without understanding underlying reasoning

## Cargo culting cards

the next thing i did was copy ideas without understanding underlying reasoning

around 2020 i started working on wellcome collection stories site
light front-end stuff

that site does a lot more long-form, timeless writing
and articles are accompanied by gorgeous imagery
that's cool!
what if I did that

replaced my list of links with article cards
each with picture, description and date

[[screenshot]]

Screenshot 2024-12-19 at 23.17.40

recent posts were card on homepage

Screenshot 2024-12-19 at 23.17.58

writing description was good!
first bit of pseudo-marketing -- trying to persuade people they might want to read something, not just letting them passively land on page

fun with css flex
one of the most complex web layouts to date
(i build simple web pages)

definitely felt fun for a while!

## to heck with homogeneity

was a good shot in the arm and i enjoyed picking out pictures and colours
but problems with this approach:

1. finding card images was a stretch sometimes
  -> does it help anyone if i put a stock image of a fish on fish shell?

2. disincentivised to write
  -> good articles get prominent billing on homepage
  -> posting something more niche makes it less prominent

the cards felt novel and special at first but shine faded
if everything is special, nothing is

um

the thing that finally prompted the solution was the sheer size of the articles page
although images are lazy loaded, just the HTML markup was nearly half a megabyte
oof
and i don't want to paginate

how do i make it smaller?
do i need all these card images?

then it hit me: different types of post should have a different visual appearance
cards for good articles, list of links for rest

hybrid approach

Screenshot 2024-12-19 at 23.18.40

[[screenshot]]

the cards really draw your attention because they're the first thing you should look at
then the list of links, if you already know you're looking for something specific

organised by date-ish, thumbing scales for cards
cards will always be organised in nice-looking groups
and cards will always be first

meanwhile homepage loses list of recent posts, and just a random selection of favourites
this is a componet called "eggbox" stolen from stories
shows a random selection on each page load, 6 of 43
so they're the first thing a new reader see, hope you'll see something you like

Screenshot 2024-12-19 at 23.19.35

[[screenshot]]

in hindsight this is _so obvious_
anybody who's done design knows you use contrast to draw the reader's attention
big or prominent elements are important, small or hidden elements less so
example i thought of as i designed this was newspapers: headline story gets a big space on the page, small local news is much smaller

wellcome collection stories doesn't do my niche, specific stuff so all cards is appropriate for them
i wanted to write more stuff like that but i didn't want to write just that

## today i learned

and created a new site section "today i learned" for quick posts which are published with minimal editing
get some of the most specific, niche google fodder out of main feed

"if you open more than 10 pages in google"

lowers bar to posting even further
as long as it contains some useful info then worth posting!
seeding future google results

## down with dates, turn to tags

one other change i made was removing all the dates from article list

organising everything by date is holdover from default blog structure
how blogs have been organised for years
good for journals and news but that's not what I write!
nobody is looking for "what alex wrote in 2021"

(for more on this read amy hoy)

i am primary user of this blog, and I know I almost never look by date on other personal blogs
i do look at topics!
like to go to somebody's list of topics, and ctrl-click to open a bunch of topics in tabs

[[screenshot]]

Screenshot 2024-12-19 at 23.19.54

so removed dates from primary nav, and replaced with list of tags/topics
anecdotally, this is what i use now!
previosuly would find article by going to article index, ⌘+F in page to find title, now use tags

dates still on individual pages -- useful to know if programming post is outdated

this is the first iteration of tag page and might refine later -- for example, no way to see popular vs niche tags
maybe a tag cloud? but harder to read

in meantime, list of popular tags on homepage

[[screenshot]]

Screenshot 2024-12-19 at 23.19.35

this is all part of broader push to help people find good stuff

---

## So, how's it going?

honestly really happy
articles page looks great, no longer feel disincentive to post
(haven't posted much in last month or so because working on another big project, but oh well)
and feel breathing room to edit and write long articles properly

love the new topic-based navigation which I use a lot
(and have discovered stuff i forgot i wrote in there)

love the today i learned
am writing a lot of stuff that would otherwise have been lost

one thing that's surprising is how much a few design choices were suppressing my writing
i have so much to say!
but was being disincentivised from doing it
where else is that happening?

have been withdrawing from social media and touching AI tentatively
feels fun to have a place on the internet that's just mine, where i can experiment with design and appearance and do whatever i want

this feels like the promise of the web -- an infinite canvas where we can build wherever we want
fun to be breaking a few of the cultural conventions around what a blog is

have one or two more things banked for 2024 and then want to double down in 2025
goal is to write, not to build space for writing
see you in 2025!
