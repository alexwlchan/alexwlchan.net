---
layout: post
date: 2021-12-10 21:36:55 +0000
title: The ever-improving error messages of Rust
summary: An improvement to Rust's error handling that I almost reported, until I realised it was fixed.
tags:
  - rust
  - error messages
---

In [my last-but-one post](/2021/dominant-colours/), I mentioned the quality of Rust's compiler errors.
I encountered another compiler error today that I thought was less-than-optimal, I was going to file an issue for it… then I discovered it's been fixed in a newer version of Rust.
Nice!

I've been writing a lot of Scala this week, and Scala uses s-prefixed strings for [string interpolation].
For example:

```scala
val name = "Alex"
println(s"Hello, $name")  // Hello, Alex
```

And so when I came to write some Rust, that s-prefix crept into my strings:

```rust
let name = "Alex";
println!(s"Hello, {}!", name);
```

If you compile that code with the 2018 edition of Rust, this is the error you get:

<pre>
<code><span class="rustc_error">error:</span> <span style="font-weight: bold;">expected `,`, found `"Hello, {}!"`</span>
 <span class="rustc_lineno">--></span> src/main.rs:3:15
  <span class="rustc_lineno">|</span>
<span class="rustc_lineno">3 |</span>     println!(s"Hello, {}!", name);
  <span class="rustc_lineno">|</span>               <span class="rustc_error">^^^^^^^^^^^^ expected `,`</span></code></pre>

Although it knows there's an issue somewhere on this line, it's highlighting everything *except* the erroneous prefix.
I did work out what I'd done wrong, but not after a bit of head-scratching.

I was going to suggest tweaking Rust's output to highlight this sort of erroneous prefix -- string prefixes are used in lots of languages ([including Rust itself][raw_strings]), so I'm surely not the first person to make this mistake.
The [issue template] asks you to include a runnable example on play.rust-lang.org, and that's where I discovered this has already been fixed.

If you compile that code with the 2021 edition of Rust, you get three errors -- and the first of them highlights this prefix.

<pre>
<code><span class="rustc_error">error:</span> <span style="font-weight: bold;">prefix `s` is unknown</span>
 <span class="rustc_lineno">--></span> src/main.rs:3:15
  <span class="rustc_lineno">|</span>
<span class="rustc_lineno">3 |</span>     println!(s"Hello, {}!", name);
  <span class="rustc_lineno">|</span>              <span class="rustc_error">^ unknown prefix</span>
  = <span style="font-weight: bold;">note:</span> prefixed identifiers and literals are reserved since Rust 2021</code></pre>

Small improvements like this don't fundamentally change the language or what it can do, but they do add up to a much more pleasant experience as a programmer.

[string interpolation]: https://docs.scala-lang.org/overviews/core/string-interpolation.html
[raw_strings]: https://stackoverflow.com/q/26611664
[issue template]: https://raw.githubusercontent.com/rust-lang/rust/master/.github/ISSUE_TEMPLATE/diagnostics.md
