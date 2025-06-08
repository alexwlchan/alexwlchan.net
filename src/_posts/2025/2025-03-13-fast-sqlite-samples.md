---
layout: post
date: 2025-03-13 20:24:51 +0000
title: Fast and random sampling in SQLite
summary: I tested four approaches, from `ORDER BY RANDOM()` to picking random `rowid` values in Python, and found one that's both fast and diverse. Here's what worked (and what didn't).
tags:
  - sqlite
---
I was building a small feature for the [Flickr Commons Explorer] today: show a random selection of photos from the entire collection.
I wanted a fast and varied set of photos.

This meant getting a random sample of rows from a SQLite table (because the Explorer [stores all its data in SQLite][tech]).
I'm happy with the code I settled on, but it took several attempts to get right.

[tech]: https://www.flickr.org/how-does-the-commons-explorer-work/
[Flickr Commons Explorer]: https://commons.flickr.org/

## Approach #1: `ORDER BY RANDOM()`

My first attempt was pretty naïve – I used an `ORDER BY RANDOM()` clause to sort the table, then limit the results:

```sql
SELECT *
FROM photos
ORDER BY random()
LIMIT 10
```

This query works, but it was slow -- about half a second to sample a table with 2 million photos (which is very small by SQLite standards).
This query would run on every request for the homepage, so that latency is unacceptable.

It's slow because it forces SQLite to generate a value for every row, then sort all the rows, and only then does it apply the limit.
SQLite is fast, but there's only so fast you can sort millions of values.

I found a suggestion from [Stack Overflow user Ali][stackoverflow] to do a random sort on the `id` column first, pick my IDs from that, and only fetch the whole row for the photos I'm selecting:

```sql
SELECT *
FROM photos
WHERE id IN (
    SELECT id
    FROM photos
    ORDER BY RANDOM()
    LIMIT 10
)
```

This means SQLite only has to load the rows it's returning, not every row in the database.
This query was over three times faster -- about 0.15s -- but that's still slower than I wanted.

[stackoverflow]: https://stackoverflow.com/a/24591688/1558022

## Approach #2: `WHERE rowid > (…)`

Scrolling down the Stack Overflow page, I found [an answer by Max Shenfield][shenfield] with a different approach:

```sql
SELECT * FROM photos
WHERE rowid > (
  ABS(RANDOM()) % (SELECT max(rowid) FROM photos)
)
LIMIT 10
```

The `rowid` is a [unique identifier][rowid] that's used as a primary key in most SQLite tables, and it can be looked up very quickly.
SQLite automatically assigns a unique `rowid` unless you explicitly tell it not to, or create your own integer primary key.

This query works by picking a point between the biggest and smallest `rowid` values used in the table, then getting the rows with rowids which are higher than that point.
If you want to know more, Max's answer has a more detailed explanation.

This query is much faster -- around 0.0008s -- but I didn't go this route.

The result is more like a random slice than a random sample.
In my testing, it always returned contiguous rows -- `101`, `102`, `103`, `…` -- which isn't what I want.
The photos in the Commons Explorer database were inserted in upload order, so photos with adjacent row IDs were uploaded at around the same time and are probably quite similar.
I'd get one photo of an old plane, then nine more photos of other planes.
I want more variety!

(This behaviour isn't guaranteed -- if you don't add an `ORDER BY` clause to a `SELECT` query, then the [order of results is undefined][undefined_order].
SQLite is returning rows in `rowid` order in my table, and a quick Google suggests that's pretty common, but that may not be true in all cases.
It doesn't affect whether I want to use this approach, but I mention it here because I was confused about the ordering when I read this code.)

[rowid]: https://www.sqlite.org/lang_createtable.html#rowid
[shenfield]: https://stackoverflow.com/a/66085192/1558022
[undefined_order]: https://www.sqlite.org/lang_select.html#:~:text=If%20a%20SELECT%20statement%20that%20returns%20more%20than%20one%20row%20does%20not%20have%20an%20ORDER%20BY%20clause,%20the%20order%20in%20which%20the%20rows%20are%20returned%20is%20undefined

## Approach #3: Select random rowid values outside SQLite

Max's answer was the first time I'd heard of `rowid`, and it gave me an idea -- what if I chose random `rowid` values outside SQLite?
This is a less "pure" approach because I'm not doing everything in the database, but I'm happy with that if it gets the result I want.

Here's the procedure I came up with:

1.  Create an empty list to store our sample.

2.  Find the highest `rowid` that's currently in use:

    ```sql
    sqlite> SELECT MAX(rowid) FROM photos;
    1913389
    ```

3.  Use a random number generator to pick a `rowid` between 1 and the highest `rowid`:

    ```pycon
    >>> import random
    >>> random.randint(1, max_rowid)
    196476
    ```

    If we've already got this `rowid`, discard it and generate a new one.

    (The `rowid` is a signed, 64-bit integer, so the minimum possible value is always 1.)

4.  Look for a row with that `rowid`:

    ```sql
    SELECT *
    FROM photos
    WHERE rowid = 196476
    ```

    If such a row exists, add it to our sample.
    If we have enough items in our sample, we're done.
    Otherwise, return to step 3 and generate another `rowid`.

    If such a row doesn't exist, return to step 3 and generate another `rowid`.

This requires a bit more code, but it returns a diverse sample of photos, which is what I really care about.
It's a bit slower, but still plenty fast enough (about 0.001s).

This approach is best for tables where the `rowid` values are mostly contiguous -- it would be slower if there are lots of `rowid`s between 1 and the max that don't exist.
If there are large gaps in `rowid` values, you might try multiple missing entries before finding a valid row, slowing down the query.
You might want to try something different, like tracking valid `rowid` values separately.

This is a good fit for my use case, because photos don't get removed from Flickr Commons very often.
Once a row is written, it sticks around, and over 97% of the possible `rowid` values do exist.

<style>
  table#results {
    border: var(--border-width) var(--border-style) var(--block-border-color);
    border-radius: var(--border-radius);
    background-color: var(--block-background);
    padding: var(--default-padding);
  }

  table#results tr:not(:last-of-type) > th,
  table#results tr:not(:last-of-type) > td {
    border-bottom: 2px solid var(--block-border-color);
  }

  table#results tr > td:nth-child(2) {
    padding-left: 1em;
  }
</style>

## Summary

Here are the four approaches I tried:

<table id="results">
  <tr>
    <th>Approach</th>
    <th>Performance (for 2M rows)</th>
    <th>Notes</th>
  </tr>
  <tr>
    <td><code>ORDER BY RANDOM()</code></td>
    <td>~0.5s</td>
    <td>Slowest, easiest to read</td>
  </tr>
  <tr>
    <td><code>WHERE id IN (SELECT id …)</code></td>
    <td>~0.15s</td>
    <td>Faster, still fairly easy to understand</td>
  </tr>
  <tr>
    <td><code>WHERE rowid > ...</code></td>
    <td>~0.0008s</td>
    <td>Returns clustered results</td>
  </tr>
  <tr>
    <td>Random <code>rowid</code> in Python</td>
    <td>~0.001s</td>
    <td>Fast and returns varied results, requires code outside SQL, may be slower with sparsely populated <code>rowid</code></td>
  </tr>
</table>


I'm using the random <code>rowid</code> in Python in the Commons Explorer, trading code complexity for speed.
I'm using this random sample to render a web page, so it's important that it returns quickly -- when I was testing <code>ORDER BY RANDOM()</code>, I could feel myself waiting for the page to load.

But I've used <code>ORDER BY RANDOM()</code> in the past, especially for asynchronous data pipelines where I don't care about absolute performance.
It's simpler to read and easier to see what's going on.

Now it's your turn -- visit the [Commons Explorer](https://commons.flickr.org) and see what random gems you can find.
Let me know if you spot anything cool!
