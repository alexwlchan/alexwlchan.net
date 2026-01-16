---
layout: til
date: 2024-01-17 13:09:57 +00:00
title: How to tally combinations of values across multiple columns
tags:
  - sqlite
---
Recently I've been doing a lot of tallying of values within a single column, so I remember this structure of query quite well:

```sql
SELECT
  column_name, COUNT(column_name)
FROM
  table
GROUP BY
  column_name;
```

You can also tally combinations of values across multiple columns, which takes the form:

```sql
SELECT
  column_name1, column_name2, COUNT(*)
FROM
  table
GROUP BY
  column_name1, column_name2;
```

Here's an example of a real query from a table of web server logs, which counts occurrences of a status code on each day:

```sql
SELECT
  date, status, count(*) as hits
FROM
  access_logs
GROUP BY
  date, status
ORDER BY
  hits desc
```