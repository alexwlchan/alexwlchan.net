---
layout: article
date: 2026-04-29 09:24:49 +01:00
title: Building a basic cache with SQLite
summary: An SQLite table that caches expensive operations has dramatically sped up local development of this website.
topics:
  - SQLite
  - Blogging about blogging
---
This website is a static website, built with [a static site generator][mosaic] I wrote myself.
When I'm working on the site locally, I want it to build quickly.
The site is relatively small, modern computers are overflowing with power, so I don't want to be waiting.
Rendering all the HTML pages takes about 15 seconds -- slow enough that I feel the delay *every time*.

When I was using Jekyll, everything got much faster when I [used the Jekyll cache][jekyll-caching].
There's a bunch of expensive computation that doesn't need to be repeated every time I build the site -- for example, converting a chunk of Markdown to HTML can be done once and cached forever.

Since I'm no longer using Jekyll, I've replaced the Jekyll cache with a basic SQLite cache.
I chose SQLite because it's fast, familiar, and I can use it with the [Python standard library][pydoc-sqlite3].

Every cache entry has three parts: a *namespace*, *key*, and *value*.
The namespace groups all entries from a single operation, the key identifies an individual entry, and the value is the output of the expensive computation.
For example, in my Markdown-to-HTML cache, the namespace is `convert_markdown`, the key is the input Markdown, and the value is the output HTML.

Currently I just store basic string values.
I could store structured data as JSON or something, but I haven't needed to yet.

My [cache implementation][gh-cache] is written in Python, but it's just a thin wrapper around SQLite queries.

## SQLite queries

To **create an empty cache**:

```sql {"names":{"1":"cache_entries"}}
CREATE TABLE IF NOT EXISTS cache_entries(
  namespace, key, value, date_saved, 
  PRIMARY KEY (namespace, key)
)
```

This creates an empty table called `cache_entries` with four columns: the namespace/key/value described previously, and a `date_saved` column for debugging.
I thought it would be useful to record when I saved a cache entry, but I haven't needed it yet.

The composite `PRIMARY KEY` ensures I only have one cache entry for a given namespace/key pair.

To **store a cache entry**, I use a standard SQL `INSERT OR REPLACE`:

```sql
INSERT OR REPLACE INTO cache_entries VALUES (?,?,?,?);
```

To **retrieve a cache entry**, I use a standard `SELECT`:

```sql
SELECT value FROM cache_entries WHERE namespace=? AND key=?;
```

One thing I discovered is that this query can be noticeably slow if the cache value is large, because SQLite has to read many pages to retrieve the value.
In some cases I just want to know if a value is cached, not what it actually is -- the mere presence of the cache entry allows me to skip some work.

I have another query to **detect if the cache has a matching entry**, which is much faster because it skips reading the value:

```sql
SELECT EXISTS(SELECT 1 FROM cache_entries WHERE namespace=? AND key=?)
```

Finally, I have a couple of queries to purge the cache -- either an individual entry, or for an entire operation:

```sql
DELETE FROM cache_entries WHERE namespace=? AND key LIKE ?;
DELETE FROM cache_entries WHERE namespace=?;
```

## Choosing cache keys

For small inputs, I use the input as the cache key.

For large inputs (like the Markdown for an entire blog post), I use the MD5 hash as the key rather than the raw input.
That reduces the amount of data written to disk, and should make the database faster.
SQLite uses 4KB pages, which is smaller than many of my blog posts.
You can store lots of MD5 hashes in a 4KB page, whereas a raw blog post would span multiple pages.
That logic is handled outside the caching code.

When the result depends on an external file (like rendering a template), I include the last modified time of the external file in the cache key.
When the external file changes, I get a cache miss and recompute the result.

## How it's going

If you're interested, [my cache implementation][gh-cache] is public, as are [the tests][gh-cache-tests].

The cache has taken some fine-tuning.
[Cache invalidation][wiki-cache-invalidation] is famously difficult, and there are definitely times when I'm not invalidating the cache properly.
When I build the live version of the site, I delete the existing cache and start fresh to avoid stale cache entries.

For local development, this has been a big win.
Re-rendering all the HTML pages used to take about 15 seconds, but with a warm cache it takes 0.06 seconds.
That's a 200&times; speedup that I feel every time I hit save, and it's made working on this site a smoother and more satisfying experience.

[gh-cache]: https://github.com/alexwlchan/alexwlchan.net/blob/main/mosaic/cache.py
[gh-cache-tests]: https://github.com/alexwlchan/alexwlchan.net/blob/main/tests/test_cache.py
[jekyll-caching]: /2024/jekyll-caching/
[mosaic]: /2026/mosaic/
[pydoc-sqlite3]: https://docs.python.org/3/library/sqlite3.html#module-sqlite3
[sqlite-on-conflict-replace]: https://sqlite.org/lang_conflict.html
[sqlite-unique-constraint]: https://sqlite.org/lang_createtable.html#uniqueconst
[wiki-cache-invalidation]: https://en.wikipedia.org/wiki/Cache_invalidation
