---
layout: post
title: Adding caching to Jekyll's built-in filters
summary:
tags:
  - jekyll
  - blogging-about-blogging
---

https://pixabay.com/photos/filter-technology-metal-round-192936/
https://pixabay.com/photos/highway-lights-night-road-2025863/

I rebuilt the site recently
  - Why?
  - I use Jekyll
  - https://www.cs.cornell.edu/~asampson/blog/jekyll.html
    > Jekyll is not better than the rest for any fundamental design reason; it’s better because it’s enormously popular and therefore excels in the long tail of details. It has great documentation, a thriving plugin and tool ecosystem, and frequent bug fixes. In my experience, it has much fewer frustrating corner cases compared to Nanoc and Pelican.
  - But I'd built Jekyll into a weird corner case! "Don't do it like me"
  - Lots of advantages of using a popular SSG, thrown away because set up in a weird way
  - No more!
  
One thing I'm trying to do is make the site faster to build
  - This site is relatively small
  - Modern computers are silly fast!
  - Why am I waiting close to a minute to build?

Found two bits of low-hanging fruit that are widely applicable

#1 Use the jekyll Cache API

I have a lot of custom plugins

Jekyll has a built-in cache API
Slightly slower on initial build, but faster later
Sprinkle caching everywhere

one example - non-breaking spaces

Also think about what I'm putting in the cache
Shelf headers, why do expensive post-processing in cache????
Big win

#2 Wrap Jekyll filters with caching

do profiling, found smartify was taking a big chunk of site time

smartify is sprinkled everywhere
* articles
* index pages
* RSS feed

let's wrap in Jekyll cache API!

add to _plugins directory

fast_smartify?

tradeoff:
* have to remember thing, but very obviously custom
* don't like to override built-in things, because divergent and weird
  precisely what I'm trying to get away from!

ended up wrapping in smartify, overwriting built-in filter
and hey stuff from code crimes!

# should it be cached in jekyll core?

mmm

I considered proposing it, but on reflection I'm not sure it's a good idea

is caching a pareto improvement?
im not sure

might be cases where it slows the site down
e.g. jekyll cache persists to disk, putting many more filesystem calls in there, is that right?

even if it's better or at worst indifferent, cache invalidation = hard problem in computer science
for my site I know this is there, and I know I'm making extensive use of Cache API
if i start getting weird issues I know where to debug
not everyone does!
may be trading off performance for frustration

and for people like me who want it and are willing to tolerate the potential issues of caching
not hard to add

# result

I didn't think to get before/after numbers
Not concerned about hitting a specific number
But it felt "slow"
site now takes ~2.5s to build
Now … it doesn't feel "fast" but it doesn't feel slow either

I'm sure more can be wrung out, but increasingly esoteric and complicated
these are quick wins

follows broad trajectory of all software
starts fast, cruft gradually accumulates, clear out and reset
will soon end up
