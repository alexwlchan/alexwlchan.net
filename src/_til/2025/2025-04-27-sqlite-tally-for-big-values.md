---
layout: til
title: To filter the results of a SQLite tally for values with a certain frequency, use a `HAVING` instead of a `WHERE` clause
summary:
  "<code>SELECT col_name, COUNT(*) <br/>FROM tbl_name <br/>GROUP BY col_name <br/>HAVING COUNT(*) > 100;</code>"
date: 2025-04-27 21:13:50 +0100
tags:
  - sqlite
---
I was using SQLite to tally some values in a table, which I've done a bunch of times:

```sql
SELECT col_name, COUNT(*)
FROM tbl_name
GROUP BY col_name
LIMIT 10
```

This will print the 10 most frequent tally items, which is useful for exploring the data, but today I wanted to see items above a certain frequency -- all values that appear 100 times or more.

I tried to write this with a `WHERE` clause:

```sql
SELECT col_name, COUNT(*)
FROM tbl_name
GROUP BY col_name
WHERE COUNT(*) > 100
```

but I got an error: *"Error: misuse of aggregate: count()"*.

I found a [Stack Overflow answer](https://stackoverflow.com/a/648089/1558022) that mentions the `HAVING` clause, which does what I want:

```sql
SELECT col_name, COUNT(*)
FROM tbl_name
GROUP BY col_name
HAVING COUNT(*) > 100
```
