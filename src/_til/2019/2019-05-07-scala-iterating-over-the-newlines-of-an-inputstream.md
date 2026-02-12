---
layout: til
title: "How to iterate over the lines of an InputStream in Scala"
date: 2019-05-07 17:38:01 +01:00
tags:
  - scala
old_syntax_highlighting: true
---

```scala
import java.io.{BufferedReader, InputStream, InputStreamReader}

val is = new InputStream(…)

val bufferedReader = new BufferedReader(new InputStreamReader(is))

Iterator
  .continually(bufferedReader.readLine())
  .takeWhile { _ != null }
  .foreach { line => println(line) }
```
