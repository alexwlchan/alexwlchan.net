---
layout: post
date: 2025-01-07 21:30:31 +00:00
title: How I test Rust command-line apps with `assert_cmd`
summary: Some practical examples of how this handy crate lets me write clear, readable tests.
tags:
  - rust
  - software testing
---
Rust has become my go-to language for my personal toolbox -- small, standalone utilities like [create_thumbnail], [emptydir], and [dominant_colours].
There's no place for Rust in my day job, so having some self-contained hobby projects means I can still have fun playing with it.

I've been using the [`assert_cmd` crate][assert_cmd] to test my command line tools, but I wanted to review my testing approach before I write my next utility.
My old code was *fine* and it *worked*, but that's about all you could say about it -- it wasn't clean or idiomatic Rust, and it wasn't especially readable.

My big mistake was trying to write Rust like Python.
I'd written wrapper functions that would call `assert_cmd` and return values, then I wrote my own assertions a bit like I'd write a Python test.
I missed out on the nice [assertion helpers] in the crate.
I'd skimmed just enough of the `assert_cmd` documentation to get something working, but I hadn't read it properly.

As I was writing this blog post, I went back and read the documentation in more detail, to understand the right way to use the crate.
Here are some examples of how I'm using it in my refreshed test suites:

[create_thumbnail]: /2024/create-thumbnail/
[emptydir]: /2024/emptydir/
[dominant_colours]: /2021/dominant-colours/
[assert_cmd]: https://crates.io/crates/assert_cmd
[assertion helpers]: https://docs.rs/assert_cmd/latest/assert_cmd/assert/struct.Assert.html

## Testing a basic command

This test calls `dominant_colours` with [a single argument][arg], then checks it succeeds and that a single line is printed to stdout:

```rust
use assert_cmd::Command;

/// If every pixel in an image is the same colour, then the image
/// has a single dominant colour.
#[test]
fn it_prints_the_colour() {
    Command::cargo_bin("dominant_colours")
        .unwrap()
        .arg("./src/tests/red.png")
        .assert()
        .success()
        .stdout("#fe0000\n")
        .stderr("");
}
```

[arg]: https://docs.rs/assert_cmd/latest/assert_cmd/cmd/struct.Command.html#method.arg

If I have more than one argument or flag, I can replace `.arg` with `.args` to [pass a list][args]:

```rust
use assert_cmd::Command;

/// It picks the best colour from an image to go with a background --
/// the colour with sufficient contrast and the most saturation.
#[test]
fn it_chooses_the_right_colour_for_a_light_background() {
    Command::cargo_bin("dominant_colours")
        .unwrap()
        .args(&[
            "src/tests/stripes.png",
            "--max-colours=5",
            "--best-against-bg=#fff",
        ])
        .assert()
        .success()
        .stdout("#693900\n")
        .stderr("");
}
```

[args]: https://docs.rs/assert_cmd/latest/assert_cmd/cmd/struct.Command.html#method.args

Alternatively, I can omit `.arg` and `.args` if I don't need to pass any arguments.

## Testing error cases

Most of my tests are around error handling -- call the tool with bad input, and check it returns a useful error message.
I can check that the command failed, the exit code, and the error message printed to stderr:

```rust
use assert_cmd::Command;

/// Getting the dominant colour of a file that doesn't exist is an error.
#[test]
fn it_fails_if_you_pass_an_nonexistent_file() {
    Command::cargo_bin("dominant_colours")
        .unwrap()
        .arg("doesnotexist.jpg")
        .assert()
        .failure()
        .code(1)
        .stdout("")
        .stderr("No such file or directory (os error 2)\n");
}
```

## Comparing output to a regular expression

All the examples so far are doing an exact match for the stdout/stderr, but sometimes I need something more flexible.
Maybe I only know what part of the output will look like, or I only care about checking how it starts.

If so, I can use the `predicate::str::is_match` predicate from the [`predicates` crate][predicates] and define a regular expression I want to match against.

Here's an example where I'm checking the output contains a version number, but not what the version number is:

```rust
use assert_cmd::Command;
use predicates::prelude::*;

/// If I run `dominant_colours --version`, it prints the version number.
#[test]
fn it_prints_the_version() {
    // Match strings like `dominant_colours 1.2.3`
    let is_version_string =
        predicate::str::is_match(r"^dominant_colours [0-9]+\.[0-9]+\.[0-9]+\n$").unwrap();

    Command::cargo_bin("dominant_colours")
        .unwrap()
        .arg("--version")
        .assert()
        .success()
        .stdout(is_version_string)
        .stderr("");
}
```

[predicates]: https://crates.io/crates/predicates

## Creating focused helper functions

I have a couple of helper functions for specific test scenarios.

I try to group these by common purpose -- they should be testing similar behaviour.
I'm trying to avoid creating helpers for the sake of reducing repetitive code.

For example, I have a helper function that passes a single invalid file to `dominant_colours` and checks the error message is what I expect:

```rust
use assert_cmd::Command;
use predicates::prelude::*;

/// Getting the dominant colour of a file that doesn't exist is an error.
#[test]
fn it_fails_if_you_pass_an_nonexistent_file() {
    assert_file_fails_with_error(
        "./doesnotexist.jpg",
        "No such file or directory (os error 2)\n",
    );
}

/// Try to get the dominant colours for a file, and check it fails
/// with the given error message.
fn assert_file_fails_with_error(
    path: &str,
    expected_stderr: &str,
) -> assert_cmd::assert::Assert {
    Command::cargo_bin("dominant_colours")
        .unwrap()
        .arg(path)
        .assert()
        .failure()
        .code(1)
        .stdout("")
        .stderr(predicate::eq(expected_stderr))
}
```

Initially I wrote this helper just calling `.stderr(expected_stderr)` to do an exact match, like in previous tests, but I got an error *"`expected_stderr` escapes the function body here"*.
I'm not sure what that means -- it's something to do with borrowing -- but wrapping it in a predicate seems to fix the error, so I'm happy.

---

## My test suite is a safety net, not a playground

Writing this blog post has helped me refactor my tests into something that's actually good.
I'm sure there's still room for improvement, but this is the first iteration that I feel happy with.
It's no coincidence that it looks very similar to other test suites using `assert_cmd`.

My earlier approaches were far too clever.
I was over-abstracting to hide a few lines of boilerplate, which made the tests harder to follow.
I even wrote a macro with [a variadic interface] because of a minor annoyance, which is stretching the limits of my Rust knowledge.
It was fun to write, but it would have been a pain to debug or edit later.

It's okay to have a bit of repetition in a test suite, if it makes them easier to read.
I keep having to remind myself of this -- I'm often tempted to create helper functions whose sole purpose is to remove boilerplate, or create some clever parametrisation which only made sense as I'm writing it.
I need to resist the urge to compress my test code.

My new tests are more simple and more readable.
There's a time and a place for clever code, but my test suite isn't it.

[a variadic interface]: https://doc.rust-lang.org/rust-by-example/macros/variadics.html
