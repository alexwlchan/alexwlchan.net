---
layout: post
date: 2022-05-05 14:01:56 +00:00
title: Running a Rust binary in Glitch
summary: Using different targets to build Rust binaries that will run in Glitch.
tags:
  - glitch
  - rust

colors:
  index_light: "#ff386a"
  index_dark:  "#5e76fd"
---

Earlier today I was trying to run a Rust app in [Glitch].
I figured this would be pretty simple -- Glitch apps run in Linux containers, so if I compiled a Rust binary outside Glitch and downloaded it at startup time, that should work, and I wouldn't have to wait for the Rust compiler every time my Glitch app started.
Linux is Linux, right?

(Let me tell you I'm not a C developer without telling you I'm not a C developer.)

I got it working, but it didn't work first time.

I started by building my Rust app in an Ubuntu container.
I'd installed the latest version of Rust with [Rustup], and I used Cargo to build the binary:

```console
$ cargo build --release
```

Then I modified my Glitch app to download the binary on startup, and tried to run it.
Uh oh:

```
./hello-world: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.28' not found (required by ./hello-world)
```

So something is missing.
Hmm.

Because I haven't done much C development, I don't really know what glibc is, or why it's important.
All I can tell is that it's missing.

I have a vague understanding that glibc is an implementation of libc, which is a collection of low-level functions that other programs can use, e.g. "write these bytes to a file".
Different platforms might have different implementations of libc, but they all have the same interface.
A program can either include its own implementation of libc (is that static linking?), or it can call out to an implementation in the OS (dynamic linking?).

I'm guessing that something in the Ubuntu/Rust toolchain I used expects the OS to have a copy of glibc, so it doesn't include it.
(Does Ubuntu use glibc?)
But the Linux used in the Glitch container doesn't have glibc, so when my Rust app tries to use glibc, it crashes.

I found a [Stack Overflow answer][answer] from somebody having similar issues; it suggests linking against MUSL libc.
I don't know the difference between glibc and MUSL libc, but the latter is statically linked, so presumably it doesn't care whether there's a libc in the app container.
The answer says it might not work if you're using other libraries which might in turn use libc, but I'm not, so it's fine.

Back in my Ubuntu container, I built my binary using the suggested commands:

```console
$ rustup target add x86_64-unknown-linux-musl
$ cargo build --target x86_64-unknown-linux-musl --release
```

and now I have a binary that works.
I copied that into Glitch, and it ran flawlessly.

I still don't really understand libc and compilers and linking, and that's okay.
Programming is really complicated, and while I'd like to know about everything, there's not always time to do a deep dive.
Sometimes, it's enough to get something working, and move on.

[Glitch]: https://glitch.com
[Rustup]: https://rustup.rs
[answer]: https://stackoverflow.com/a/63759392
