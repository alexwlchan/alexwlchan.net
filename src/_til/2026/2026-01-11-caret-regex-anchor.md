---
layout: til
title: The caret anchor (`^`) matches differently in Python and Ruby
date: 2026-01-11 10:16:27 +00:00
tags:
  - regex
---
One thing I've come to learn is that there is no "one" regex syntax, and it varies across different languages.
Today I learnt another difference!

<style type="x-text/scss">
  @use "components/tables";
  
  table {
    table-layout: fixed;
  }
  
  th {
    text-align: left;
  }
</style>

<table class="block">
  <tbody>
    <tr>
      <th style="width: 60px; text-align: center; padding: 0 0.5em;">Anchor</th>
      <th>Python (<code>re</code>)</th>
      <th>Ruby</th>
    </tr>
  </tbody>
  <tbody>  
    <tr>
      <td style="text-align: center;"><code>^</code></td>
      <td>Start of <strong>string</strong> by default, start of <strong>line</strong> in <code>MULTILINE</code> mode</td>
      <td>Start of <strong>line</strong> (always)</td>
    </tr>
    <tr>
      <td style="text-align: center;"><code>\A</code></td>
      <td>Start of <strong>string</strong></td>
      <td>Start of <strong>string</strong></td>
    </tr>
  </tbody>
</table>

I discovered this while trying to write a regex in Ruby that would match a word if it appears at the start of the string or the start of a line.

I'm most familiar with Python's regex syntax, and I got confused.
I learnt about the `\A` anchor while reading the [Ruby docs][rb-regex], and then I looked for it in the [Python docs][py-regex].
Comparing the two is what made me realise the caret behaves differently across the two languages.

In this particular case, I can write my regex as `%r{^hello}` and that matches the start of the string or the start of the line, which is simpler than what I expected.

[py-regex]: https://docs.python.org/3/library/re.html#regular-expression-syntax
[rb-regex]: https://docs.ruby-lang.org/en/master/Regexp.html#class-Regexp-label-Boundary+Anchors

