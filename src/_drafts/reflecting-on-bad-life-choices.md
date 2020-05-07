---
layout: post
title: Taking tuple unpacking to terrible places
summary: I want to assign a bunch of variables to True, but I don't know how many there are. Reflection to the rescue!
category: Python
---

Yesterday, I posted [a snippet of code on Twitter](https://twitter.com/alexwlchan/status/1258147811851460608) that has upset people:

{% tweet https://twitter.com/alexwlchan/status/1258147811851460608 %}

This is a horrific abuse of tuple unpacking, a feature that is usually used for sensible things.
It abuses reflection and the `exec()` function to work, and should never be used for anything serious.
That said, even bad ideas can have interesting things to tell us, so in this post I'm going to explain how it works and how I wrote it.

<figure>
  <img src="5602797265_26f669c246_o.jpg" alt="A side view mirror from a car, shattered and bent lying on the pavement.">
  <figcaption>
    Superstition says breaking a mirror will bring seven years of bad luck.
    Sensibility says using reflection will bring seven years of filthy looks from everybody who has to maintain your code.
  </figcaption>
</figure>



## What is tuple unpacking?

Many programming languages support [*parallel assignment*](https://en.wikipedia.org/wiki/Assignment_(computer_science)#Parallel_assignment), which allows you to assign multiple variables at once:

```
a, b = 0, 1
```

This will set `a` to 0, and `b` to 1.
It's a more concise version of

```
a = 0
b = 1
```

This is often used in Python to return multiple values from a single function:

```python
def f():
    return 0, 1

a, b = f()
```

In Python-land, this is called *tuple unpacking*.
The structures `0, 1` and `a, b` are both Python tuples -- the parentheses you often write around tuples (e.g. `(0, 1)` or `(a, b)`) are optional.

For tuple unpacking to work, you need to have the same number of elements on both sides, so you can build a 1-to-1 mapping between left- and right-hand sides.
If there's a mismatched number of elements, you get an error.
For example:

```pycon
>>> a, b = 0, 1, 2, 3, 4, 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: too many values to unpack (expected 2)
```

The details of tuple unpacking could be a whole other blog post; here it's sufficient to know that this feature exists and you need to balance both sides for it to work.



## Where did this idea come from?

Here's a conversation from a group chat yesterday (shared with permission):

> sgsabbage: I just wrote a boolean as 'Trues'
>
> kapellosaur: You should be able to use that as tuple unpacking
>
> kapellosaur: a, b, c, d = Trues
>
> sgsabbage: :D

We all had a laugh, briefly discussed what dark magic it might take to pull this off, and then conversation moved on.

The tricky part is that the length of `Trues` has to vary depending on the left-hand side -- remember that tuple unpacking only works if you have the same number of elements on both sides.
