---
layout: note
date: 2026-05-27 00:27:03 +01:00
title: GitUp can't diff text files larger than 8MB
summary: Larger files don't appear in the diff view; they're just shown as a file icon.
topic: Git
hidden_topics:
  - GitUp
---
I use [GitUp](https://github.com/git-up/GitUp) as my Git interface, and I was wondering why some of my text files were no longer showing a graphical diff in the interface.

I tried bisecting the files, thinking it might be some special characters that cause the file to be registering as a binary file, and discovered that 8,388,608 bytes is the magic number -- it doesn't produce diffs for files larger than that.
Note that 
<math>
  <mn>8,388,608</mn>
  <mo>=</mo>
  <mn>8</mn>
  <mo>&times;</mo>
  <msup>
    <mn>2</mn>
    <mn>20</mn>
  </msup>
</math> -- that is, 8MB.

A quick search shows other tools having bugs or edge cases at 8,388,608 bytes.

I'm not going to dive into the GitUp source code to work out what the issue is here; for now it's enough to know I can fix my diffs by reducing the size of my source files.
