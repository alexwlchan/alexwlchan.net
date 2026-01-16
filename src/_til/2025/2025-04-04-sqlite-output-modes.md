---
layout: til
title: You can set an output mode for SQLite
date: 2025-04-04 06:57:36 +01:00
tags:
  - sqlite
---
Via a [toot from Ian Jackson](https://tech.lgbt/@Diziet/114010058212633945), I learnt that SQLite supports [different output formats](https://sqlite.org/cli.html#changing_output_formats):

The default output mode is `list`, where values are pipe-separated:

<pre><code>sqlite&gt; <strong>.mode list</strong>
sqlite&gt; <strong>select * from tbl1;</strong>
hello!|10
goodbye|20
sqlite&gt;</code></pre>

Ian's toot shows off the `box` mode, which renders some ASCII boxes:

<pre><code>sqlite&gt; <strong>.mode box</strong>
sqlite&gt; <strong>select * from tbl1;</strong>
┌─────────┬─────┐
│   one   │ two │
├─────────┼─────┤
│ hello   │ 10  │
│ goodbye │ 20  │
└─────────┴─────┘
sqlite&gt;</code></pre>

(They look better in my terminal, where the lines are all joined up.)

Perhaps the one I'm most likely to use is `line`, which prints one column per line -- very useful for tables which have lots of columns:

<pre><code>sqlite&gt; <strong>.mode line</strong>
sqlite&gt; <strong>select * from tbl1;</strong>
  one = hello
  two = 10

  one = goodbye
  two = 20
sqlite&gt;</code></pre>

Currently there are 14 different output formats.
The others that look interesting are `csv`, `json`, `html` and `markdown`, which print the data in markup that you can use immediately -- I can imagine there might be cases where that might allow me to use the raw output of a SQLite query.
