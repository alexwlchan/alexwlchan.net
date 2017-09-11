---
title: Ode to docopt
summary: How to write better, cleaner command-line interfaces with the docopt library.
tags: python, slides
category: slides
date: 2017-09-11 12:01:13 +0100
layout: post
theme:
  color: 008000
  touch_icon: docopt
---

Every week, we have an hour of developer learning at work -- maybe a talk, a workshop, or some other session about of topic of interest to developers.
Last week, we did a round of lightning talks.
We're quite a mixed group of developers -- in background, technical stacks, and what we actually work on -- so coming up with a topic that's useful to all can be tricky.

For my slot, I decided to wax lyrical about [the docopt library][docopt].
Once upon a time, I was sceptical, but it's become my go-to library for any sort of command-line interface.
Rather than fiddling with argparse and the like, I just write a docopt help string, and the hard work is done for me.
I've used it in multiple languages, and thought it might be handy for other devs at work.
Ergo, this talk.

You can [download my slides as a PDF](/docopt/docopt_slides.pdf), or read the notes below.

<!-- summary -->

---

{% slide docopt 1 %}

This is a talk about docopt, a family of libraries for writing command-line interfaces.

{% slide docopt 2 %}

As developers, we often have to write command-line interfaces.
Here's an example usage string from a static site generator.

If you've seen other CLI tools, you might be able to work out how to use it:

*   There's a command called `new`, which takes a mandatory `<path>` parameter and an optional `--theme` parameter.
*   There's a second command `build`, which can be called standalone or with the `--continuous` flag.
*   There's a third command `serve`, which has two optional parameters: `--host` and `--port`.
    We can also see that both of these flags have defaults.
*   Finally, we could use `-h` or `--help` to get a help message, and `--version` to see the version string.

So how would we implement this in code?

{% slide docopt 3 %}

If we're using Python, we might use [argparse][argparse] from the standard library.
But this code is pretty mucky: we have to set up parsers, subparsers, all that… yuck!
(And this is a simple example!)

Parsing arguments like this is hard, because you have to define your own parsing rules.
Code like this is hard to read -- it's not obvious what it's doing, or how to use the program, unless you actually run it.
If you hae to edit code like this, it can be tricky to know exactly where to make a change, and be sure you haven't inadvertently broken something elsewhere.

And argparse is complicated -- I never get it right first time.

{% slide docopt 4 %}

Let's reflect on [this wisdom][wisdom] from Kenneth Reitz.
We don't want to define our interfaces by hand -- there must be a better way!

Luckily for us, such a module already exists!

{% slide docopt 5 %}

This is what the same code looks like with [the docopt module][module].
I write a help string and call the single `docopt` function.
Then docopt will read my help string, construct a parser, and use that to define my command-line interface.

This is much nicer than our previous example.
It's much easier to see how the code works or add new options, and we write less parsing code (and so less bugs!).
And because the interface is auto-generated from the help string, it always stays up-to-date.

{% slide docopt 6 %}

In Python, docopt returns a dictionary with the different arguments.

In languages with stronger typing, you can define a custom structure, and docopt will create an instance of that structure from the parsed arguments.
For example, this is the struct I'd define in Rust:

```rust
pub struct Args {
  pub cmd_new: bool,
  pub arg_path: String,
  pub flag_theme: Option<String>,

  pub cmd_build: bool,
  pub flag_continuous: bool,

  pub cmd_serve: bool,
  pub flag_host: Option<String>,
  pub flag_port: Option<String>,

 pub flag_version: bool,
}
```

{% slide docopt 8 %}

So how does docopt work its magic?

It relies on the format of our help string.
Remember how we were able to read this help string, because it looked like help strings from other programs?

There's a standard for writing these help strings, as part of [POSIX][posix].
By sticking to these rules, docopt can work out how our program is meant to be used, and build an appropriate parser.

{% slide docopt 9 %}

Typically the help string passed to docopt also includes some front matter (a human-readable description) and explanation of the different options and commands -- but the usage string is the interesting part.

{% slide docopt 10 %}

Heere's a brief illustration of the sort of things you can define with docopt.
There's a full description of the rules on the docopt website.

{% slide docopt 11 %}

docopt started life as a Python library, nearly five years ago -- and is still available for Python, if that's what you use.

{% slide docopt 12 %}

But what if you use something else?
Because docopt is such a nice idea, it's been ported to lots of other languages.
You can find all the ports in the GitHub organisation.

This includes lots of the languages we use at Wellcome, including PHP and Scala.

*[CoffeeScript is the closest to a JavaScript port in the GitHub organisation. I thought this meant docopt was an exception to [Atwood's Law][atwood], but I've since found a [Node.js port][nodejs].]*

{% slide docopt 13 %}

As an example, here's our program ported to PHP.
Again, most of the code is writing the help string, the parsing code is just a call into a function provided by docopt.

(Another nice thing: docopt is often delivered as a single file, so you can add it to a project even if you don't/can't use a package manager.)

{% slide docopt 14 %}

More information about docopt, including links to the ports and more detailed instructions, is on the [docopt website][docopt].

[argparse]: https://docs.python.org/3.5/library/argparse.html
[wisdom]: ;https://github.com/kennethreitz/python-for-humans/blob/master/python-for-humans/1_content.md#the-litmus-test
[module]: https://pypi.org/project/docopt/
[posix]: https://en.wikipedia.org/wiki/POSIX
[atwood]: https://blog.codinghorror.com/the-principle-of-least-power/
[nodejs]: https://github.com/felixSchl/neodoc
[docopt]: http://docopt.org
