---
layout: til
title: Create compact JSON with Python
summary: |
  Calling `json.dumps(…, separators=(',', ':'))` will reduce the amount of whitespace in the final string.
date: 2018-10-24 08:18:00 +00:00
tags:
  - python
  - json
---

To create compact JSON in Python:

```pycon
>>> json.dumps({'a': 1, 'b': 2})
'{"a": 1, "b": 2}'

>>> json.dumps({'a': 1, 'b': 2}, separators=(',', ':'))
'{"a":1,"b":2}'
```

(via [Raymond Hettinger](https://twitter.com/raymondh/status/842777864193769472))
