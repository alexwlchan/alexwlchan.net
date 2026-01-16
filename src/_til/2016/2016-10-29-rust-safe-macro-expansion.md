---
layout: til
title: Rust macros are smarter than just text substitution
summary: This is a safety feature that prevents macros expanding in an unexpected way.
date: 2016-10-29 08:22:54 +00:00
tags:
  - rust
---
## The footgun in C macros

C macros are literal text substitution by the preprocessor.
The macro expression is replaced in your source code before it's compiled, which creates a footgun.
You can get unexpected results if the expression with substitutions doesn't have the operator precedence you expect.

Here's a trivial example of a C macro that gets this wrong:

```c
#define ADD_ONE(X) X + 1
ADD_ONE(9) * 2
```

What's the result?

A human might read `ADD_ONE(9)` like a function call, so expect it to be evaluated before any other operators.
They'd thus expect the result::

<pre><code>ADD_ONE(9) * 2 = 10 * 2 = <strong>20</strong></code></pre>

But the C compiler just substitutes the text into the code, and then applies operator precedence, so it goes:

<pre><code>ADD_ONE(9) * 2 = 9 + 1 * 2 = <strong>11</strong></code></pre>

The correct macro is:

```c
#define ADD_ONE(X) (X + 1)
```

This is a trivial example, but illustrates the potential confusion of C macros.

## How does Rust do better?

Rust has [declarative macros](https://doc.rust-lang.org/book/ch20-05-macros.html) which are syntax-aware, not just text substitutions.

In 2018 I wrote "Rust macros have to be self-contained expressions", but I'm not sure that's quite true.
I suspect they're more nuanced than that, but what follows is still correct.

If you try to write the C footgun macro in Rust, the compiler won't let you.
For example, the following code fails to compile with the error "no rules expected this token in macro call" on the `x`:

```rust
macro_rules! plus_one {
    ($x:expr) => $x + 1;
}
```

It won't be happy until you add the missing parentheses:

```rust
macro_rules! plus_one {
    ($x:expr) => ($x + 1);
}
```

Again, this is a trivial example, but I'm sure this mechanism protects you in more complex cases.

(I originally wrote about this [on Twitter](https://www.twitter.com/alexwlchan/status/792280535150239745), and copied it to this site in October 2025.)

<!--
```c
#include <stdio.h>

#define ADD_ONE(X) X + 1

int main() {
    printf("ADD_ONE(5) * 2 = %d\n", ADD_ONE(5) * 2);

    return 0;
}
```

```rust
macro_rules! plus_one {
    ($x:expr) => ($x + 1);
}

fn main() {
    let x = plus_one!(9) + 1;
    println!("{}", x);
}
```
-->