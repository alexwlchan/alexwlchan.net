---
layout: post
date: 2016-06-07 12:00:00 +0000
tags: python
title: Introduction to property-based testing
category: Talks
---

This is a presentation I gave for the Cambridge Python User Group in June&nbsp;2016.
Notes and the slides are shown below.

The notes aren't a transcript, just my rough notes of the major points I wanted to cover.

I was speaking for about an hour, so there's quite a lot of material here.
Enjoy!

<!-- summary -->

---

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 0,
  :alt => "Title slide."
%}

Automated testing is a necessity of modern software development.
It gives us a safety net for our code &ndash; running continuous tests help us catch bugs and regression before code reaches our users.

In this talk, I'll show you three powerful approaches to automated testing that help you find bugs in your code, but which don't cost an arm and a leg.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 1,
  :alt => "Agenda slide."
%}

Part&nbsp;1 is the practical stuff: property-based testing with Hypothesis.
This is what most people think of when they say "property-based testing".
In parts&nbsp;2 and&nbsp;3, we'll look at some more advanced ideas in the same vein.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 2,
  :alt => "How do we usually test code?"
%}

But first, I think it's instructive to look at how we normally write tests.
Let's suppose we're testing a single function.

1.  We start by writing down some example inputs &ndash; what sort of inputs do we expect to our function?
2.  Once we know exactly what the inputs should be, we can write down exactly what the outputs should be.
3.  Finally, we tell the computer to run through our examples, and check the results are as we expect.
    Any deviation from the expected output is a failure.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 3,
  :alt => "An example: sorting a list of integers, with a few examples of lists and their sorted outputs."
%}

Let's look at an example: sorting a list of integers.
Perhaps not something we do very often, but it illustrates the point.

On the left, I've written down some example lists.
On the right, I've written down what those lists look like when they're sorted.
That gives us our test cases.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 4,
  :alt => "Some Python code showing how we might write a test for a function that sorts a list of integers."
%}

We can encode these examples in Python.
*[Note: I'm using [pytest][pytest] assert syntax throughout, but all my examples work just as well with unittest.]*

This style of testing has some problems:

*   Coming up with examples is boring.
    Somebody has to write them out by hand.
    If it's boring, it doesn't get done.

*   They're hard to maintain.
    We have lots of hard-coded data in our test suite.
    Lots of magic strings and numbers, and it's not always obvious when they're correct.

*   The big problem is that it's hard to get good coverage.
    Not line coverage &ndash; there's [coverage.py][cov] for that &ndash; but getting a good coverage of the input space.
    All this test tells us is that we have five working examples.

    How do we know there isn't another input where it's completely broken?

    How do we know there aren't edge cases we're missing?

    (If you write the tests at the same time as the code, will you remember to test an edge case if you forgot to code for it?)

Coming up with a good set of examples is *hard*.
You want something random and unbiased &ndash; that gives you a better chance of hitting edge cases, and finding bugs in your code.

Humans are bad at this, so why don't we ask the computer?

[pytest]: http://pytest.org/latest/
[cov]: https://pypi.python.org/pypi/coverage/

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 5,
  :alt => "Header slide: “Property-based testing with Hypothesis”"
%}

In property-based testing, rather than write the examples ourselves, we let the computer come up with them.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 6,
  :alt => "A description of the steps of property-based testing"
%}

How it works:

1.  Start by describing the input.
    Tell the computer what sort of examples we want it to use.
    The computer will use this to generate random inputs.

2.  Describe the output.
    Because we don't know exactly what the input will be, we can't write down the exact input.
    We need to give the computer other ways to tell if the test has passed.
    These are the "properties".

3.  Run the test lots of times &ndash; let the computer draw examples, and check them against our property.
    It can draw hundreds of examples in a very short time; far more than we could practically write by hand.

This gives us a much more demanding test.
Our code has to stand up to hundreds of examples &ndash; that makes it much more likely to find a bug (if one exists).
If we don't find a bug, we have much more confidence in our code.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 7,
  :alt => "A slide with a bulleted list, titled “When can we say a list is sorted?”"
%}

Let's go back to our list sort example.

The inputs to this test are in the name &ndash; a list of integers &ndash; so let's think about properties.
How do I know if a list is sorted?

*   A sorted list is a list.
    If I try to sort a list, and I get back a string, a tuple or a float, something's gone wrong.
*   A sorted list preserves the items in the list.
    If a sort routine throws away or inserts items, it's made a mistake.
*   A sorted list is ordered: if I compare pairs of adjacent elements, every pair has to be sorted.
    Anything else is a bug.

These three properties are a much stronger test than the five examples.
This *defines* a sorting routine &ndash; if a function passes these three conditions, it sorts a list of integers.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 8,
  :alt => "Python code showing how we’d assert that a list of integers is sorted."
%}

We can write these properties as code.
This is a very compact test: in just a few lines of code, we've provided a complete test for a sort routine.

Our test has two arguments: a sort function, and a list of numbers.
We'll provide the first argument, and we'd like the computer to fill in the second.
We'd like it to generate lots of random lists of random integers.
At this point, we could just break out the random module, but I want to show you an alternative.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 9,
  :alt => "A bullet slide with a picture of a man’s face: “Enter Hypothesis”."
%}

We're going  to look at a Python library called Hypothesis.
Hypothesis is best known for being used as a property based testing library, but it's real strength is in generating structure random data. That might sound like an oxymoron &ndash; I'll explain what I mean shortly.

When you're using it for property-based testing, it integrates with all the standard Python test runners, so you can run it alongside your regular unit tests.

It's inspired by a Haskell library called [QuickCheck][quickcheck], which is where the idea of property-based testing originally comes from.
This sort of testing has its roots in the world of functional programming.

[quickcheck]: http://www.cse.chalmers.se/~rjmh/QuickCheck/

It's written by David MacIver, pictured here.
I believe David originally wrote this as a way to learn about Python (most people settle for "hello world"), and it sort of&#8230; grew.

<!-- TODO: take out the link -->

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 10,
  :alt => "Some Python code showing how to run a test with Hypothesis, and what the output looks like."
%}

This is what our example looks like with Hypothesis.
I've only had to add two lines: imports, and the `@given` decorator.

The `@given` decorator is the entry point to a test with Hypothesis.
We supply it with a *strategy* (in this case, `st.lists(st.integers())`) and it draws 200&nbsp;examples.
It passes the examples into your test, and sees what happens.

So it's creating 200&nbsp;random lists of random integers, and testing them with Python's builtin sort routine.
It checks our sort conditions, and sees if it finds a failure.
It doesn't find a counterexample (probably not surprising), so it lets the test pass.
This only shows up as one test case in your test runner, so you don't get swamped with individual test cases.

If it had found a counterexample, it would fail the test.
That prints a single failing example, and registers a failure in your test runner.
We'll see what that looks like shortly.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 11,
  :alt => "A slide with a bulleted list: “What are strategies?”"
%}

Let's break down what Hypothesis gets is over generating random examples ourselves.
First up is strategies.

A strategy is recipe for random data.
This is how we *describe the input*.
It tells Hypothesis what sort of examples to create.

Hypothesis can generate examples of all the built-in types: numbers, strings, and so on.
When you're dealing with floating point numbers or Unicode strings, it can actually be hard to come up with the most pathological examples, but Hypothesis can do it for you.
It's also supposed to have good support for generating examples based on Django models, but I don't use Django so I haven't tried those features.

It's really easy to compose strategies &ndash; we've already seen that, where we composed the list strategy and the integer strategy to create a list of integers.
And what if you have custom classes?
Easy to create example data with those too.

Finally, strategies know how to shrink themselves.
Creating small, easy-to-debug examples is a key feature of property-based testing.

*[Note: you can read about all the strategies Hypothesis supports in [the docs](http://hypothesis.readthedocs.io/en/latest/data.html).]*

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 12,
  :alt => "Python code showing a custom Hypothesis strategy for creating instances of a `Person` class."
%}

Let's look at how we can create examples from custom classes, using Hypothesis's strategies.

Here I have a Person class that records a few attribute: name, birthday, pets, and height.
Maybe I'm making a Facebook for pet owners.

The `builds` strategy lets me build a strategy from my Person class: the first argument is a target, and then the subsequent args and kwargs are passed into the class constructor.
Voila: a strategy that creates instances of the Person class.

But the examples are pretty messy.
You can tune strategies to get data that fits your application: you don't just have to accept all text, or all numbers.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 13,
  :alt => "Python code showing the previous strategy, but with some restrictions on creating names."
%}

I'll start by sorting out the names.
You can't have the empty string as your name, and I'll restrict the set of characters you can draw from.
Now we get names that look a bit odd, but aren't completely ridiculous.
*[Note: I know these are both [bogus restrictions][names] on names, but it illustrates the point.]*

Next, let's sort out birthdays.
This example comes from the year&nbsp;9241.
I feel like if a time traveller comes back from the future, they won't be signing up for Facebook for Pets.

[names]: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 14,
  :alt => "Python code showing the previous strategy, but extra restrictions on when you can have a birthday."
%}

We can bound the years from which Hypothesis draws dates.
Now we get a more sensible birthday: 21st June, 1982.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 15,
  :alt => "Python code showing the previous strategy, but now you have to choose a pet from “dog”, “cat” and “fish”."
%}

Next, let's tackle the pets, because Hypothesis is giving us silly examples.
In this case, there are only a few valid values, so we give tell Hypothesis an explicit set of choices with `sampled_from`.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 16,
  :alt => "Python code showing the previous strategy, but now your height is between 0.0 and 3.0."
%}

Finally, let's fix the fact that the last person's height was larger than the size of the known universe&#8230; and negative.
We can bound the height to something vaguely sensible.

In just a few lines of code and config, we've glued together Hypothesis's strategies to generate examples from a custom class, and constrained it to give examples to match our use case.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 17,
  :alt => "A Hypothesis test that casserts the double-negative number of itself, and test output showing that NaN is a counterexample."
%}

Filtering at the strategy level lets us cut out wide swathes of examples.
What about specific examples?

Here's a test that anybody sensible would expect to pass &ndash; reversing the sign of a number twice gets us back to the original number &ndash; but floating numbers are horrible.
NaN has the fun property that it's not less than or equal to itself, so comparing NaN to NaN will fail.

Hypothesis prints us this nice output showing us the counterexample, and raises a failure in our test runner.

But if we decide that Hypothesis has found a silly example, how can we exclude it?

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 18,
  :alt => "Code and output for a Hypothesis test that uses `assume()` to filter out a specific example."
%}

We can use `assume()` to filter specific examples.
This throws a magic exception that tells Hypothesis "this was a bad example, give me less examples like this".

Once we exclude that bad example, the problem goes away, and the test passes.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 19,
  :alt => "Code for a Hypothesis test that asserts float addition is associative, and output showing a counterexample and a failed test."
%}

Here's another example showing why floating-point numbers are horrible.
Another sensible property that fails.

When your application deals with complex spaces like floating-point numbers, or Unicode text, Hypothesis is an invaluable testing tool.  It can go out and find examples that you'd never think to test yourself.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 20,
  :alt => "A slide with a bulleted list: “What is shrinking?”"
%}

Next feature: shrinking.

When we find a bug, we want to reduce it to a minimal failing example.
A small example is easier to debug and reason about, and generally easier to assess.
There are tried-and-tested techniques for stripping down examples: try smaller values, reduce the size of lists, binary debugging, and so on.

Hypothesis's strategies know how to make smaller examples, and Hypothesis can try lots of examples really quickly.
So when it finds a failing example, Hypothesis doesn't just show you the messy first example.
It tries to *shrink* the example, and find the smallest failure it can.
This gives you much nicer results.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 21,
  :alt => "Code for a test that makes a specious assumption about integer lists, and the output from a failing test."
%}

Here's a dubious proposition about sorting: sorting the concatenation of two lists is the same as sorting them individually, and concatenating both results.

It's not surprising that it fails, but the counterexample is really small: there isn't a simpler example that still triggers this bug.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 22,
  :alt => "Output from a test that shows the different examples which were tried before it gave the result."
%}

If we look at the examples Hypothesis was trying, we see this wasn't luck.
The first example where it hit this bug was horrible: a big list containing some horrible integers.

It starts reducing the size of the lists, discovering it doesn't need many elements to repro the failure.
Eventually it gets down to one element in each list.
Then it tries cutting down the value in each list.
It actually overshoots, and tries `xs=[0], ys=[1]`, an example which doesn't fail, before finding the minimal example that it presents to the user.

Doing this shrinking is possible by hand, but it's another example of work we can push off to the computer.
I think it's a really important feature of property-based testing libraries: it makes the bugs much more palatable to work with.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 23,
  :alt => "A slide with a bulleted list: “What about rare examples?”"
%}

Now, let's think about flakiness.

By default, Hypothesis tries 200&nbsp;examples per test, but it's quite plausible that we'd have a bug that occurs in less than 1&nbsp;in&nbsp;200 cases.
If we were drawing truly random examples, a test would fail randomly, depending on whether it happened to draw a failing example.
That gives us flakey tests, which are worse than no tests at all &ndash; they only act to cause confusion.

So Hypothesis keeps an *examples database*: a local file recording any interesting examples that it finds.
When it runs a test, it starts by looking for prior examples in the database.
This means that once it finds a failing example, it will persistently fail that test until you fix the bug, or tell Hypothesis that it was a bad example.

*[Note: Hypothesis actually stores _every_ failing example that it finds, and gradually discards them when the test starts passing again.  So if the process of shrinking causes Hypothesis to encounter more than one bug, it won't forget.  This was a question on the day.]*

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 24,
  :alt => "Some example code for a function and test to get somebody’s next birthday."
%}

To see this, let's go back to my person class.

I keep forgetting my friends' birthdays, so I've written a function that tells me when somebody has their next birthday.
There's a bug in this code, specifically this line:

    birthday = date(current_year, month, day)

If somebody's birthday is 29th&nbsp;February, this will throw an error.
But people with that birthday are comparatively rare &ndash; only about 1&nbsp;in&nbsp;1000&nbsp;birthdays fall on that day.

(This example is based on a very similar bug that I wrote two years ago, and which we only noted this past spring.)

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 25,
  :alt => "Showing the output of eight successive runs of Hypothesis: seven passed green, the eighth found a bug."
%}

Unsurprisingly, the first test run succeeds &ndash; 200&nbsp;examples, with a 1&nbsp;in&nbsp;1000&nbsp;failure rate.
And the second run.
And the third.

When I ran this before the talk, it took eight runs before it found the bug &ndash; but it did indeed find it.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 26,
  :alt => "Output from the first test that found the bug, taking 0.48 seconds."
%}

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 27,
  :alt => "Output from a subsequent run that found the bug, taking just 0.09 seconds."
%}

Hypothesis discovers the bug, and raises it as an error.
It's also stored the bug in its database, so the next time I run this test, it takes a fraction of the time it took the original.
(0.09s compared to 0.48s.)

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 28,
  :alt => "A Hypothesis test that uses the `@example` decorator to remember an example."
%}

Once we've found this example, we'd like Hypothesis to always check it in future &ndash; as it's rare, we might not spot a regression immediately.

We can easily use the `@example` decorator to capture this example, and this means Hypothesis will always try this example, in addition to the random examples from the strategy.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 29,
  :alt => "Slide with a bulleted list: “Hypothesis summary”."
%}

<!-- TODO: fix URL colouring -->
<!-- TODO: fix the pip install colour -->

So that's the features that distinguish Hypothesis from generating random examples.
It enables a very powerful style of testing, and I have yet to throw it at a codebase and not see bugs fall out.

Hypothesis is available from PyPI.
There's really good documentation [on ReadTheDocs](http://hypothesis.readthedocs.io/), and lots of articles about this style of testing [on hypothesis.works](http://hypothesis.works/articles/).
This includes a [list of property-based testing libraries](http://hypothesis.works/articles/quickcheck-in-every-language/) in other languages, and [how you can hire David](http://hypothesis.works/services/) for training and support.

Often when I show people this style of testing, they get excited and think it's cool, but don't know where to get started.
Now I want to show you some simple patterns for getting started with property-based testing.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 30,
  :alt => "Code and a bulleted list: “Testing patterns: simple fuzzing”."
%}

Let's start with a simple assertion: your code shouldn't crash.
If I can pass your function input that causes it to throw an exception, that's almost certainly wrong.

Use Hypothesis to throw random data into your function.
See what happens.
Along the way, you'll have to think carefully about exactly what sort of input your function takes.

Then start making simple assertions about the output.
Does your function return anything?  If so, make an assertion.
Can your function return None?  If not, make an assertion.
Does your function return a consistent type?  Make an assertion.

This is small stuff, but it starts to expose cracks in your code.

We'll come back to this idea later.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 31,
  :alt => "Code and a bulleted list: “Testing patterns: round trip”."
%}

Another pattern is what I call "round trip".
Suppose we have two functions that are inverses &ndash; in that case, applying both functions should get us back to where we started.

This is particularly useful any time you have to do encoding or decoding of data, or if you're writing any sort of serialisation code.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 32,
  :alt => "Code and a bulleted list, and output from a failing test: “Testing patterns: simple fuzzing”."
%}

Here's an example of this pattern in practice.
This a test from the Mercurial codebase.
They have functions for converting from UTF&#8209;8 to binary, and back.

When they were tested with this pattern, it flushed out at least two bugs in the UTF&#8209;8 handling.
Two bugs from three lines of code.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 33,
  :alt => "Code and a bulleted list: “Testing patterns: invariants and idempotents”."
%}

Another good place to start is to look for invariants.
What doesn't change when you apply your function?
We've already seen an example of this &ndash; in our sort test, we checked that the items in the list stayed the same.
Items, size, length are all good examples &ndash; assert that your invariant properties really are invariant.

In the same vein, look for idempotent functions &ndash; functions whose effect can only be felt once.
For example, here I'm normalising text before I save it in a database.
The normalisation only needs to be applied once, so if calling it a second time changes the output, something's gone wrong.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 34,
  :alt => "Code and a bulleted list: “Testing patterns: test oracle”."
%}

The final pattern: a test oracle.

When we use random examples in our tests, we can't say exactly what the output should be when we run the example in our function &ndash; unless we have a second implementation of the function.
Then we can compare the results.

This is a really good pattern if you're refactoring or reimplementing old code.
You can ensure that both implementation have the same results, and then you know you've written a true replacement.

Also works if you can find a simpler, easier-to-check implementation that's unsuitable for production (for example, a slow but simple implementation).

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 35,
  :alt => "Slide with a bulleted list: a list of testing patterns."
%}

So that gives you a few ideas for how to get started.

But there are lots of other ways to use it, which will vary depending on your code.
What defines "correctness" in your tests?
If you can answer that, you usually have enough to start writing this sort of test.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 36,
  :alt => "Header slide: “Property-based testing with Hypothesis”."
%}

So that's property-based testing.
Rather than hard-coding our test cases, we let the computer write our examples for us.
This gets us much better coverage &ndash; trying hundreds of examples, not a handful.
It's a great way to find new bugs, but when it doesn't, it's giving us far more confidence in our code than we'd get from traditional tests.

This is something you can put into practice straight away.
You can add these to your existing unit tests immediately, and start reaping the benefits of better coverage and confidence.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 37,
  :alt => "Header slide: “Stateful testing with Hypothesis”."
%}

For part&nbsp;2, I want to push this idea a bit further.
So far, we've only looked at testing a single function &ndash; could we test something more complex?

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 38,
  :alt => "Slide with a bulleted list: “What is stateful testing?”."
%}

Most applications are large and complicated and have lots of moving parts.
They're not one-off functions that act in isolation.

Imagine a database.
We can do reads, and we can do writes.
We might test both operations in isolation, but how do we know the database works end-to-end?
How do we know there isn't some series of reads and writes that gets it into an inconsistent state?

How can we test that a program works?
We could hard-code a series of steps through the program, but we're back to square&nbsp;one.
Could we get the computer to do some randomization for us?

This is a somewhat experimental part of Hypothesis.
I haven't seen it used much in practice, but I think it's a really interesting idea.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 39,
  :alt => "Slide with a numbered list: how stateful testing works."
%}

To run a stateful test, we tell Hypothesis about the sort of actions it can run with our code &ndash; for example, it can do a database read, or a database write.
Then we tell Hypothesis what the system should look like after a given action.
This is how Hypothesis knows whether something has gone wrong &ndash; whether it's found a breaking sequence of actions.

With that set up, we let Hypothesis loose.
It tries the actions in lots of different orders, trying to find something that gets the system into an inconsistent state.
And like in part&nbsp;1, it's going to be somewhat intelligent about the failures it finds.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 40,
  :alt => "Code showing a Hypothesis test for a priority queue."
%}

So let's look at an example.

Here's a test for a simple [priority queue][pqueue].
Each item on the queue has a label and a priority.
We can add ("push") items to the queue, or get the item with the highest priority ("pop").

The `@rule` decorator tells Hypothesis about these two actions we can take, and the relevant inputs &ndash; for the push action, this means a label and a priority for the new item.
The `@precondition` decorator on the pop action tells is that we can only pop if we have a non-empty queue.
Popping from an empty queue probably gives an error, but not one that's very interesting.

Within the pop action, we're computing the most important item on the list, and then we check whether the queue returns that item.
If not, that's an error.

[pqueue]: https://en.wikipedia.org/wiki/Priority_queue

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 41,
  :alt => "Output from a Hypothesis test for a failing test with the priority queue."
%}

But what happens when Hypothesis finds an error?
This will throw an AssertionError, but out of context that's not very useful.
So that's not what Hypothesis gives us.

Instead, it gives us a series of steps that reproduce the issue.
Having an example workflow to produce the error is much more useful.
And Hypothesis applies its shrinking smarts to try to give you a small repro.
It won't necessarily be minimal, but it's usually pretty small.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 42,
  :alt => "Header slide: “Stateful testing with Hypothesis”."
%}

Letting Hypothesis drive your program is a really interesting approach.
I haven't seen many people using it yet, but I think there's a lot of potential.
I'm trying to make a conscious effort to do more of this type of testing.

(Subtext: if you are doing this, please write about it!)

*[Note: I haven't asked David, but I think some of the stateful testing work in Hypothesis is at least partially inspired by ScalaCheck.  I've been looking at Scala examples for inspiration in this area.]*

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 43,
  :alt => "Header slide: “Fuzz testing with AFL”."
%}

For the final part, I want to go back to the idea of trying to find inputs that crash your code.
There's a whole field called [fuzz testing][fuzz], often for the purposes of security.

[fuzz]: https://en.wikipedia.org/wiki/Fuzz_testing

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 44,
  :alt => "Slide with a bulleted list: “Fuzz testing”."
%}

We've already seen the procedure, which is pretty simple &ndash; fire data at a program, see if it crashes.
Hypothesis will normally do this 200&nbsp;times per test; dedicated fuzzing tools do more like thousands or millions of inputs.

There are two ways you can fuzz:

1.  Brute-force.
    Just guess what sort of inputs might be interesting, and try those.
    This is the technique used by anybody looking in from the outside, who only sees the public interface to your program.

2.  Fuzzing with feedback.
    We have a massive advantage over our adversaries, because we have our own source code.
    We can see not just whether the input causes a crash, but which path it takes through our program.

    This turns out to be a very powerful line of attack.
    Compared to the number of possible inputs, there are relatively few distinct paths through our code.
    If we could find them all, and fuzz each of them in turn, we'd be able to shake out a lot of bugs.

We're going to look at this second path.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 45,
  :alt => "Slide with a bulleted list and a picture of a rabit: “Enter american fuzzy lop (afl)”."
%}

There's a security-based fuzzer called *american fuzzy lop (afl)*.
It's written in C, and it uses this idea.
As it tries millions of inputs, it looks for inputs that trigger distinct paths through your program, and then tries genetic algorithms and the like to fuzz along each path.

Because it learns from the structure of your program, it doesn't need to be know anything about the sort of input data its testing &ndash; it can learn entirely based on how your code works.
This is very powerful, because it chooses its inputs based on what your code is actually parsing, not just what you think it does.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 46,
  :alt => "Slide with a bulleted list: “Under the covers”."
%}

So how does it do this?
How does it learn different paths?

It uses compile-time tracing.
You recompile your C program with a special version of GCC or Clang, and this inserts tracing statements.
This tracing helps it know when it's gone down a different path, and so found an interesting new category of input.

That won't work in Python, because Python isn't a compiled language.
Instead, we can use python-afl, which applies the same principle, but to Python code.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 47,
  :alt => "Code for a C program that aborts if you type the string “parrot”."
%}

Here's an example of a simple C program that reads text from stdin, and crashes if that string starts with "parrot".
We recompile it with AFl's version of GCC, and throw the fuzzer at it.
If it was only guessing randomly, it would be take a long time to get to this error &ndash; the chance of guessing this string by accident is pretty small.

We give the fuzzer a directory of inputs (I just used `helloworld`), and a directory to write its results.
Then the fuzzer goes to town.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 48,
  :alt => "Terminal output showing a fuzzing session with AFL."
%}

When AFL is running, it gives us this nice dashboard.

After just two minutes, it's already tried over a million examples, and it's just getting started.
You can imagine how many inputs it might find if you run it for hours or days, which is the typical runtime for a fuzzer.

And it's already got pretty close to our bug, having found five distinct paths through the code.
It writes out a list of "interesting" inputs that it's found, where an interesting input is one that takes you down a different code path.
So far it's found "hell", "pell", "pall", "parl" and "parr".

That gives you an idea of how powerful this is in its native state.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 49,
  :alt => "Python code for fuzzing the python-cryptography library with AFL."
%}

But we don't write C, we write Python.
Running AFL against Python code is pretty simple: you install AFL, python-afl and Cython, and then you write this sort of simple test script.

Again, our script reads from stdin, and we're passing that to a function.
This example comes from a [blog post by Alex Gaynor](https://alexgaynor.net/2015/apr/13/introduction-to-fuzzing-in-python-with-afl/), and it's testing the python-cryptography library.
This test [exposed several bugs](https://github.com/pyca/cryptography/issues/1838).

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 50,
  :alt => "Terminal output showing an AFL fuzzing session against python-cryptography."
%}

And again, we get the nice curses output, but it's much slower.
After a similar length of time to the C example, it's tried just 16,000&nbsp;examples.

Not much to be done about this &ndash; in this case, Python is just slow.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 51,
  :alt => "AFL’s trophy list: a table showing all the software with bugs found by AFL."
%}

AFL has a pretty impressive [trophy list][trophy], and this is only a third of it.
Plenty of software has been improved by testing with AFL.
It's even taken a swing at software that had already been hardened by conventional fuzzers, and dropped out several more bugs.

[trophy]: http://lcamtuf.coredump.cx/afl/

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 52,
  :alt => "Header slide: “Fuzz testing with AFL”."
%}

Fuzz testing with AFL is a great way to harden your software.
It runs for hours or days, so you don't want it in your CI suite, but a one-off run will usually drop out a fair number of bugs.

{%
  slide_image
  :deck => "hypothesis-intro",
  :slide => 53,
  :alt => "Recap slide."
%}

Summary slide.

1.  Property-based testing.
    Take your regular examples-based tests, and let the computer write your examples for you.

2.  Stateful testing.
    Tell the computer how to use your program, and let it find ways to break it.

3.  Fuzz testing with AFL.
    Give the computer a simple entry point to your program, and let it find interesting (and buggy) paths through your program.

You can get started with the property-based testing right away; the stateful testing and fuzz testing take a bit longer to get up to speed, but are definitely worth it.
I would encourage you all to try it, and if you do, please write about it!
I'd love to hear about what other people are doing, particularly with the stateful testing.

Thank you all for your time.
I hope this has been useful.

<!-- # Questions

What about flakey examples?

Sharing examples DB?

Multiple examples ine xamples DB?

not enough examples -->

