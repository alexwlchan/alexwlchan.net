---
layout: til
date: 2024-05-04 09:29:22 +01:00
title: How to get a tally of tally counts in SQLite
summary: |
  Using a nested query allows me to perform a two-level aggregation of the values in a column – how many values appear once, how many twice, and so on.
tags:
  - sqlite
---
I was poking through my [analytics data](https://github.com/alexwlchan/analytics.alexwlchan.net) and I was curious how many pages people are looking at.
I track hits in a SQLite database, with a table called `events` and a column `session_id` which contains an anonymous ID to track visitors across multiple pages.

I already know how to tally over that column:

```sql
SELECT
    session_id,
    COUNT(session_id) as count
FROM
    events
GROUP BY
    session_id
ORDER BY
    count DESC
```

```
session_id                           | count
988e1f9a-733d-4aef-a134-034ddab75354 | 568
f4ef0793-fb47-4023-976a-05bc2595b22e | 553
2fe39ac6-977a-488a-9b23-71ac88f1698b | 420
c11e1ffe-d3be-48af-91a6-52a07a97c39c | 402
76f677e9-120d-4f2f-9c0d-b2b63550bba2 | 388
```

(Unsurprisingly, all the really high numbers are from `localhost` with me testing the site in preview.)

But what if I want to tally over the `count` column?
Since the session IDs are randomly generated they're not very useful; it'd be more useful to see how many people visited one page, two pages, three pages, and so on.

Thanks to ChatGPT, I know that what I need to do is a "nested query" like so:

```sql
SELECT
    count,
    COUNT(*) as frequency
FROM
(
    SELECT
        session_id,
        COUNT(session_id) as count
    FROM
        events
    GROUP BY
        session_id
    ORDER BY
        count DESC
)
GROUP BY
    count
ORDER BY
    count
```

```
count | frequency
1     |     98297
2     |      7899
3     |      1698
4     |       692
5     |       329
```

I'm not sure how well this query performs, but it's good enough for one-off experiments, and useful to know that I can pass the output of one SQL query to another.
