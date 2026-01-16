---
layout: til
date: 2024-05-12 11:46:34 +01:00
title: Get a Palette colour as a command-line argument with Clap
summary: |
  Wrapping a `Palette:Srgb` in a struct and implementing `FromStr` for the struct allows you to take hexadecimal colours as command-line inputs.
tags:
  - rust
  - rust:clap
  - rust:palette
  - colour
---
I was writing a command-line tool using the [Clap crate](https://docs.rs/clap/latest/clap/index.html), and I wanted to be able to pass a hexadecimal string as an argument and have it be parsed as a [Palette colour](https://docs.rs/palette/latest/palette/).
Some of this work might be reusable if I ever want to parse different types with Clap.

These examples use Clap 4.5.4 and Palette 0.7.6.

## Parsing a string argument as a Rust type

Clap uses the [`ValueParser` trait](https://docs.rs/clap/latest/clap/builder/struct.ValueParser.html) to convert a raw argument value into a typed value.
It has built-in implementations of this trait for certain common types.

For example, here's a simple program that takes a single argument which is validated as and converted to a `usize`:

```rust
use clap::{Arg, Command};

fn main() {
    let arg = Arg::new("count")
                  .value_parser(clap::value_parser!(usize));

    let m = Command::new("My Program")
                    .arg(arg)
                    .get_matches();

    let count: &usize = m.get_one::<usize>("count").unwrap();

    println!("count = {}", count);
}

// $ cargo run 42
// count = 42
```

## Parsing a string argument as a custom type

Initially I was looking at how to implement `ValueParser` for the `Srgb` type, but then I came across a [Reddit post by Kbknapp](https://www.reddit.com/r/learnrust/comments/115ldw2/comment/j92ziu6/) that suggested instead implementing `FromStr`.

Initially I considered writing my own wrapper type and implementing `FromStr` myself, but then I remember that I can use `from_str()` [to parse hex codes as Palette colours](/til/2022/how-to-use-hex-colours-with-the-palette-crate/), which means it already implements `FromStr` -- I get the behaviour I want "for free":

```rust
use clap::{Arg, Command};
use palette::Srgb;

fn main() {
    let arg = Arg::new("wrapper")
                  .value_parser(clap::value_parser!(Srgb<u8>));

    let m = Command::new("My Program").arg(arg).get_matches();

    let wrapper: &Srgb<u8> = m.get_one::<Srgb<u8>>("wrapper").unwrap();

    println!("color = {:?}", wrapper);
}

// $ cargo run '#d01c11'
// color = Rgb { red: 208, green: 28, blue: 17, … }
```

Initially I thought I'd have to write my own wrapper struct and implement `FromStr` on it, but then I realised I can just use the implementation of `FromStr` that's provided by Palette.

You can't implement traits for types defined outside the current crate, so a wrapper struct would be useful if I ever want to do this with a type that doesn't already implement `FromStr`.
