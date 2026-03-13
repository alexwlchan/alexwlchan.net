---
layout: note
date: 2026-03-13 21:53:42 +00:00
title: My randline project is tested by Crater
summary: I got a GitHub issue warning me that my project will break with a future version of Cargo.
topic: Rust
---

One of the tools used by the Rust development team is [Crater][crater], a tool which can compile and test Rust crates en masse.
It's used to detect breaking changes in the compiler, by testing unreleased versions of the compiler with large amounts of Rust code written by lots of different people.
That includes every crate published on crates.io, and at least some Rust projects on GitHub.

The existence of Crater speaks to the level of standardisation in Rust build tooling -- most projects will use `cargo build` and `cargo test`.
It would be impossible to do this for a language like Python, where there are lots of popular approaches and every project runs tests in a different way.

Earlier this week, Ed Page (who's on the Cargo team) [opened an issue][issue15] in my `randline` project:

> Test binary is looked up in unit tests which relies on internals of Cargo and will break with existing / upcoming features […]
>
> This problem was identified by the following crater run: <a href="https://github.com/rust-lang/rust/pull/149852">rust-lang/rust#149852</a>

This issue almost certainly comes from my version of the `assert_cmd` crate -- I'm several versions behind the latest.

I'm not rushing to fix this because I'm not working on randline right now, but I'm quite excited to realise some of my Rust is prominent enough to be featured in Crater runs.

[crater]: https://doc.crates.io/contrib/tests/crater.html
[issue15]: https://github.com/alexwlchan/randline/issues/15
