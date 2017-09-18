---
date: 2016-04-08 13:03:00 +0000
layout: post
slug: regexes-are-code
summary: Regexes have a reputation for being unreadable monsters, but it doesn't have
  to be that way.
tags: regex
title: Treat regular expressions as code, not magic
---

Regular expressions (or *regexes*) have a reputation for being unreadable.
They provide a very powerful way to manipulate text, in a very compact syntax, but it can be tricky to work out what they're doing.
If you don't write them carefully, you can end up with an unmaintainable monstrosity.

Some regexes are [just pathological][email_regex][^1], but the vast majority are more tractable.
What matters is how they're written.
It's not difficult to write regexes that are easy to read – and that makes them easy to edit, maintain, and test.
This post has a few of my tips for making regexes that are more readable.

Here's a non-trivial regex that we'd like to read:

```python
MYSTERY = r'^v?([0-9]+)(\.([0-9]+)(\.([0-9]+[a-z]))?)?$'
```

What's it trying to parse?
Let's break it down.

[^1]: Validating email addresses is a problem that you probably shouldn't try to solve with regexes.
Usually you want to know that the user has access to the address, not just that it's correctly formatted.
To check that, you need to actually send them an email – which ensures it's valid at the same time.

[email_regex]: http://www.ex-parrot.com/~pdw/Mail-RFC822-Address.html

### Tip 1: Split your regex over multiple lines

A common code smell is "clever" one-liners.
Lots of things happen on a single line, which makes it easy to get confused and make mistakes.
Since disk space is rarely at a premium (at least, not any more), it's better to break these up across multiple lines, into simpler, more understandable statements.

Regexes are an extreme version of clever one-liners.
Splitting a regex over multiple lines can highlight the natural groups, and make it easier to parse.
Here's what our regex looks like, with some newlines and indentation:

```python
MYSTERY = (
    r'^v?'
    r'([0-9]+)'
    r'('
        r'\.([0-9]+)'
        r'('
            r'\.([0-9]+[a-z])'
        r')?'
    r')?$'
)
```

This is the same string, but broken into small fragments.
Each fragment is much simpler than the whole, and you can start to understand what the regex is doing by analysing each fragment individually.
And just as whitespace and indentation are helpful in non-regex code, here they help to convey the structure – different groups are indented to different levels.

So now we have some idea of what this regex is matching.
But what was it *trying* to match?

### Tip 2: Comment your regexes

Comments are really important for the readability of code.
Good comments should explain *why* the code was written this way – what problem was it trying to solve?
<!-- Comments explain the motivation of the programmer. -->

This is helpful for many reasons.
It helps us understand what the code is doing, why it might make some non-obvious choices, and helps to spot bugs.
If we know what the code was supposed to do, and it does something different, we know there's a problem.
We can't do that with uncommented code.

Regexes are a form of code, and should be commented as such.
I like to have an overall comment that explains the overall purpose of the regex, as well as individual comments for the broken-down parts of the regex.
Here's what I'd write for our example:

```python
# Regex for matching version strings of the form vXX.YY.ZZa, where
# everything except the major version XX is optional, and the final
# letter can be any character a-z.
#
# Examples: 1, v1.0, v1.0.2, v2.0.3a, 4.0.6b
VERSION_REGEX = (
    r'^v?'                          # optional leading v
    r'([0-9]+)'                     # major version number
    r'('
        r'\.([0-9]+)'               # minor version number
        r'('
            r'\.([0-9]+[a-z]?)'     # micro version number, plus
                                    # optional build character
        r')?'
    r')?$'
)
```

As I was writing these comments, I actually spotted a mistake in my original regex – I'd forgotten the `?` for the optional final character.

With these comments, it's easy to see exactly what the regex is doing.
We can see what it's trying to match, and jump to the part of the regex which matches a particular component.
This makes it easier to do small tweaks, because you can go straight to the fragment which controls the existing behaviour.

So now we can read the regex.
How do we get information out of it?

### Tip 3: Use non-capturing groups.

The parentheses throughout my regex are *groups*.
These are useful for organising and parsing information from a matching string.
In this example:

*   The groups for minor and micro version numbers are followed by a `?` – the dot and the associated number are both optional.
    Putting them both in a group, and making them optional together, means that `v2` is a valid match, but `v2.` isn't.

*   There's a group for each component of the version string, so I can get them out later.
    For example, given `v2.0.3b`, it can tell us that the major version is `2`, the minor version is `0`, and the micro version is `3b`.

In Python, we can look up the value of these groups with the `.groups()` method, like so:

```pycon
>>> import re
>>> m = re.match(VERSION_REGEX, "v2.0.3b")
>>> m.groups()
('2', '.0.3b', '0', '.3b', '3b')
```

Hmm.

We can see the values we want, but there are a couple of extras.
We could just code around them, but it would be better if the regex only captured interesting values.

If you start a group with `(?:`, it becomes a *non-capturing group*.
We can still use it to organise the regex, but the value isn't saved.

I've changed two groups to be non-capturing in our example:

```python
# Regex for matching version strings of the form vXX.YY.ZZa, where
# everything except the major version XX is optional, and the final
# letter can be any character a-z.
#
# Examples: 1, v1.0, v1.0.2, v2.0.3a, 4.0.6b
NON_CAPTURING_VERSION_REGEX = (
    r'^v?'                          # optional leading v
    r'([0-9]+)'                     # major version number
    r'(?:'
        r'\.([0-9]+)'               # minor version number
        r'(?:'
            r'\.([0-9]+[a-z]?)'     # micro version number, plus
                                    # optional build character
        r')?'
    r')?$'
)
```

Now when we extract the group values, we'll only get the components that we're interested in:

```pycon
>>> m = re.match(NON_CAPTURING_VERSION_REGEX, "v2.0.3b")
>>> m.groups()
('2', '0', '3b')
>>> m.group(2)
'0'
```

Now we've cut out the noise, and we can access the interesting values of the regex.
Let's go one step further.

### Tip 4: Always use named capturing groups

What does `m.group(2)` mean?
It's not very obvious, unless I have the regex that `m` was matching against.
When reading code, it can be difficult to know what the value of a capturing group means.

And suppose I later change the regex, and insert a new capturing group before the end.
I now have to renumber *anywhere* I was getting groups with the old numbering scheme.
That's incredibly fragile.

There's a reason we use text, not numbers, to name variables in our programs.
If a variable has a descriptive name, the code is much easier to read, because we know what the variable "means".
And when we're writing code, we're much less likely to get variables confused.

The same logic should apply to regexes.

Many regex parsers now support *named capturing groups*.
You can supply an alternative name for looking up the value of a group.
In Python, the syntax is `(?P<name>...)` – it varies slightly from language to language.

If we add named groups to our expression:

```python
# Regex for matching version strings of the form vXX.YY.ZZa, where
# everything except the major version XX is optional, and the final
# letter can be any character a-z.
#
# Examples: 1, v1.0, v1.0.2, v2.0.3a, 4.0.6b
NAMED_CAPTURING_VERSION_REGEX = (
    r'^v?'                                # optional leading v
    r'(?P<major>[0-9]+)'                  # major version number
    r'(?:'
        r'\.(?P<minor>[0-9]+)'            # minor version number
        r'(?:'
            r'\.(?P<micro>[0-9]+[a-z]?)'  # micro version number, plus
                                          # optional build character
        r')?'
    r')?$'
)
```

We can now look up the attributes by name, or indeed access the entire collection with the `groupdict` attributed.

```pycon
>>> m = re.match(NAMED_CAPTURING_VERSION_REGEX, "v2.0.3b")
>>> m.groups()
('2', '0', '3b')
>>> m.group('minor')
'0'
>>> m.groupdict()
{'major': '2', 'micro': '3b', 'minor': '0'}
```

If I look up a group with `m.group('minor')`, it's much clearer what it means.
And if the underlying regex ever changes, the lookup is fine as-is.
Named capturing groups make our code much more explicit and robust.

### Conclusion

The tips I've suggested – significant whitespace, comments, using descriptive names – are useful, but they're hardly revolutionary.
These are all hallmarks of *good code*.

Regexes are often allowed to bypass the usual metrics of code quality.
They sit as black boxes in the middle of a codebase, monolithic strings that look complicated and scary.
If you treat regexes as code, rather than magic, you end up breaking them down, and making them more readable.
The result is always an improvement.

Regexes don't have to be scary.
Just treat them as another piece of code.
