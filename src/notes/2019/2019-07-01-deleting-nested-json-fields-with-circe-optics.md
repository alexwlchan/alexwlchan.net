---
layout: note
title: "Deleting nested JSON fields with Circe optics"
date: 2019-07-01 18:30:47 +01:00
topic: Scala
hidden_topics:
  - JSON
---

Removing a top-level field:

```scala
root.obj.modify { _.remove("ingestType") }(json)
```

Removing a nested field:

```scala
root.ingestType.obj.modify { _.remove("x") }(json)
```
