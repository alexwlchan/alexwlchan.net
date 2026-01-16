---
layout: til
date: 2024-03-24 15:26:20 +00:00
title: How to change the name of an internal link in an Obsidian table
summary: Escaping the pipe like `[[filename\|display text]]` allows you to customise the of a link in a table.
tags:
  - obsidian
---

<style>
  .columns2 {
    display: grid;
    grid-gap: 10px;
    grid-template-columns: auto auto;
  }

  .columns2 img {
    margin-top:    auto;
    margin-bottom: auto;
  }
</style>

I use tables to track recurring documents like bank statements, linking to the file and pulling out some key info at the top level.
But I don't want the filename poking through -- `statement_sqeiu_1234.pdf` -- I want a nice human-readable name.

I can do [internal links with custom display text](https://help.obsidian.md/Linking+notes+and+files/Internal+links) in Obsidian like so:

```
[[statement_sqeiu_1234.pdf|April 2024 statement]]
```

But if I try that syntax in a table, the table breaks:

<div class="columns2">
  <pre><code>| Internal link                    |
| -------------------------------- |
| [[Welcome|This is the new note]] |</code></pre>
  {%
    picture
    filename="obsidian-table-broken.png"
    width="305"
    alt="A table with two columns, because 'Welcome' and 'This is the new note' have been split into two columns."
  %}
</div>

The trick is to escape the pipe in the middle of the internal link:

<div class="columns2">
  <pre><code>| Internal link                     |
| --------------------------------- |
| [[Welcome\|This is the new note]] |</code></pre>
  {%
    picture
    filename="obsidian-table-fixed.png"
    width="305"
    alt="A table with one columns, with 'This is the new note' correctly showing as the link text."
  %}
</div>

You get this behaviour "for free" if you use the Obsidian editor, but for some of these repetitive tables I do the initial editing in an external editor, and then bring it back into Obsidian.
