---
layout: post
title: "emptydir: look for (nearly) empty directories and delete them"
summary:
tags:
  - rust
  - my-tools
colors:
  css_light: "#bf4f1a"
  css_dark:  "#f69669"
---
{% comment %}
  Card image from https://www.pexels.com/photo/orange-crab-in-shallow-photo-584501/
{% endcomment %}

I've released a new command-line tool on GitHub: [emptydir], which looks for directories which are empty or nearly empty, and deletes them.

This isn't a completely trivial problem, because emptiness is deceptive.
Consider the following folder.
Finder tells us it has 0 items, so it must be empty, right?

{%
  picture
  filename="totally_empty.png"
  width="547"
  alt="A Finder window for a folder 'totally_empty' which doesn’t show any files, and the status bar says '0 items, 262.9 GB available'."
%}

What you don't see is the invisible [`.DS_Store` file][ds_store] created by Finder -- this is a file that keeps some information about how you want the folder to look.
For example, if you arrange the icons on your Desktop, their positions get stored in a `.DS_Store` file.
If you delete the file and relaunch Finder, your Desktop icons will revert to the default grid layout.

If there are files in the folder, the `.DS_Store` is a useful file to keep around.
If the folder is empty, it's unlikely to be worth saving.

Because I don't care about lonely `.DS_Store` files, I wrote the following rule in `emptydir`:

> If a folder contains nothing but a `.DS_Store` file, delete the entire folder.
>
> If there's anything else in the folder, leave it as-is.

This means that `emptydir` will clean up this apparently-empty folder and the hidden `.DS_Store` file it contains.
Hooray!

There are a couple of other folders which I'm similarly happy to delete if they're the only thing in their parent folder -- `.venv` (my Python virtual environment) and `__pycache__` (compiled Python byte code), both of which are transient folders I can easily recreate.

[emptydir]: https://github.com/alexwlchan/emptydir
[ds_store]: https://en.wikipedia.org/wiki/.DS_Store

## Why not use `find`?

Deleting empty directories isn't a new problem.
For example, there's an [answer on Unix Stack Exchange][answer] with hundreds of upvotes that suggests the following command:

```
find . -type d -empty -delete
```

This is what I used for a while, but it only deletes folders that are completely empty -- it will miss folders with `.DS_Store` files.

You could use `find` to delete all the `.DS_Store` files also:

```
find . -type f -name .DS_Store -delete
```

but this is too aggressive -- those files are actually useful in folders with visible files, and I'd be annoyed if all my view options were continually reset.
If I've taken the time to arrange my icons carefully, I don't want them to be reset!

Maybe there's a way to do what I want with `find`, but I couldn't work out how to do it.

[answer]: https://unix.stackexchange.com/a/107556/43183

## How does it work?

I started by looking for a Rust function that could walk a directory tree and recursively find all the subdirectories -- the Rust equivalent of Python's [`os.walk` function][os.walk].

I quickly stumbled upon the [walkdir crate][walkdir], which provides precisely this functionality.
Adapting one of the examples from the README, I was able to build a simple iterator that prints all the subdirectories of the current directory:

```rust
use walkdir::WalkDir;

let directories = WalkDir::new(".")
    .into_iter()
    .filter_map(|e| e.ok())
    .filter(|e| e.file_type().is_dir());

for dir in directories {
    println!("{}", dir.path().display());
}

// .
// ./target
// ./target/debug
// ./target/debug/.fingerprint
// …
```

While I was reading the documentation, I discovered the [`contents_first()` method][contents_first] -- when you set this to `true`, it yields the contents of a directory before the directory itself.
And my use case is called out explicitly: _"this is useful when, e.g. you want to recursively delete a directory"_.

```rust
let directories = WalkDir::new(".")
    .contents_first(true)
    .into_iter()
    .filter_map(|e| e.ok())
    .filter(|e| e.file_type().is_dir());
```

(It turns out that Python's `os.walk` has a similar argument `topdown`, which I'd never come across before writing this Rust code.
Because I've been using `os.walk` for years and I "knew" how to use it, it's been a long time since I looked at the docs.)

This iterator generates every directory, but I only want to get directories which are safe to delete.
How do I know if a directory only contains files/folders which are safe to delete?

I started with a function that lists all the entries in a given directory:

```rust
use std::collections::HashSet;
use std::ffi::OsString;
use std::fs;
use std::io;
use std::path::Path;

fn get_names_in_directory(dir: &Path) -> io::Result<HashSet<OsString>> {
    let mut names = Vec::new();

    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        names.push(entry.file_name());
    }

    Ok(HashSet::from_iter(names))
}

println!("{:?}", get_names_in_directory(Path::from(".")));
// Ok({"Cargo.toml", "target", ".git", "src", ".gitignore", "Cargo.lock"})

println!("{:?}", get_names_in_directory(Path::from("/dev/null")));
// Err(Os { code: 20, kind: NotADirectory, message: "Not a directory" })
```

This returns a `HashSet` because sets are easy to compare.

I can also create a set of the names I consider safe to delete if they're the only thing in a directory:

```rust
let deletable_names = HashSet::from([
    OsString::from(".DS_Store"),
    OsString::from("__pycache__"),
    OsString::from(".venv"),
]);
```

I can combine these to make a function that tells me whether a directory is safe to delete:

```rust
fn can_be_deleted(path: &Path) -> bool {
    let deletable_names = HashSet::from([
        OsString::from(".DS_Store"),
        OsString::from("__pycache__"),
        OsString::from(".venv"),
    ]);

    match get_names_in_directory(path) {
        Ok(names) => names.is_subset(&deletable_names),
        Err(_) => false,
    }
}
```

I can then add this function on the end of my iterator:

```rust
let directories_to_delete = WalkDir::new(".")
    .contents_first(true)
    .into_iter()
    .filter_map(|e| e.ok())
    .filter(|e| e.file_type().is_dir())
    .filter(|e| can_be_deleted(e.path()));
```

and then I can iterate over this filtered list, and delete any directories which are safe to delete.
It prints the path as it deletes a directory, so I can see what it's doing:

```rust
for dir in directories_to_delete {
    match fs::remove_dir_all(dir.path()) {
        Ok(_) => println!("{}", dir.path().display()),
        Err(_) => (),
    };
}
```

To make this into a standalone tool, I added a stack of tests, and a basic command-line interface using the [clap crate].
This allows me to choose which directory will be searched for empty directories -- either the working directory, or another directory of my choice:

```console
$ emptydir
$ emptydir /path/to/other/directory
```

If you want to see the full code or install it yourself, I've published all the code [on GitHub](https://github.com/alexwlchan/emptydir).

[os.walk]: https://docs.python.org/3/library/os.html#os.walk
[walkdir]: https://crates.io/crates/walkdir
[clap crate]: https://crates.io/crates/clap
[contents_first]: https://docs.rs/walkdir/latest/walkdir/struct.WalkDir.html#method.contents_first

## Why did you make this?

Beyond the fact that finding and deleting empty directories is something I do on a semi-regular basis, there are a few reasons why I made this as a standalone project and wrote this article:

**I want to make my code easier to find.**
I have a lot of handy tools and utilities, which I used to put in my <a href="https://github.com/alexwlchan/scripts">scripts repo</a>.
But that repo is a grab bag of loosely related code, there's not much reason for anybody else to look at it, and it's hard for them to find the useful parts if they do.

Standalone projects with a clear purpose are more discoverable than a miscellaneous bag of bits.

**Explaining my code makes it better.**
If I take the time to write an article that explains my code in more detail, the code always gets better.
I read it more carefully, and I improve parts that are tricky or confusing.
I also gather reference links, and I often discover something new as I do -- like when I learnt that Python's `os.walk` has a `topdown` argument as I wrote this article!

This is particularly important right now, because:

**I'm giving Rust another go.**
I recently switched to `uv` and `ruff` for my Python work, and I was reminded of how much faster Rust can be than even a carefully-written Python script.
Although I've tried Rust several times and I enjoy writing it, I'm still a novice and I have no experience working in large or shared Rust codebases.

In this project, I tried to write more idiomatic Rust, and I'm proud of the result.
For example, my older code makes liberal use of `unwrap()`, but this project uses proper `Result` types.
This was a nice, small, self-contained task to get some Rust practice, and I learnt a lot.
Python is still my go-to language, but I'm gradually feeling more confident in Rust.

---

If you want to try `emptydir` for yourself or read the finished code, all the code is [on GitHub](https://github.com/alexwlchan/emptydir).

This was a practice run for a slightly larger tool that I'm also building in Rust, and I'll write about that soon.
