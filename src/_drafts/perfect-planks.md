---
layout: post
title: Picking perfect planks with Python
summary: How do you pick the right combination of planks to lay a wooden floor?
tags: python combinatorics maths
---

My friend Madeline is busy renovating her new house, and two nights ago she posted an interesting combinatorics problem:

{% tweet https://twitter.com/oldenoughtosay/status/1434281850709610498 %}

If you start with a pencil and paper, you can start to find some valid combinations.
Here's a few:

```
360 = 180 + 180
    = 90 + 90 + 90 + 90
    = 60 + 60 + 60 + 60 + 60 + 60
    = 90 + 75 + 75 + 70 + 50
```

But what if we wanted to find *all* the combinations?
Using a computer would be much faster than doing it by hand -- so how do we write an appropriate program?

Fortunately for me, I happened to know that Python's [itertools library][itertools] has several functions designed to solve just this sort of problem.
If you haven't used it, the itertools library is a collection of useful functions for working with [iterators].
In Python, iterators are streams that create their entries one-by-one, rather than all upfront.
You step through the iterator to see what it contains, and for long streams this can be much more efficient.

This particular problem is called ["combination with replacements"][combos], and we can use a [function of the same name][function]:

```python
from itertools import combinations_with_replacement
```

When we call this function, we have to tell it the length of the combination.
For example, we can find all the combinations of three boards:

```python
board_lengths = [40, 50, 60, 70, 75, 90, 170, 180]

for combo in combinations_with_replacement(board_lengths, 3):
    print(combo)
```

Here's a sample of the output:

```
(40, 40, 40)
(40, 40, 50)
(40, 40, 60)
…
(170, 170, 180)
(170, 180, 180)
(180, 180, 180)
```

You can see it's working through the combinations in order -- this is the sort of tedious task that's easy for a computer to get right, where a human might slip up.

Then we can filter these combinations to find the ones that sum to the total we want:

```python
target_length = 360

for combo in combinations_with_replacement(board_lengths, 3):
    if sum(combo) == target_length:
        print(combo)
```

and we learn that there's just one combination of length 3:

```
(90, 90, 180)
```

But how many boards do we need?
The valid combinations can be different lengths – in the first few examples I wrote down, there were 2 boards, then 4, then 6, then 5.
When do they stop?
What's the biggest valid combination of boards we could possibly have?

To answer this, let's imagine we're looking at combinations of *N* boards, for some number *N*.
What's the smallest total length they could possibly have?

We'll get the smallest total if we use *N* copies of the shortest board.
If that's longer than the total we're aiming for, then every combination of length *N* will be too long, and we can stop looking.

In Madeline's example, the shortest board has length&nbsp;40 and the target length is 360.
First let's consider *N*&nbsp;=&nbsp;9.
The shortest possible total of a combination of 9 boards is 9&nbsp;×&nbsp;40&nbsp;=&nbsp;360, which is okay.
Now consider *N*&nbsp;=&nbsp;10.
The shortest possible total of a combination of 10 boards is 10&nbsp;×&nbsp;40&nbsp;=&nbsp;400, which is too big -- so we only have to look at combinations of 9 boards or fewer.

To implement this logic, we can use the [`count` function from itertools][count], which gives us an infinite counter:

```python
from itertools import count
```

We'll keep increasing the number of boards until the shortest possible combination is too long:

```python
for number_of_boards in count():
    shortest_possible_total = number_of_boards * min(board_lengths)

    if shortest_possible_total > target_length:
        break

    for combo in combinations_with_replacement(board_lengths, number_of_boards):
        # ...
```

We can put this together for our final solution:

```python
from itertools import count, combinations_with_replacement

board_lengths = [40, 50, 60, 70, 75, 90, 170, 180]
target_length = 360

for number_of_boards in count():
    shortest_possible_total = number_of_boards * min(board_lengths)

    if shortest_possible_total > target_length:
        break

    for combo in combinations_with_replacement(board_lengths, number_of_boards):
        if sum(combo) == target_length:
                print(combo)
```

and we discover that there are 64 possible combinations that sum to 360.

Because we've made this a program, it's easy to re-run if we want to try different parameters.
It turns out that Madeline actually wanted [a total of 330][330], so we can edit the parameters and find the 46 combinations that sum to 330.
Or if she runs out of a particular board length, we can find a new set of solutions with the lengths she has left.

What's great is that we hand off all the hard work of finding the combinations to itertools -- we just have to pick the ones that are interesting.
If you're ever solving a combinatorics problem in Python, start by looking at itertools.

[combos]: https://en.wikipedia.org/wiki/Combination
[itertools]: https://docs.python.org/3/library/itertools.html
[iterators]: https://docs.python.org/3/glossary.html#term-iterator
[function]: https://docs.python.org/3/library/itertools.html#itertools.combinations_with_replacement
[330]: https://twitter.com/oldenoughtosay/status/1434284327718817795
[count]: https://docs.python.org/3/library/itertools.html#itertools.count
