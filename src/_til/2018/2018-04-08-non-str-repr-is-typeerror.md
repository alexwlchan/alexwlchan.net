---
layout: til
title: Python throws a TypeError if you return a non-string from a custom `__repr__` or `__str__` method
summary: |
  It fails with the error "`__repr__`/`__str__` returned non-string".
date: 2018-04-08 16:15:31 +0000
tags:
  - python
---
Here's an example of an object with a non-string `__repr__`:

```python
class BadRepr:
    def __repr__(self):
        return -1

br = BadRepr()
print(repr(br))
```

which fails with a TypeError:

```console?prompt=$
$ python3 bad_repr.py
Traceback (most recent call last):
  File "bad_repr.py", line 6, in <module>
    print(repr(br))
          ~~~~^^^^
TypeError: __repr__ returned non-string (type int)
```

And similar code with a non-string `__str__`:

```python
class BadStr:
    def __str__(self):
        return -1

bs = BadStr()
print(str(bs))
```

which fails in a similar way:

```console?prompt=$
$ python3 bad_str.py
Traceback (most recent call last):
  File "bad_str.py", line 6, in <module>
    print(str(bs))
          ~~~^^^^
TypeError: __str__ returned non-string (type int)
```

(I originally wrote about this [on Twitter](https://www.twitter.com/alexwlchan/status/983015490720288768), and copied it to this site in October 2025.)
