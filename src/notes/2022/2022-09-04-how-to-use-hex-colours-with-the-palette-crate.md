---
layout: note
date: 2022-09-04 11:20:59 +01:00
title: How to use hex colours with the palette crate
summary: |
  You can use `Srgb::from_str()` to parse a hexadecimal string as a colour in the palette crate.
topics:
- Rust
- Colours
---
I'm using the [Palette crate](https://docs.rs/palette/latest/palette/index.html) to do some colour work, and I want a way to take a CSS hex colour and turn it into a nicely-typed Palette colour.
I could tell that Palette is able to do this, but it took me a while to figure out how.

The examples below were written with Palette 0.7.6.

## The FromHexError enum

If you search the Palette docs [for the word `hex`](https://docs.rs/palette/latest/palette/index.html?search=hex), all the results point you to the [`FromHexError` enum](https://docs.rs/palette/latest/palette/rgb/enum.FromHexError.html):

> Error type for parsing a string of hexadecimal characters to an `Rgb` color.

This is a pretty strong clue that Palette is able to do this, but is frustratingly vague about *how*.

## Use from_str() to parse a hex code

I can't remember how, but I eventually came across the [`from_str`](https://docs.rs/palette/latest/palette/rgb/struct.Rgb.html#method.from_str) function:

<style>
  dl code {
    .n { color: var(--blue); }
    .p { color: var(--accent-grey); }
  }
</style>

<blockquote>
  <dl>
    <dt><code>fn <span class="n">from_str</span><span class="p">(</span><span class="n">hex</span><span class="p">:</span> &str<span class="p">) -> </span>Result<span class="p">&lt;</span>Self, Self<span class="p">::</span>Err<span class="p">&gt;</span></code></dt>
    <dd>
      Parses a color hex code of format ‘#ff00bb’ or ‘#abc’ (with or without the leading ‘#’) into a <code>Rgb&lt;S, u8&gt;</code> instance.
    </dd>
  </dl>
</blockquote>

Here's an example of it in practice:

```rust {"names":{"1":"std","2":"str","3":"FromStr","4":"palette","5":"FromColor","6":"Hsv","7":"Srgb","8":"main","9":"rgb","13":"hsv"}}
use std::str::FromStr;
use palette::{FromColor, Hsv, Srgb};

fn main() {
    let rgb = Srgb::from_str("#d01c11").unwrap();
    let hsv = Hsv::from_color(rgb.into_format::<f32>());

    println!("rgb = {:?}", rgb);
    println!("hsv = {:?}", hsv);
}

// rgb = Rgb { red: 208, green: 28, blue: 17, … }
// hsv = Hsv { hue: RgbHue(3.4554975), saturation: 0.9182692, value: 0.81568635, … }
```

## Use `named_from_str()` to parse CSS color names

While writing this TIL, I found there's also [a function for parsing colour names](https://docs.rs/palette/latest/palette/named/fn.from_str.html):

<blockquote>
  <dl>
    <dt><code>pub fn <span class="n">from_str</span><span class="p">(</span><span class="n">name</span><span class="p">:</span> &str<span class="p">) -> </span>Option<span class="p">&lt;</span>Srgb<span class="p">&lt;</span>u8<span class="p">&gt;&gt;</span></span></code></dt>
    <dd>Get a SVG/CSS3 color by name. Can be toggled with the <code>"named_from_str"</code> Cargo feature.<br/><br/>
    The names are the same as the constants, but lower case.</dd>
  </dl>
</blockquote>

Here's an example of it in practice:

```rust {"names":{"1":"palette","2":"FromColor","3":"Hsv","4":"palette","5":"named","6":"main","7":"rgb","11":"hsv"}}
use palette::{FromColor, Hsv};
use palette::named;

fn main() {
    let rgb = named::from_str("orange").unwrap();
    let hsv = Hsv::from_color(rgb.into_format::<f32>());

    println!("rgb = {:?}", rgb);
    println!("hsv = {:?}", hsv);
}

// rgb = Rgb { red: 255, green: 165, blue: 0, … }
// hsv = Hsv { hue: RgbHue(38.823532), saturation: 1.0, value: 1.0, … }
```