---
layout: post
title: "randline: get a random selection of lines in a file using reservoir sampling"
summary: I wrote a tiny Rust tool that can get random samples in a memory-efficient way.
tags:
  - my tools
  - rust
---
I've posted another command-line tool on GitHub: [randline], which gives you a random selection of lines in a file:

```console
$ randline < /usr/share/dict/words
Urania

$ randline 3 < /usr/share/dict/words
foolhardiness
rhinoscopic
wormhood
```

There are lots of ways to solve this problem; I wrote my own as a way to get some more Rust practice and try a new-to-me algorithm called [reservoir sampling].

[randline]: https://github.com/alexwlchan/randline
[reservoir sampling]: https://en.wikipedia.org/wiki/Reservoir_sampling

## Prior art

There's a [`shuf` command][shuf] in coreutils which solves exactly this problem (and does a few more things besides):

```console
$ shuf -n 3 /usr/share/dict/words
brimstone
melody's
reimbursed
```

I don't have coreutils on my Mac, so I can't use `shuf`.

There are lots of other approaches, using tools like `awk`, `sort -R` and `perl`.
If you're interested, check out these [Stack Overflow] and [Unix & Linux Stack Exchange][UL] threads for some examples.

For my needs, I wrote a tiny Python script called `randline` which I saved in my PATH years ago, and I haven't thought much about since:

```python
import random
import sys


if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()
    try:
        k = int(sys.argv[1])
    except IndexError:
        k = 1

    random.shuffle(lines)
    print("\n".join(lines[:k]))
```

(I'm not sure why my past self decided not to use [random.sample].)

This script has worked fine, but I stumbled across it recently and it got me thinking.
This approach isn't very efficient -- it loads the whole file into memory, then shuffles it, then returns.
Can we be more efficient?

[shuf]: https://www.gnu.org/software/coreutils/manual/html_node/shuf-invocation.html#shuf-invocation
[Stack Overflow]: https://stackoverflow.com/q/9245638/1558022
[UL]: https://unix.stackexchange.com/q/108581/43183
[random.sample]: https://docs.python.org/3/library/random.html#random.sample

## Reservoir sampling

I felt like it must be possible to do this sort of random sample in a better way.
In other Python scripts, I try to process files as a stream -- look at one line at a time, rather than loading the whole file at once.
This doesn't do much for small files, but it pays off when you have really big files.

Taking a random sample of one or more lines feels like it could be done in a similar way.
Why not create a "buffer" to hold the *k* items I've selected, and on each line decide whether to (1) replace one of the items in the buffer or (2) discard the line?
This has a smaller and more predictable memory footprint, and should scale to any size of file.

But how do you decide whether to keep or discard an item?
You can't change your mind and retrieve the item later.

This reminded me of the [secretary problem], which I studied in school.
You're interviewing *n* candidates for a job, and after each interview you can choose to hire somebody immediately, and dismiss them and interview the next candidate.
Once you dismiss somebody, you can't ask them back later.
How do you hire the best person?
I'd forgotten the answer, but I knew there was a mathematically optimal approach.

It's not quite the same, but it made me think that other people have probably thought about this problem already.
But how do I find their research?

I explained the problem to ChatGPT, and it pointed me in the right direction: I was describing [reservoir sampling].
It's exactly what I was thinking of, including the memory efficiency that started this line of thinking:

> Reservoir sampling is a family of randomized algorithms for choosing a simple random sample, without replacement, of *k* items from a population of unknown size *n* in a single pass over the items. The size of the population *n* is not known to the algorithm and is typically too large for all *n* items to fit into main memory. The population is revealed to the algorithm over time, and the algorithm cannot look back at previous items.

The buffer I'd imagined is called the "reservoir", and there are various algorithms for getting a uniform sample of the input items.
Perfect!

[secretary problem]: https://en.wikipedia.org/wiki/Secretary_problem

## Actually implementing the algorithm

The Wikipedia article describes several algorithms, including a simple Algorithm&nbsp;R and an optimal Algorithm&nbsp;L.
The description is pretty simple:

> If we generate *n* random numbers <em>u</em><sub>1</sub>,&nbsp;…,&nbsp;<em>u</em><sub><em>n</em></sub> ~&nbsp;*U*[0,1] independently, then the indices of the smallest *k* of them is a uniform sample of the *k*-subsets of {1,&nbsp;…,&nbsp;*n*}.


---

but not particular efficient – load whole thing into memory.
what if want to do it more efficiently?

not sure what to do
ask Claude, it suggested https://en.wikipedia.org/wiki/Reservoir_sampling

aha!
sounds perfect

let's implement Algorithm L in Rust

did ask Claude to generate some code, but too much for me to really understand
and defeats point of exercise!

here's the key algo:

```rust
code goes here
```

is this idiomatic rust? idk but I can understand it which is more important

added some tests and basic wrapper
don't really understand why Algorithm L works, but did some testing and it does the right thing

testing was another useful exercise in Rust, and I understand `.iter()` and `.into_iter()`better now
reference/value, but really grok it
cf test what comes out?

```
let a = vec!["a", "b", "c"];

reservoir_sample(a.iter(), 5);       // Vec<&String>
reservoir_sample(a.into_iter(), 5);  // Vec<String>
```

also why there's an f32 weight instead of i32

and continue to get a bit more practice writing Rust

feels like a niche tool but published on GitHub anyway
you want it? go check it out