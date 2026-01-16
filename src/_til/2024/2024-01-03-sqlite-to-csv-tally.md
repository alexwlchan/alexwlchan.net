---
layout: til
date: 2024-01-03 10:57:21 +00:00
title: Getting a tally of SQLite values as a CSV
tags:
  - sqlite
  - csv
---

I often find myself looking for unique values in a SQLite column.
I always forget the exact syntax for this; this is the sort of query I want:

```sql
SELECT
  column_name, COUNT(*)
FROM
  table
GROUP BY
  column_name;
```

Normally my next step is to take that output and shove it into a spreadsheet, so I can play with it in something like Numbers.
I found a [Stack Overflow thread](https://stackoverflow.com/q/6076984/1558022) which explains how to get SQLite to save your data to a CSV file:

```sqlite3-console
sqlite> .mode csv
sqlite> .headers on
sqlite> .once tally.csv
sqlite> SELECT
   ...>   column_name, COUNT(*)
   ...> FROM
   ...>   table
   ...> GROUP BY
   ...>   column_name;
```

I was hoping for some convenient one-liner, but it seems like you can't chain the dot commands, e.g. `.mode csv; .headers on;` gives an error.

After you run this command, it will print further query output to stdout, still formatted as CSV.
If you want to return it to the default state:

```sqlite3-console
sqlite> .mode list
sqlite> .headers off
```
