---
layout: til
title: How to play with SQLite functions without real data
summary: You can run a `SELECT function(…);` query without any tables.
date: 2025-08-19 18:56:33 +0100
tags:
  - sqlite
---
SQLite includes a bunch of [core functions](https://sqlite.org/lang_corefunc.html) like `lower(X)`, `round(X)` and `unicode(X)`.
I wanted to test how these functions work in my local instance of SQLite, but I didn't have a database handy.

It turns out you can write a query that calls these functions on simple values, without needing to fetch that data from a table first:

```sql
sqlite> SELECT lower("A");
a
sqlite> SELECT round(5.5);
6.0
sqlite> SELECT unicode("é");
233
```

The reason I was testing this is because I learnt that the `lower()` and `upper()` functions aren't Unicode-aware unless you load the ICU extension.
Without it, they only know how to change the case of ASCII letters.

The version of SQLite included with macOS doesn't have the ICU extension:

```sql
sqlite> SELECT lower("A");
a
sqlite> SELECT lower("Á");
Á
sqlite> SELECT upper("ı");
ı
```