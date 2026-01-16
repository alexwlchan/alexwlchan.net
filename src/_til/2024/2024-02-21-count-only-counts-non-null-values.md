---
layout: til
date: 2024-02-21 16:00:27 +00:00
title: The COUNT(X) function only counts non-null values
tags:
  - sqlite
---
I was running a tally in a `photos` table with a text column `photos`, and I got a surprising result:

```
sqlite> SELECT media, COUNT(media) FROM photos GROUP BY media;
|0
photo|1813253
video|1131
```

Why is there a value with 0 results in the tally?
That seems odd!

The issue turned out to be a misunderstanding on my part about the COUNT(X) function – it only counts the number of times that [X is not NULL](https://www.sqlite.org/lang_aggfunc.html#count).

I had a number of null rows in the database, but they weren't being counted:

```
sqlite> SELECT COUNT(*) FROM photos WHERE media IS NULL;
340
```

The tally query I actually want uses `COUNT(*)`, not `COUNT(X)`:

```
sqlite> SELECT media, COUNT(*) FROM photos GROUP BY media;
|340
photo|1813253
video|1131
```

## Other thoughts/clues

*   I initially asked ChatGPT, which told me that `GROUP BY` can find deleted rows.
    I haven't been able to find an independent source for this, so I think it might be a hallucination.
    
    It did suggest running the `VACUUM` command as a way to trigger some sort of database rebuild, but that didn't change the behaviour I was seeing.
    
*   One of ChatGPT's other suggestions was creating a new table -- that felt like a more helpful suggestion, because it might force a table rebuild and flush any transient data.

    I ended up running the following lines repeatedly, adjusting the limit/offset and trying to cut down the table to find the rows that triggered the problem:

    ```sql
    DROP TABLE
      new_photos;

    CREATE TABLE
      new_photos
    AS SELECT
      id, media
    FROM
      photos
    LIMIT 5
    OFFSET 54850;
    
    SELECT media, COUNT(media) FROM new_photos GROUP BY media;
    ```

    Once I'd got a small enough set, I inspected those rows manually and found the data that was causing the mysterious tally behaviour:
    
    ```
    sqlite> SELECT id, media FROM photos LIMIT 5 OFFSET 54850;
    14541672258|photo
    14541680439|photo
    14728030192|photo
    14725963694|photo
    52966470900|
    ```
    
    This was the clue I needed to go double-check how `COUNT(X)` works.

*   The tally should count every row in the database.
    If I'd cross-checked the total of the tally with the number of rows in the database, I'd have noticed the missing rows:

    ```
    sqlite> SELECT COUNT(*) FROM photos;
    1814724
    ```
    
    but the initial tally has 1813253 + 1131 = 1814384, which is short.