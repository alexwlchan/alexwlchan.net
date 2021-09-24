---
layout: post
date: 2021-09-22 07:56:04 +0000
title: Operations on strings don't always commute
summary: Is uppercasing then reversing a string the same as reversing and then uppercasing? Of course not.
tags: unicode
---

<!-- https://twitter.com/jpwarren/status/1440152993693777924 -->

Earlier today, I saw a tweet linking to the [ButFirst module][module], a Perl module that lets you run a block of code before something else.
For example:

```perl
# Print a greeting, but first find caffiene.
{
    print "Good morning!\n";
} but first {
    print "I need a coffee\n";
}
```

This is a bad idea, which the README acknowledges as such (*"Any use of this module should be considered a bug"*) -- but I love fun stuff like this.

I was particularly struck by the last example in the README:

```perl
while (<>) {
    print;
} butfirst {
    $_ = reverse $_;
} butfirst {
    $_ = uc $_;
}
```

This prints a series of lines, with each line reversed and uppercased -- but in which order?
The README explains in a comment, but I think it's somewhat ambiguous – I could interpret this as reversing first, or uppercasing first.

That got me wondering: does it matter?
Reversing a string and uppercasing a string should be completely orthogonal operations, so we should be able to swap the order with impunity.
(This is called [commutativity].)
That seems reasonable, right?

But strings are rarely reasonable – there are lots of weird corners of Unicode where strings do unexpected things.
Are there strings where upper(reverse(s)) ≠ reverse(upper(s))?

I tried a few examples by hand with [combining characters] and didn't get anywhere useful, so I wrote a test to have [Hypothesis] search for interesting examples instead.
([Source code](/files/2021/test_for_noncommutative_strings.py))
It tried a few hundred examples, then stumbled upon a string where uppercasing and reversing don't commute:

```
>>> 'ﬁ'.upper()[::-1]
'IF'
>>> 'ﬁ'[::-1].upper()
'FI'
```

Python is uppercasing the `ﬁ` ligature to `FI`, which is correct if you follow the [Unicode spec][fi_spec], and feels intuitively fine – but proves that we can't swap the order of these string operations.

Perl's `uc` function doesn't seem to be Unicode aware, so uppercasing `ﬁ` returns the same string unmodified.
I did write [another test](/files/2021/test_for_noncommutative_strings_in_perl.py) to try to find strings where you can't swap uppercasing/reversing in Perl, but it couldn't find any examples.
Maybe these operations are safe to swap in Perl (but I wouldn't bet on it).

Either way, this is another reminder that strings can behave in decidedly unintuitive ways.
Unicode is complicated, and I only know a fraction of the rough edges.

[module]: https://metacpan.org/pod/Acme::ButFirst
[combining characters]: https://en.wikipedia.org/wiki/Combining_character
[Hypothesis]: https://github.com/HypothesisWorks/hypothesis
[commutativity]: https://en.wikipedia.org/wiki/Commutative_property
[fi_spec]: https://util.unicode.org/UnicodeJsps/character.jsp?a=FB01
