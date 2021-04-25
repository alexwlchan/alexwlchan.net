---
layout: post
date: 2020-05-12 06:57:53 +0000
title: Taking tuple unpacking to terrible places
summary: I want to assign a bunch of variables to True, but I don't know how many there are. Reflection to the rescue!
category: Python
tags: python
---

A week ago, I posted [a snippet of code on Twitter](https://twitter.com/alexwlchan/status/1258147811851460608) that has upset people:

{% tweet https://twitter.com/alexwlchan/status/1258147811851460608 %}

Making that tweet work requires a horrific misuse of tuple unpacking, a feature that is usually used for sensible things.
It needs reflection and the `exec()` function to work, and should never be used for anything serious.
That said, even bad ideas can have interesting things to tell us, so in this post I'm going to explain how it works and how I wrote it.

_Attention conservation notice:_ I had fun trying this idea, and writing out the notes was a useful exercise, but I don't know how much other people will get out of it.
You might find it interesting anyway, but this is probably more niche than my posts.

You can [skip to the end](#actually-useful-information) if you just want the practical lessons.

<figure>
  <img src="/images/2020/shattered_mirror.jpg" alt="A side view mirror from a car, shattered and bent lying on the pavement.">
  <figcaption>
    Superstition says breaking a mirror will bring seven years of bad luck.
    Sensibility says overusing reflection will bring seven years of filthy looks from everybody who has to maintain your code.
    Image by <a href="https://www.flickr.com/photos/seishin17/5602797265">Kristopha Hohn on Flickr</a>, used under CC&nbsp;BY-SA.
  </figcaption>
</figure>



## What is tuple unpacking?

Many programming languages support [*parallel assignment*](https://en.wikipedia.org/wiki/Assignment_(computer_science)#Parallel_assignment), which allows you to set multiple variables at once:

```
longitude, latitude = 51.9, -0.2
```

This will set `longitude` to `51.9`, and `latitude` to `-0.2`.
It's a more concise version of

```
longitude = 51.9
latitude = -0.2
```

This is often used in Python to return multiple values from a single function:

```python
def get_position():
    return 51.9, -0.2

longitude, latitude = get_position()
```

Another name for this is *tuple unpacking*.
The structures `longitude, latitude` and `51.9, -0.2` are both Python tuples -- the parentheses you often write around tuples are optional.

For tuple unpacking to work, you need to have the same number of variables on the left-hand side as elements on the right, so they can be paired up together.
If they don't match, you get an error.
For example:

```pycon
>>> longitude, latitude, altitude = 51.9, -0.2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: too many values to unpack (expected 3)
```

The details of tuple unpacking could be a whole other blog post; here it's sufficient to know that this feature exists and you need to balance both sides for it to work.



## Where did this idea come from?

Here's a conversation from a group chat last week (shared with permission):

> [Sean](https://twitter.com/sgsabbage): I just wrote a boolean as 'Trues' <br/>
> [Kathy](https://twitter.com/kapellosaur): You should be able to use that as tuple unpacking <br/>
> [Kathy](https://twitter.com/kapellosaur): a, b, c, d = Trues <br/>
> [Sean](https://twitter.com/sgsabbage): :D

We all had a laugh, briefly discussed what dark magic it might take to pull this off, and then conversation moved on.
It wasn't until the evening, when I was on my daily walk, that gears began to turn in my brain and I thought about how you might actually do this.

Remember that tuple unpacking only works if you have the same number of elements on both sides.
This means that `Trues` has to return the same number of elements as there are variables on the left-hand side -- in this example, four -- and the number of variables can vary.

The only way this can work is if `Trues` can dynamically resize itself to be the correct length.
So this boils down to the following question: **how can a function know the length of the tuple it's being unpacked into?**

To make this work, such a function needs to be able to see the source code where it's being called.
This is a technique called [reflection](https://en.wikipedia.org/wiki/Reflection_(computer_programming)), where a program can read or modify its own source code.

Anything involving reflection and parsing source code is prone to be fiddly, so I actually wrote _four_ implementations, each less buggy than the last.
We could jump straight to the end, but let's go through all of them in turn to see how I tried to tackle the problem.



## Attempt #1: the trouble with tracebacks

If you've used Python for any length of time, you've probably seen an example of reflection-like behaviour, even if you didn't realise it.
Consider the following program:

```python
# divide_by_zero.py
def divide(x, y):
    return x / y

result = divide(1, 0)
```

If you run this code, it throws an exception and you get a stack trace:

```
Traceback (most recent call last):
  File "divide_by_zero.py", line 4, in <module>
    result = divide(1, 0)
  File "divide_by_zero.py", line 2, in divide
    return x / y
ZeroDivisionError: division by zero
```

This is meant to help us debug a broken program -- if something goes wrong, it gives us a clue about where the problem is.
The stack trace tells us what code was executing when the exception was thrown, including the filename, line number and line of code.

Normally stack traces are used in the context of error handling, but there's no reason you can't look at them elsewhere -- for example, if you wanted to work out where a function was being called from.
The information is usually printed to stderr for a human to read, but we can also capture the current stack trace by calling [`extract_stack()`](https://docs.python.org/3/library/traceback.html#traceback.extract_stack) from the [traceback module](https://docs.python.org/3/library/traceback.html).

Observe:

```python
import traceback

def Trues():
    for frame_summary in traceback.extract_stack():
        print(frame_summary)
        print(repr(frame_summary.line))
        print("")

    return True, True

a, b = Trues()
```

If you run this code, this is what you get:

```
<FrameSummary file horror1.py, line 11 in <module>>
'a, b = Trues()'

<FrameSummary file horror1.py, line 4 in Trues>
'for frame_summary in traceback.extract_stack():'
```

That `a, b = Trues()` line is what we want -- it tells us where this function is being called, and what it's being expanded into.
We can do some naive string parsing on this line to work out how many variables there are on the left-hand side:

```python
# Find the line where this function is called
calling_code = traceback.extract_stack()[0].line

# The line will be something like ``a, b = Trues()``.
# Count variables on the left-hand side.
trues_count = len(calling_code.split("=")[0].split(","))
```

Then we return that number of Trues:

```python
import traceback

def Trues():
  # Find the line where this function is called
  calling_code = traceback.extract_stack()[0].line

  # The line will be something like ``a, b = Trues()``.
  # Count variables on the left-hand side.
  trues_count = len(calling_code.split("=")[0].split(","))

  return [True] * trues_count

a, b = Trues()
print(a, b)  # True True

a, b, c, d = Trues()
print(a, b, c, d)  # True True
```

Hooray!
We've got it working, and we can pat ourselves on the back for a job terribly done.
Let's all go ho---wait a minute, there's a problem.
(And no, not just the existence of this code.)

Python allows you to split statements over multiple lines.
For example, this is valid Python:

```python
a, b, \
c, d = 1, 2, 3, 4
```

If you try to use `Trues()` with a tuple definition that's split over multiple lines, you get an error:

```python
a, b, \
c, d = Trues()
```

```
Traceback (most recent call last):
  File "horror1.py", line 14, in <module>
    c, d = Trues()
ValueError: not enough values to unpack (expected 4, got 2)
```

If you look at the traceback, you see it only knows about the last line of the assignment -- the `a, b, \` from the previous line has been omitted.
This is annoying for our use case, but it makes sense in the context of stack traces -- the line of code in the stack trace is a clue, rather than a complete program.
Limiting to a single line keeps the stack trace readable.



## Attempt #2: exec()-utive dysfunction

Let's try to add support for multi-line expressions.
I wrote this code at 11pm, and this approach wasn't the most sensible choice, but it's what I tried first.

Since traceback only gives us one line, we have to get the remaining lines ourselves.
The traceback does tell us the number of the line that was executing, so let's open the file and read all the lines up to that one:

```python
import itertools

def Trues2():
  # Find the line where this function is called
    current_frame = traceback.extract_stack()[0]

    # Read all the lines up to the point where ``Trues2()`` is
    # called from.
    with open(current_frame.filename) as srcfile:
        lines = list(itertools.islice(srcfile, current_frame.lineno))

    ...
```

(This code could throw a memory error if the source file is exceptionally large, but that's the least of our problems.)

So we know that the code on `current_frame.lineno` is part of the assignment that calls `Trues2()`.
Are any of the preceding lines?

One (very bad) way to do this would be to work backwards through the file, including more and more lines until we find something that can't be a valid assignment expression.
First we grab the single line from the traceback.
Then we grab that line, and the line before it.
Then we grab those two lines, and the line before them.
And so on, until we realise we've taken too much.

How do we know if something is a valid assignment?
We could use a proper parser, or we could cheat and use [the `exec()` function](https://docs.python.org/3/library/functions.html#exec) to parse the code for us.
This function can dynamically execute Python code, so we can use it to see if this is an assignment expression.

It's useful in a pinch, but be very careful using it -- in particular, never pass untrusted input to `exec()`.
And even if you completely trust the input to `exec()`, be careful -- it can have side-effects.
For example, running `exec('a = 1')` will happily overwrite whatever value you previously had in `a`, and it's easy to imagine even more destructive possibilities.

Let's work back through `lines`, grabbing more and more lines until something goes wrong.

When we get a snippet that includes a NameError or a SyntaxError, we know we're looking at a line that isn't part of this assignment expression:

```python
def Trues2():
    ...
    def dummy_trues():
        return [True]

    for line_count in range(1, len(lines)):
        # Remove any leading whitespace to get around indentation issues
        src = "\n".join([l.strip() for l in lines[-line_count:]])

        try:
            # We have to pass a definition for Trues2(), even not if
            # the right one, otherwise it'll use the top-level function,
            # and then you get a recursion error.
            exec(src, {"Trues2": dummy_trues})

        except (NameError, SyntaxError):
            src = "\n".join([l.strip() for l in lines[-line_count+1:]])
            break

        # If the dummy_trues() function guessed the wrong number of True's,
        # the exec() will throw a ValueError.  If it guessed right, the
        # code will execute successfully.
        except ValueError:
            pass
        else:
            pass
    ...
```

An example would probably be helpful.
Let's suppose our program was

```python
def Trues2():
    ...
    return

a, b, \
c, d = Trues2()
```

Then the loop would go as follows:

*   src: `c, d = Trues2()`.

    This is a valid Python snippet, but running it inside `exec()` throws a ValueError.
    The version of `Trues2()` inside the `exec()` returns a list with 1 True, not 2.

*   src: `a, b, \\n c, d = Trues2()`.

    As before, this is a valid Python snippet that throws a ValueError inside `exec()`.

*   src: `return\n a, b \\n c, d = Trues2()`.

    This snippet throws a SyntaxError: _"'return' outside function"_, so we know we've captured too much.
    Backtrack one line: the source code of the expression is `a, b \\n c, d = Trues2()`.

Once we have the complete assignment, we need to work out how many things to unpack it into.
We could use the naive string manipulation from the previous attempt, or we take our `exec()`-shaped hammer and use it again.

If you look at the code above, you see we have to pass a definition for `Trues2()` into the namespace of `exec()`; otherwise we get a recursion error.
If it returns the wrong number of `True`'s, you get a ValueError.
We can exploit this to find the correct number of `True`'s, by counting up until we stop getting ValueError's:

```python
def Trues2():
    ...
    for true_count in itertools.count(start=1):
        result = [True] * true_count

        def guessed_trues():
            return result

        try:
            exec(src, {"Trues2": guessed_trues})
        except:
            pass
        else:
            return result
```

Here we've taken one bad idea (using `exec()`) and added a second bad idea (an infinite loop).
This is what people mean by [composition](https://en.wikipedia.org/wiki/Function_composition_(computer_science)), right?

But there's another type of multi-line expression you can write, which this code fails to parse correctly.
In Python, any expression inside parentheses can be split across multiple lines:

```python
(a, b
c, d) = Trues2()
```

If you try to run this code, it hangs forever.

The problem is the last line `c, d) = Trues2()`.
This isn't syntactically valid, so trying to `exec()` it throws a SyntaxError.
Because of a bug in the backtracking logic, the loop guesses that the assignment is the whole file, and tries to `exec()` it inside the itertools loop.
It always fails, because the definition of Trues2() passed into the `exec()` namespace gets replaced by the one in the file.

The fix is to keep track of whether we've seen a syntactically valid group of lines yet, and only stop after that's happened:

```python
def Trues2():
    ...
    def dummy_trues():
        return [True]

    have_seen_valid_lines = False

    for line_count in range(1, len(lines)):
        # Remove any leading whitespace to get around indentation issues
        src = "\n".join([l.strip() for l in lines[-line_count:]])
        try:
            # We have to pass a definition for Trues2(), even not if
            # the right one, otherwise it'll use the top-level function,
            # and then you get a recursion error.
            exec(src, {"Trues2": dummy_trues})

        except (NameError, SyntaxError) as err:
          if have_seen_valid_lines:
              src = "\n".join([l.strip() for l in lines[-line_count+1:]])
              break

        # If the dummy_trues() function guessed the wrong number of True's,
        # the exec() will throw a ValueError.  If it guessed right, the
        # code will execute successfully.
        except ValueError:
            have_seen_valid_lines = True
        else:
            have_seen_valid_lines = True
    ...
```

Let's step through this example again:

```python
def Trues2():
  ...

(a, b,
c, d) = Trues2()
```

Now the loop would go as follows:

*   src: `c, d) = Trues2()`.

    This isn't a valid Python snippet; it throws a SyntaxError.
    Try grabbing the next line up.

*   src: `(a, b, \n c, d) = Trues2()`.
    This is a valid Python snippet, but running it in `exec()` is is a ValueError.

*   src: `return result \n (a, b, \n c, d) = Trues2()`.

    This isn't a valid snippet, exec()-ing it throws a SyntaxError, and we've already seen some valid Python.
    Backtrack one line: the source code of the expression is `(a, b, \n c, d) = Trues2()`.

Putting this all together:

```python
import itertools
import traceback

def Trues2():
    # Find the line where this function is called
    current_frame = traceback.extract_stack()[0]

    # Read all the lines up to the point where ``Trues2()`` is
    # called from.
    with open(current_frame.filename) as srcfile:
        lines = list(itertools.islice(srcfile, current_frame.lineno))

    # Work backwards through the lines from where ``Trues2()`` is called
    # to find the maximal chunk of Python code that ends at the point
    # where the function is called.
    def dummy_trues():
        return [True]

    have_seen_valid_lines = False

    for line_count in range(1, len(lines)):
        # Remove any leading whitespace to get around indentation issues
        src = "\n".join([l.strip() for l in lines[-line_count:]])
        try:

            # We have to pass a definition for Trues2(), even not if
            # the right one, otherwise it'll use the top-level function,
            # and then you get a recursion error.
            exec(src, {"Trues2": dummy_trues})

        # Either of these mean we've captured too much, so this
        # isn't the assignment expression -- backtrack.
        except (NameError, SyntaxError) as err:
          if have_seen_valid_lines:
              src = "\n".join([l.strip() for l in lines[-line_count+1:]])
              break

        # If the dummy_trues() function guessed the wrong number of True's,
        # the exec() will throw a ValueError.  If it guessed right, the
        # code will execute successfully.
        except ValueError:
            have_seen_valid_lines = True
        else:
            have_seen_valid_lines = True

    # Now we've got the complete assignment expression (probably),
    # start increasing the number of True's we return until we
    # stop getting ValueErrors.
    for true_count in itertools.count(start=1):
        result = [True] * true_count

        def guessed_trues():
            return result

        try:
            exec(src, {"Trues2": guessed_trues})
        except:
            pass
        else:
            return result

a, b = Trues2()
print(a, b)

a, b, c, d = Trues2()
print(a, b, c, d)

a, b, \
c, d = Trues2()
print(a, b, c, d)

(a, b,
c, d) = Trues2()
print(a, b, c, d)
```

This is the version of the code I tweeted, for maximum horror.

This code is doubly cursed: gratuitous use of `exec()` and the potential for an infinite loop.
It's Bad Idea Central, and it's also pretty fragile.
If you play around with this, you'll quickly find other cases where the line detection breaks, and the code gets stuck in an infinite loop.

Sometimes `exec()` has its uses (for example, it's how namedtuples are constructed in the collections module), but parsing arbitrary source code is definitely not one of them.

We could continue to patch this code to cover more edge cases and issues, but it's clear we're flogging a dead horse.
Applying raw string manipulation to parse source code for anything but the simplest syntax is going to get horrifically complicated.
It's time to use a proper parser.



## Attempt #3: staring in abstract horror

When Python runs your program, it starts by parsing your source code into an [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) (AST).
This represents the structure of the program, rather than the exact characters in the file.
If we can inspect the AST, we can understand what we're unpacking into much more reliably.

I should note that I'm firmly out of my depth here.
I know that ASTs are a thing and they're the "right" way to parse source code, but I've never used them in anger.

Python has an [ast module](https://docs.python.org/3/library/ast.html#ast.AST) for working with abstract syntax trees, but I don't really know where to use it.
I did find the *executing* Python library that gets [the currently executing AST node](https://github.com/alexmojaki/executing), which seems like a useful starting point.

We have to use the [inspect module](https://docs.python.org/3/library/inspect.html) instead of traceback to get the current frame, and then pass it to this library to get the AST node:

```python
import inspect

import executing

def Trues3():
    # Get the AST node for the function call to Trues3()
    frame = inspect.currentframe()
    current_frame = inspect.getouterframes(frame)[1].frame
    node = executing.Source.executing(current_frame).node

a, b = Trues3()
```

I don't really know much about AST nodes or how they work, so once I'd got a node out, I did a lot of poking around with functions like `type(…)` and `dir(…)`.

Calling `type(mystery)` tells us the type of `mystery`.
Calling `dir(mystery)` tells us all the methods and attributes on `mystery`.
Both of these can help us understand how to use unfamiliar types and objects.
I couldn't find any documentation for the different types of AST node, but using these functions allowed me to find everything I needed.

They tell me that this node is an `ast.Call`, which seems to represents where we're calling `Trues3()` -- in this case, the right-hand side of an expression `… = Trues3()`.

This node has an attribute `.parent`.
By grabbing that and inspecting the type, I found an `ast.Assign` node.
This represents an assignment; that is, an expression of the form `X = Y`:

```python
def Trues3():
    ...
    assert isinstance(node, ast.Call)

    assign_node = node.parent
    assert isinstance(assign_node, ast.Assign)
```

The Assign node has an attribute `.targets` which is a list.
I assume the list can have more than one entry, but in practice I never saw it have more than one.
Entries were things like `<_ast.List object at 0x102312b90>` or `<_ast.Tuple object at 0x104da9b90>`.

Let's grab that value:

```python
def Trues3():
    ...
    target = assign_node.targets[0]
```

And then we count how many entries it contains, and use that to assemble the result:

```python
import ast
import inspect

import executing

def Trues3():
    # Get the AST node for the function call to Trues3()
    frame = inspect.currentframe()
    current_frame = inspect.getouterframes(frame)[1].frame
    calling_node = executing.Source.executing(current_frame).node
    assert isinstance(calling_node, ast.Call), calling_node

    assign_node = calling_node.parent
    assert isinstance(assign_node, ast.Assign), assign_node

    target_node = assign_node.targets[0]
    assert isinstance(target_node, (ast.List, ast.tuple)), target_node

    return [True] * len(target.elts)

a, b = Trues3()
print(a, b)

a, b, c, d = Trues3()
print(a, b, c, d)
```

This is significantly shorter than the version where we're parsing the source file itself, and without any nasty use of `exec()` or infinite loops!
Hooray, we're finally done.



## Attempt #4: Ye gods, she's still going?

Once you start using the AST, there's scope to handle more interesting expressions.
Tuple unpacking allows you to put more complex, nested expressions on the left-hand side (although if you're doing this in practice, you might want to think about breaking up the expression over multiple lines).

You can make all of the following work in a fairly sensible way:

```python
a = Trues4()
a, b = Trues4()
a, b, c = Trues4()

a, b, \
c, d = Trues4()

(a, b,
c, d) = Trues4()

a, b = Trues4(), Trues4()
(a, b), (c, d, e) = Trues4(), Trues4()

a, *b, c = Trues4()
```

I'm not going to explain them all, but here's the relevant source code:

```python
import ast
import inspect
import secrets

import executing

def truthify(node):
    if isinstance(node, ast.Name):
        return True

    result = []
    for entry in node.elts:
        if isinstance(entry, ast.Name):
            result.append(True)
        elif isinstance(entry, (ast.List, ast.Tuple)):
            result.append(truthify(entry))
        elif isinstance(entry, ast.Starred):
            result.extend([True] * secrets.randbelow(100))
        else:
            raise RuntimeError(f"Unrecognised AST node: {entry}")

    return result

def Trues4():
    # Get the AST node for the function call to Trues3()
    frame = inspect.currentframe()
    current_frame = inspect.getouterframes(frame)[1].frame

    try:
        calling_node = executing.Source.executing(current_frame).node
    except AttributeError as err:
        # e.g. a = Trues4()
        if err.args == ("'Name' object has no attribute 'elts'",):
            return True
        else:
            raise

    assert isinstance(calling_node, ast.Call)

    if isinstance(calling_node.parent, ast.Assign):
        assign_node = calling_node.parent
        target = assign_node.targets[0]

        return truthify(target)

    # Handle expressions of the form (a, b) = (Trues4(), Trues4())
    elif isinstance(calling_node.parent, ast.Tuple):
        index_in_tuple = calling_node.parent.elts.index(calling_node)
        assign_node = calling_node.parent.parent

        return truthify(assign_node.targets[0].elts[index_in_tuple])

    else:
        raise RuntimeError(f"Unrecognised calling node parent: {calling_node.parent}")
```



## What next?

There's one thing I didn't manage to get working.
If you look back at the original chat message, the suggestion was to use a standalone variable, not a function:

```python
a, b, c, d = Trues
```

It should be possible to make this work, by shoving all the interesting logic inside the `__iter__` method of the `Trues` object.
This is the method that gets called when Python tries to iterate over something; for example, when it's trying to extract something to unpack it into a tuple.

Here's a minimal example of how you could set up that `__iter__` method:

```python
class Truthiness:
    def __iter__(self):
        yield from [True, True, True, True]

Trues = Truthiness()

a, b, c, d = Trues
print(a, b, c, d)
```

If you could get the interesting logic running inside that method, you'd match the original idea perfectly.

Unfortunately, the *executing* library can't find the current AST node if you try this.
Poking around a bit, there's an `UNPACK_SEQUENCE` operation in the Python bytecode, and the library doesn't know how to turn that into an AST node.
I briefly considered trying to patch the library, but I'm so out of my depth it didn't seem worth the effort.

Exercise for the reader!



## Actually useful information

Although this sort of dynamic tuple unpacking is terrible and using it in production would be an act of corporate sabotage, there are some useful things we can learn from this exercise:

*   The [traceback](https://docs.python.org/3/library/traceback.html) and [inspect](https://docs.python.org/3/library/inspect.html) modules can tell us what code is executing right now.
    In particular `traceback.extract_stack()` and `inspect.currentframe()`.

*   We can use `exec()` to execute arbitrary Python code.
    Be careful doing this, especially with untrusted input or code that might have side-effects.

*   Abstract syntax trees (ASTs) can tell us about the structure of a program, and skip the exact formatting of the source code.
    We can use the [executing library](https://pypi.org/project/executing/) to get the currently executing AST node.

*   Calling `type(mystery)` tells us the type of `mystery`.
    Calling `dir(mystery)` tells us all the methods and attributes on `mystery`.
    Both of these can help us understand how to use unfamiliar types.

*   Python calls the `__iter__` method on an object when it tries to iterate over it; for example, when it's trying to extract elements to unpack into a tuple.

Learning useful stuff is part of why I experiment with bad ideas (previously: [exhibit A](/2020/04/using-dynamodb-as-a-calculator/), [exhibit B](/2019/12/yaml-impossible/)).

Trying to do something like dynamic tuple unpacking forces me to be creative.
I have to think about how to do something that was never intended to be possible, and I end up learning about things that I'd never have encountered otherwise.
The final code is unusable as soon as it's written; the new ideas I discover along the way last a lot longer.
