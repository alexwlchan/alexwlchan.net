---
layout: til
title: Using sqlite-utils to convert a CSV into a SQLite database
date: 2024-01-02 10:54:18 +00:00
summary: |
  You can use sqlite-utils on the command line to create a SQLite database from a CSV file.
tags:
  - sqlite
  - python
---

In the past I've written Python scripts that use the `csv` and `sqlite3` modules to convert CSV data into SQLite, but while reading [a Datasette tutorial][tutorial], I discovered that there's a CLI tool called `sqlite-utils` that makes this much easier.

You can [convert a CSV like so][insert_csv]:

```console
$ sqlite-utils insert [DATABASE_NAME] [TABLE_NAME] [CSV_PATH] --csv
```

For example:

```console
$ sqlite-utils insert reallyuseful.db boxes boxes.csv --csv --detect-types
```

This probably won't be exactly the table I want, compared to the precise schema I could write in my own script, but it's a lot faster!
And sqlite-utils has tools for transforming tables too, so I can finesse them if I need something different.

For example, I can make the `names` column a primary key like so:

```console
$ sqlite-utils transform realluseful.db boxes --pk name
```

[tutorial]: https://datasette.io/tutorials/clean-data
[insert_csv]: https://sqlite-utils.datasette.io/en/stable/cli.html#inserting-csv-or-tsv-data
