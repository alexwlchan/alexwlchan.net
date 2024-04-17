---
layout: post
title: Getting faster Jekyll builds with caching in plugins
summary: |
  I was able to build my Jekyll site much faster by using the built-in caching API.
tags:
  - jekyll
  - blogging-about-blogging
---

<!-- Card image: https://www.pexels.com/photo/laboratory-test-tubes-2280549/ -->

This website is a static site built with [Jekyll], and recently I overhauled the process for generating the site.
This should be invisible if you're just a reader, but it makes a big difference to me -- like any software project, I'd accumulated cruft and complexity, and it was time to sweep that all away.
The new process is simpler and should be easier to debug when stuff breaks.
Yay!

One of my goals was making the site faster to build.
This site is pretty small, modern computers are silly fast, and yet I was still waiting at least a minute for builds with a warm cache.
I was sure it could be faster!
So I tried to find ways to speed up the build process.

I found two bits of low-hanging fruit that could be useful additions to a lot of Jekyll sites.

[Jekyll]: https://jekyllrb.com/

## Use the Jekyll Cache API

I've written [quite a few Jekyll plugins][plugins] which I keep in my `_plugins` folder.

https://jekyllrb.com/tutorials/cache-api/

[plugins]: https://github.com/alexwlchan/alexwlchan.net/tree/9e6a7db8ace9066fab09886e6bafa6b86c41ed4f/src/_plugins

---

# 1 Use the jekyll Cache API

I have a lot of custom plugins

Jekyll has a built-in cache API

intro'd in Jekyll 4

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
