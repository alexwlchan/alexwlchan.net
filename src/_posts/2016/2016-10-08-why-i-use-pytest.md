---
layout: post
date: 2016-10-08 18:31:00 +0000
summary: Why py.test is my unit test framework of choice in Python.
tags: python
title: Why I use py.test
category: Programming and code
---

A question came up in Slack at work recently: _"What's your favorite/recommended unit test framework [for Python]?"_
I gave a brief recommendation at the time, but I thought it'd be worth writing up my opinions properly.

In Python, the standard library has a module for writing unit tests &ndash; the aptly-named [unittest](https://docs.python.org/3/library/unittest.html) &ndash; but I tend to eschew this in favour of [py.test](http://pytest.org/).
There are a few reasons I like py.test: my tests tends to be cleaner, have less boilerplate, and I get better test results.
If you aren't using py.test already, maybe I can persuade you to start.

I'm assuming you're already somewhat familiar with the idea of unit testing.
If not, I'd recommend Ned Batchelder's talk [Getting Started Testing](https://www.youtube.com/watch?v=FxSsnHeWQBY) and Eevee’s post [Testing, for people who hate testing](https://eev.ee/blog/2016/08/22/testing-for-people-who-hate-testing/).

So, why do I prefer py.test?

<!-- summary -->

## Less boilerplate

When you write a test with unittest, you have to subclass `unittest.TestCase` and write your tests as methods on that class.
For example:

```python
import unittest

class TestNumberFunctions(unittest.TestCase):

    def test_doubling(self):
        ...

    def test_tripling(self):
        ...
```

Whereas with py.test, you can just specify tests as top-level functions:

```python
def test_doubling():
    ...

def test_tripling():
    ...
```

The py.test code is simpler and easier to write.
I don't have to worry about making a test class, subclassing from whatever `unittest.TestCase` is, adding `self` to all my test methods, and so on.
That's all unnecessary cruft that I no longer have to deal with.

The unittest API design comes from [JUnit](http://junit.org/), a testing framework for Java.
In Java, all functions have to live as methods on a class, so this is a sensible design for a test framework.
But Python doesn't have that restriction, so we shouldn't be bound by it.

## Better asserts and error output

When you use the unittest framework, you have to remember to use the [special assert helpers](https://docs.python.org/3/library/unittest.html#assert-methods).
These produce more helpful diagnostics when a test fails.
For example, consider these two tests:

```python
class TestTheAnswer(unittest.TestCase):

    def test_with_regular_assert(self):
        assert the_answer() == 42

    def test_with_assert_helpers(self):
        self.assertEqual(the_answer(), 42)
```

If the first test fails, all we get is a traceback pointing to the line that failed.
That's all the regular assert handler can tell us:

```
Traceback (most recent call last):
  File "answer.py", line 12, in test_with_regular_assert
    assert the_answer() == 42
AssertionError
```

We know the test failed, but we have no idea what value was actually returned by `the_answer()`.
That could be incredibly helpful in debugging this failure, and it's probably the first thing we'd look for if we got this traceback.

If you use the assert helper, the error includes this information:

```
Traceback (most recent call last):
  File "answer.py", line 9, in test_with_assert_helpers
    self.assertEqual(the_answer(), 42)
AssertionError: 54 != 42
```

But in regular Python code, assert is a statement, not a function, and it's the same for any sort of logical condition.
These weird camel case functions are ugly.
Ick.

In py.test, you just have to use regular assert statements:

```python
def test_the_answer():
    assert the_answer() == 42
```

This is the sort of error output you get:

<div class="highlight"><pre>    def test_the_answer():
&gt;       assert the_answer() == 42
<span style="color: #d01c11">E       assert 54 == 42</span>
<span style="color: #d01c11">E        +  where 54 = the_answer()</span>

hitchhikers.py:14: AssertionError
</pre></div>

I much prefer this error output, and I didn't even have to remember any special methods.

We get both sides of the equation, as with unittest.
But we also see the error in the context of our code, which makes it easy to see exactly what failed, without having to open the file.
Even better, it explains where special values came from, if not hard-coded in the assert – for example, the function call that gaves us 54.
This is very helpful for debugging.

Even better, this can be used for more complex conditions that can't be easily captured with the unittest assert helpers.
Here's the output from another test failure:

<!-- And this!! -->
<div class="highlight"><pre>    def test_some_more():
&gt;       assert (the_purpose_of(life) is not None) or (the_answer() == 42)
<span style="color: #d01c11">E       assert (None is not None or 54 == 42)</span>
<span style="color: #d01c11">E        +  where None = the_purpose_of('life')</span>
<span style="color: #d01c11">E        +  and   54 = the_answer()</span>

arthur.py:16: AssertionError
</pre></div>

I have no idea how py.test is handling asserts under the hood, but it's really helpful.

## Parametrized tests

Often, I want to run the same test with multiple test cases.
With unittest, the best approach is to put them in a `for` loop:

```python
class TestFizzBuzz(unittest.TestCase):

    def test_my_fizzbuzz(self):
        for n, result in [
            (1, '1'),
            (3, 'fizz'),
            (5, 'buzz'),
            (6, 'fizz'),
            (15, 'fizzbuzz'),
            (16, '16'),
        ]:
            self.assertEqual(fizzbuzz(n), result)
```

The problem is, as soon as one of these cases fail, the test is failed and the other cases don't run.
You don't get any information about possible problems with your other test cases.

With py.test, you can use the `@pytest.mark.parametrize` decorator to parametrize your tests.
You provide a list of test cases, but each of those is then evaluated separately.
If one case fails, that doesn't block running the other test cases.
Here's what that looks like:

```python
import pytest

@pytest.mark.parametrize('n, result', [
    (1, '1'),
    (3, 'fizz'),
    (5, 'buzz'),
    (6, 'fizz'),
    (15, 'fizzbuzz'),
    (16, '16'),
])
def test_fizzbuzz(n, result):
    assert fizzbuzz(n) == result
```

When you run this with py.test, you get six test cases, and a separate pass/fail result for each.
More information when a test starts failing means it's easier to work out what's going on.

## Conclusion

I'm only scratching the surface of what py.test can do.
My needs are usually simple: running a collection of test functions.
I don't take advantage of the plugins, or fixtures, or any of the other advanced features.
All it is for me is a better unittest, but that's enough.

When I use pytest, I can write simpler, more Pythonic test code, and with better error output that I find easier to debug.
It's a nice improvement over unittest, and I'm glad to have it in my toolbox.
