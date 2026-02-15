---
layout: note
title: You can set an output mode for SQLite
date: 2025-04-04 06:57:36 +01:00
topic: SQLite
---
Via a [toot from Ian Jackson](https://tech.lgbt/@Diziet/114010058212633945), I learnt that SQLite supports [different output formats](https://sqlite.org/cli.html#changing_output_formats):

The default output mode is `list`, where values are pipe-separated:

```sqlite3
sqlite> .mode list
sqlite> select * from tbl1;
hello!|10
goodbye|20
```

Ian's toot shows off the `box` mode, which renders some ASCII boxes:

```sqlite3
sqlite> .mode box
sqlite> select * from tbl1;
┌─────────┬─────┐
│   one   │ two │
├─────────┼─────┤
│ hello   │ 10  │
│ goodbye │ 20  │
└─────────┴─────┘
```

(They look better in my terminal, where the lines are all joined up.)

Perhaps the one I'm most likely to use is `line`, which prints one column per line -- very useful for tables which have lots of columns:

```sqlite3
sqlite> .mode line
sqlite> select * from tbl1;
  one = hello
  two = 10

  one = goodbye
  two = 20
```

Currently there are 14 different output formats.
The others that look interesting are `csv`, `json`, `html` and `markdown`, which print the data in markup that you can use immediately -- I can imagine there might be cases where that might allow me to use the raw output of a SQLite query.
