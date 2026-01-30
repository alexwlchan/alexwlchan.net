---
layout: note
title: rot13 and other encodings in the codec module
summary: Use `codecs.encode(…, encoding)` and you have a choice of encodings.
date: 2025-11-01 20:15:28 +00:00
topic: Python
---
I was reminded of this while looking at some old tweets; the [codecs module](https://docs.python.org/3/library/codecs.html#module-codecs) knows how to do rot13, hex, or even zip files:

```pycon {"names":{"1":"codecs"}}
>>> import codecs
>>> codecs.encode('abc', encoding='rot13')
'nop'
>>> codecs.encode(b'abc', encoding='hex')
b'616263'
>>> codecs.encode(b'abc', encoding='zip')
b"x\x9cKLJ\x06\x00\x02M\x01'"
```

I don't know that I have a practical use for this right now, but it's kinda neat.