---
layout: post
title: Finding divisors of a number with Python
summary: Some code for using Python's itertools module to efficiently find the divisors of a number.
category: Programming and code
---

Here's a problem I was trying to solve recently: given an integer *n*, what are all the divisors of *n*?

A *factor*, also known as a [*divisor*][divisor], is an integer *m* which evenly divides of *n*.
For example, the factors of 12 are 1, 2, 3, 4, 6 and 12.

I ended up writing something with itertools, and the code uses a couple of neat bits of number theory.
I don't do that much maths these days, so the code probably won't go anywhere useful, but I'm writing it up in case it's useful to somebody else.

[divisor]: https://en.wikipedia.org/wiki/Divisor

## The simplest approach

If we want to find all the numbers that evenly divide *n*, we could just try them all:

```python
def get_divisors(n):
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            yield i
    yield n
```

This code is very simple, and for small values of *n* this is good enough -- but it's quite inefficient and slow.
As *n* gets bigger, the runtime increases linearly.
Can we do better?

## Prime factorisations

For my particular project, I was mostly working with [factorials][factorials], which have lots of small prime factors.
The factorial of *n*, denoted *n*! is the product of all the integers up to and including *n*.
For example:

<div style="text-align: center;">
  9! = 9 &times; 8 &times; 7 &times; 6 &times; 5 &times; 4 &times; 3 &times; 2 &times; 1
</div>

Because factorials have lots of small factors, I decided to try getting the divisor list by getting smaller factors.
Specifically, I was looking for *prime factors* -- factors which are also [prime numbers][primes].
(A prime is a number whose only factors are itself and 1.
For example, 2, 3 and 5 are prime, but 4 and 6 are not.)

Here's a function that finds the prime factors of *n*:

```python
def prime_factors(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            n /= i
            yield i
        else:
            i += 1

    if n > 1:
        yield n
```

This is another approach using trial division -- we keep trying factors, and if we find one, we divide it away and keep going.
This is a fairly standard approach to finding primes.

Once we have it, we can use it to write the *prime factorisation* of a number -- that is, writing the number as a product of primes.
For example, the prime factorisation of 9! is:

<div style="text-align: center;">
  9! = 2<sup>7</sup> &times; 3<sup>4</sup> &times; 5 &times; 7
</div>

And computing this factorisation is relatively efficient, especially for factorials -- because the prime factors are all very small, it doesn't take many divisions to get this prime factorisation.

There's a result in number theory called the [*fundamental theorem of arithmetic*][fta] which states that prime factorisations are unique -- for any number *n*, there's only one way to write it as a product of primes.
(I won't write a proof here, but you can find one [on Wikipedia][proof].)

This gives us a way to find divisors -- by finding all the combinations of primes.
The prime factors of any factor of *n* must be a subset of the prime factors of *n*, or it wouldn't divide *n*.

[factorials]: https://en.wikipedia.org/wiki/Factorial
[primes]: https://en.wikipedia.org/wiki/Prime_number
[fta]: https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic
[proof]: https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic#Proof


## Going from a prime factorisation to divisors

First, let's get the factors "with multiplicity" (the prime factors, and how many times each factor appears in the prime factorisation):

```python
import collections

def get_divisors(n):
    pf = prime_factors(n)

    pf_with_multiplicity = collections.Counter(pf)

    ...
```

Then, let's go ahead and construct all the powers of each prime that might appear in a possible factor of *n*.

```python
def get_divisors(n):
    ...
    powers = [
        [factor ** i for i in range(count + 1)]
        for factor, count in pf_with_multiplicity.items()
    ]
```

For example, for 9! this would give us

```python
[
    [1, 2, 4, 8, 16, 32, 64, 128],    // 2^0, 2^1, ..., 2^7
    [1, 3, 9, 27, 81],                // 3^0, 3^1, ..., 3^4
    [1, 5],
    [1, 7],
]
```

Then to combine these into factors, we can use the rather nifty [itertools.product][product], which takes a series of iterables, and spits out all the ordered combinations of the different iterables it receives.
It selects one entry from each list of prime powers, and then by multiplying them together we get a divisor of *n*.

```python
import itertools

def prod(iterable):
    result = 1
    for i in iterable:
        result *= i
    return result

def get_divisors(n):
    ...

    for prime_power_combo in itertools.product(*powers):
        yield prod(prime_power_combo)
```

And thus, we have the divisors of *n* (although unlike the original function, they're not in sorted order).

[product]: https://docs.python.org/3/library/itertools.html#itertools.product



## Putting it all together

Putting that all together gives this function for getting the divisors of *n*:

```python
import collections
import itertools


def prime_factors(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            n /= i
            yield i
        else:
            i += 1

    if n > 1:
        yield n


def prod(iterable):
    result = 1
    for i in iterable:
        result *= i
    return result


def get_divisors(n):
    pf = prime_factors(n)

    pf_with_multiplicity = collections.Counter(pf)

    powers = [
        [factor ** i for i in range(count + 1)]
        for factor, count in pf_with_multiplicity.items()
    ]

    for prime_power_combo in itertools.product(*powers):
        yield prod(prime_power_combo)
```

This particular implementation is very efficient when you have lots of small prime factors, like the factorials I was working with.
I don't know how well it performs in the general case -- and if you're doing proper scientific computing, I'm sure there are pre-existing, optimised routines for this sort of thing.

But as a fun little exercise?
I enjoyed it, and it was nice to dip my toes into number theory again.
