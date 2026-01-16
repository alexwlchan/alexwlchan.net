---
layout: til
title: Use `std::io::IsTerminal` to detect if you're running in the terminal in Rust
summary: This allows me to suppress ANSI escape codes if the output is going somewhere other than the terminal.
date: 2024-10-06 10:58:31 +01:00
tags:
  - rust
---
In my [`dominant_colours` tool](https://github.com/alexwlchan/dominant_colours), I use ANSI escape sequences to print coloured text to the console.
I to detect if my code was running in the terminal, or if it was running in a non-terminal environment where those escape codes would be unhelpful (e.g. being redirected to a file).

I found a [Stack Overflow answer](https://stackoverflow.com/a/76979724/1558022) that suggested using [`std::io::IsTerminal`](https://doc.rust-lang.org/std/io/trait.IsTerminal.html), which worked perfectly.
Here's a simple example:

```rust
use std::io::IsTerminal;

fn main() {
    if std::io::stdout().is_terminal() {
        println!("This text is \x1b[0;31mred\x1b[0m and \x1b[0;34mblue\x1b[0m");
    } else {
        println!("This text is not coloured");
    }
}
```

I added this to `dominant_colours` in [pull request #65](https://github.com/alexwlchan/dominant_colours/pull/65).
