---
layout: post
date: 2024-04-17 19:44:35 +00:00
title: Getting faster Jekyll builds with caching in plugins
summary: |
  I was able to build my Jekyll site much faster by using the built-in caching API.
tags:
  - jekyll
  - blogging about blogging
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

Most of these are various text processing functions that always return the same output for the same input.
For example, I have one plugin that [adds non-breaking spaces][nbsp] to my rendered HTML, and it always adds the same set of spaces.

This makes my plugins a good fit for Jekyll 4's [caching API], which allows me to cache the expensive computation in my plugins.
The API is quite nice: you create an instance of `Jekyll::Cache`, then you call `getset(key)`.
If `key` is already in the cache, it returns the cached value; if not, it runs the expensive computation once and stores the value in the cache.

Here's an example:

```ruby
def cache
  @@cache ||= Jekyll::Cache.new('AddNonBreakingSpaces')
end

def add_non_breaking_spaces(markdown)
  cache.getset(markdown) do
    expensive_add_non_breaking_spaces_method(markdown)
  end
end
```

In this code, `expensive_add_non_breaking_spaces_method` will only be called once, and then cached until the Markdown changes or the cache is cleared.

The cache is cleared every time you change `_config.yml` or you run Jekyll with a different verb, e.g. `build` or `serve`.
This makes it easy to see the impact that caching is having – make a change to `_config.yml`, then run `jekyll build` twice.
The first build will run with a cold cache, the second with a warm cache.
The difference is the speedup you get from caching.

In this site, adding caching to my plugins speeds up the build from ~6s to ~1.5s.
That's 4× faster!

[nbsp]: /2020/adding-non-breaking-spaces-with-jekyll/
[plugins]: https://github.com/alexwlchan/alexwlchan.net/tree/9e6a7db8ace9066fab09886e6bafa6b86c41ed4f/src/_plugins
[caching API]: https://jekyllrb.com/tutorials/cache-api/

## Add caching to the built-in Jekyll filters

I did some testing with `jekyll build --profile` to find which pages were taking the most build time, and I discovered that the built-in [`smartify` filter](https://jekyllrb.com/docs/liquid/filters/#smartify) was taking a big chunk of the build time.
This is a filter which converts &quot;straight quotes&quot; into &ldquo;curly quotes&rdquo;.

I use this filter in a lot of places (individual posts, index pages, the RSS feed) and it's another good fit for the caching API -- adding curly quotes to a piece of text will always return the same result.

There are two ways you could add caching to the `smartify` filter:

* create a new filter `cached_smartify`, and use that instead of `smartify`
* override the existing `smartify` filter to add caching

I think both approaches are fine, and it just depends on which style you prefer.
In this case, I slightly prefer the second approach, so I added a "cached smartify" plugin to my `_plugins` folder.
This overrides the existing `smartify` filter and replaces it with a cached version.
I can continue to use `smartify` in my templates as before, and enjoy a nice speedup:

```ruby
# cached_smartify.rb
module Jekyll
  module Filters
    alias builtin_smartify smartify
    
    def smartify_cache
      @@smartify_cache ||= Jekyll::Cache.new('Smartify')
    end

    # Like the builtin smartify filter, but faster.
    def smartify(input)
      smartify_cache.getset(input) do
        builtin_smartify(input)
      end
    end
  end
end
```

In my book tracker, adding caching to the `smartify` filter speeds up the build from ~1.8s to ~0.8s.
Nice!

## Conclusion

The last time I refactored the site build, it felt pretty fast.
Over time, I've gradually made changes that slowed it down, and it was feeling pretty sluggish.
I didn't think to record precise timings before I started the refactor, but I know I sometimes had to wait tens of seconds for a build to run.

Now this site takes ~1.5s to build (with a warm cache).
It doesn't exactly feel "fast", but it doesn't feel slow any more.
I'm sure I could wring out more speed if I really tried, but this is already a big improvement and fast enough for now.

A lot of the improvements came from simplifying the build system, and deleting a bunch of custom code that was causing slowness.
The Jekyll caching is only part of the speedup, but it's the improvement most likely to be applicable to other Jekyll sites.

When the site is slow, I get frustrated, bored, and tend to find excuses not to write anything.
When the site is fast, I enjoy working on it and I'm more likely to write new stuff.
One of my goals for this year is to spend more time on my writing, and making it more pleasant to write is a good step in that direction.
