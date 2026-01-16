---
layout: til
title: How to tally the attributes of the top N rows in a SQLite table
date: 2025-01-08 10:17:07 +00:00
tags:
  - sqlite
summary: |
  Use a `WITH` clause to do a nested query for the top N rows in the table, then do a tally over that result.
---
There's a `photos` table in the Flickr Commons Explorer database that has two columns: `owner_id` and `count_views`.
I wanted to get the 10,000 photos with the most views, and then see who owned each of those photos.

Getting the 10,000 photos with the most views is a pretty simple query:

```sql
SELECT *
FROM photos
ORDER BY count_views DESC
LIMIT 10000;
```

I thought maybe I could just add a `GROUP BY` clause to this query, something like this:

```sql
-- This doesn't work!
SELECT owner_id, COUNT(owner_id)
FROM photos
GROUP BY owner_id
ORDER BY count_views DESC
LIMIT 10000;
```

but this query actually counts the number of photos from each member.

I did a bit of reading, and I need to run the first query inside a `WITH` clause, and then do the tally over the result:

```sql
WITH most_viewed_photos AS (
    SELECT owner_id
    FROM photos
    ORDER BY count_views DESC
    LIMIT 10000
)
SELECT owner_id, COUNT(*) as photos_in_top_10k
FROM most_viewed_photos
GROUP BY owner_id
ORDER BY photos_in_top_10k DESC;
```

This query gives me what I want!

Then I added the `{real,user}name` value from the `members` table, which makes it a bit easier to read the result:

```sql
WITH most_viewed_photos AS (
    SELECT owner_id
    FROM photos
    ORDER BY count_views DESC
    LIMIT 10000
)
SELECT
    COALESCE(m.realname, m.username) as member_name,
    COUNT(*) as photos_in_top_10k
FROM most_viewed_photos p
JOIN members m ON p.owner_id = m.id
GROUP BY member_name
ORDER BY photos_in_top_10k DESC;
```

After I wrote this, I was reminded I did some [very similar SQLite tallying](/til/2024/get-a-tally-of-tally-counts/) last year, where I did a nested query and tallied over the results.
