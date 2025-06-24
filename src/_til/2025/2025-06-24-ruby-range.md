---
layout: til
title: Ruby's range can iterate over more than just numbers
date: 2025-06-24 04:50:58 +0100
summary: You can iterate over a range between two `String` values, because Ruby's `String` does intelligent increments of alphanumeric strings.
tags:
  - ruby
---
I was writing some Ruby code recently, and in particular I wanted to write some [ranges](https://ruby-doc.org/core-2.5.1/Range.html).
The basic usage is pretty simple, and matches what I'm used to from other programming languages -- iterate between two numbers:

```irb
irb(main):001> (1..5).each { |i| puts i.inspect }
1
2
3
4
5
=> 1..5
```

But then I discovered that Ruby's `Range` is more flexible than I realised.



## You don't need numbers as inputs

I was getting the start/end of my range as strings, and I thought I'd have to convert them to numbers first.
I was surprised when my code worked first time, and didn't throw a type error -- Ruby can iterate between two strings, and give you string values between them:

```irb
irb(main):002> ("1".."5").each { |i| puts i.inspect }
"1"
"2"
"3"
"4"
"5"
=> "1".."5"
```

This is clearly something to do with string codepoints -- for example, I can iterate between two ASCII values:

```irb
irb(main):003> ("a".."e").each { |i| puts i.inspect }
"a"
"b"
"c"
"d"
"e"
=> "a".."e"
```

or two UTF-8 values:

```irb
irb(main):004> ("ç".."ë").each { |i| puts i.inspect }
"ç"
"è"
"é"
"ê"
"ë"
=> "ç".."ë"
```

Even more surprising to me, this isn't limited to single characters -- you can also iterate over numeric ranges this way.

```irb
irb(main):005> ("101".."105").each { |i| puts i.inspect }
"101"
"102"
"103"
"104"
"105"
=> "101".."105"
```

How does this work?



## Ruby strings have a notion of "successor"

The [documentation for `Range`](https://ruby-doc.org/core-2.5.1/Range.html) gives a clue about what's going on (emphasis mine):

> Ranges can be constructed using any objects that can be compared using the `<=>` operator. Methods that treat the range as a sequence (`each` and methods inherited from `Enumerable`) **expect the begin object to implement a `succ` method to return the next object in sequence**. The `step` and `include?` methods require the begin object to implement succ or to be numeric.

The `succ` method returns the "successor" of a value, and [`String#succ`](https://www.rubydoc.info/stdlib/core/2.0.0/String:succ) is aware of numeric sequences, so it's able to increment them intelligently.
Here's the description from the Ruby docs:

> Returns the successor to `str`. The successor is calculated by incrementing characters starting from the rightmost alphanumeric (or the rightmost character if there are no alphanumerics) in the string. Incrementing a digit always results in another digit, and incrementing a letter results in another letter of the same case. Incrementing nonalphanumerics uses the underlying character set’s collating sequence.
>
> If the increment generates a “carry,” the character to the left of it is incremented. This process repeats until there is no carry, adding an additional character if necessary.
>
> ```ruby
> "abcd".succ        #=> "abce"
> "THX1138".succ     #=> "THX1139"
> "<<koala>>".succ   #=> "<<koalb>>"
> "1999zzz".succ     #=> "2000aaa"
> "ZZZ9999".succ     #=> "AAAA0000"
> "***".succ         #=> "**+"
> ```
