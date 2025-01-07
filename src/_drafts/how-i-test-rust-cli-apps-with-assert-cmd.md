---
layout: post
title: How I test Rust CLI apps with assert_cmd
summary:
tags:
  - rust
  - software testing
---
have a small number of Rust CLI apps,
including create_thumbnail, dominant_colours, and emptydir

I like Rust, it's fun!
it's become my go-to choice for small, standalone utilities
CLI apps are nice self-contained projects to play with it
because there isn't a good space for it in my day job right now

thinking about another, and want to make sure testing setup is right

I was already using `assert_cmd` crate, and had written a bunch of slightly different tests
the code was fine and it worked but it wasn't good
did a little review

my mistake was trying to write rust like python -- i'd written wrapper functions that would call assert_cmd and return a value, and wasn't taking advantage of nice assertion helpers in assert_cmd itself
i'd read just enough of the assert_cmd docs, but nothing more

finally sat down to read documentation and work out how to do it properly

1.  call a CLI app with a single argument
    check command works and produces expected stdout:

    ```rust
    #[test]
    fn it_prints_the_colour() {
        Command::cargo_bin("dominant_colours")
            .unwrap()
            .args(&["./src/tests/red.png"])
            .assert()
            .success()
            .stdout("#fe0000\n")
            .stderr("");
    }
    ```

2.  call a CLI app with multiple arguments/flags
    check command works and produces expected stdout

    ```rust
    #[test]
    fn it_chooses_the_right_color_for_a_dark_background() {
        Command::cargo_bin("dominant_colours")
            .unwrap()
            .args(&[
                "src/tests/stripes.png",
                "--max-colours=5",
                "--best-against-bg=#222",
            ])
            .assert()
            .success()
            .stdout("#d4fb79\n")
            .stderr("");
    }
    ```

2.  check a command fails with a particular error message:

    ```
    #[test]
    fn it_fails_if_you_pass_an_nonexistent_file() {
        assert_file_fails_with_error(
            "./doesnotexist.jpg",
            "No such file or directory (os error 2)\n",
        );
    }

    Command::cargo_bin("dominant_colours")
        .unwrap()
        .args(&[path])
        .assert()
        .failure()
        .code(1)
        .stdout("")
        .stderr(predicate::eq(expected_stderr))
    ```

1.  check stdout matches a regex:

    ```rust
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn it_prints_the_version() {
        // Match strings like `dominant_colours 1.2.3`
        let is_version_string =
            predicate::str::is_match(r"^dominant_colours [0-9]+\.[0-9]+\.[0-9]+\n$").unwrap();

        Command::cargo_bin("dominant_colours")
            .unwrap()
            .args(&["--version"])
            .assert()
            .success()
            .stdout(is_version_string)
            .stderr("");
    }
    ```

1.  create wrapper function for common case -- look up single file, check stderr

    ```rust
    /// Try to get the dominant colours for a file, and check it fails
    /// with the given error message.
    fn assert_file_fails_with_error(
        path: &str,
        expected_stderr: &str,
    ) -> assert_cmd::assert::Assert {
        Command::cargo_bin("dominant_colours")
            .unwrap()
            .args(&[path])
            .assert()
            .failure()
            .code(1)
            .stdout("")
            .stderr(predicate::eq(expected_stderr))
    }
    ```

always check both stdout/stderr
might be overkill, but doesn't hurt

at one point was substituting name of CLI app with `env!("CARGO_PKG_NAME")`
no!
too clever, isn't going to change and is fine to hard-code

---

reflections:

my initial approach was too clever, and favoured creating utility methods to hide a few lines of boilerplate over readability
at one point was even writing a macro with variadic arguments to cover up a slight annoyance, which is at the far limit of my Rust knowledge
bad!
time and a place for "clever" code, but tests aren't it, want a reliable safety net

the current tests are simple and readable, what good tests should be

writing this blog post is how i went back and made it *good*
got a lot shorter and simpler in the process
something i'm realising is that if i want to write good code, i need to *slow down*
it's easy to write code quickly, but writing it well means taking time and understanding all the tools and libraries i'm using
that takes longer

i'm not sure how to reconcile that with the drive to deliver quickly, esp with LLMs on the scene
but that's a thought for another day
