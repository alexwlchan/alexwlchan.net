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





## Existing approaches

There's a [`shuf` command][shuf] in coreutils which solves exactly this problem:

```console
$ shuf -n 3 /usr/share/dict/words
brimstone
melody's
reimbursed
```

But I don't have coreutils on my Mac, so I can't use `shuf`.

There are lots of other approaches, using tools like `awk`, `sort` and `perl`.
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
This approach isn't very efficient -- it loads the whole file into memory, shuffles it, then returns.
Can we do better?

[shuf]: https://www.gnu.org/software/coreutils/manual/html_node/shuf-invocation.html#shuf-invocation
[Stack Overflow]: https://stackoverflow.com/q/9245638/1558022
[UL]: https://unix.stackexchange.com/q/108581/43183
[random.sample]: https://docs.python.org/3/library/random.html#random.sample





## Reservoir sampling

In other Python scripts, I process files as a stream -- look at one line at a time, rather than loading the whole file at once.
This doesn't make much difference for small files, but it pays off when you have really big files.

I couldn't think of a good way to take a random sample of a file using streaming, but I did some reading and I found a technique called [reservoir sampling].
From the description on Wikipedia, it sounds like a perfect fit:

> Reservoir sampling is a family of randomized algorithms for choosing a simple random sample, without replacement, of *k* items from a population of unknown size *n* in a single pass over the items. The size of the population *n* is not known to the algorithm and is typically too large for all *n* items to fit into main memory. The population is revealed to the algorithm over time, and the algorithm cannot look back at previous items.

The basic idea is that rather than holding the whole file in memory at once, I can keep a fixed-sized buffer -- or "reservoir" -- of the items I've selected.
As I go line-by-line through the file, I can add or remove items in this resevoir, and it will always use about the same amount of memory.
I'm never holding more than the reservoir.





<script>
MathJax = {
  loader: {load: ['[tex]/ams']},
  tex: {
    inlineMath: [['$', '$']],
    displayMath: [
      ['$$', '$$']
    ],
    packages: {'[+]': ['ams']}
  },
  svg: {
    fontCache: 'global'
  }
};
</script>

<!-- From https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js, retrieved 30 June 2024 -->
<script id="MathJax-script" async src="/static/2024/tex-chtml.js"></script>


## Algorithm L

The [Wikipedia article][reservoir sampling] describes several algorithms, including a simple Algorithm&nbsp;R and an optimal Algorithm&nbsp;L.
The underlying principle of Algorithm&nbsp;L is pretty concise:

> If we generate $n$ random numbers $u_1, \ldots, u_n \sim U[0,1]$ independently, then the indices of the smallest $k$ of them is a uniform sample of the $k$-subsets of $\\{1, \ldots, n\\}$.

There's no proof in the Wikipedia article, but I wanted to satisfy myself that this is true.
If you're happy to take it as read, you can skip the maths and go to the next section.

Here's my brief attempt at a justification:

What we really care about is the relative ranking of the $u_1, \ldots, u_n$, not their actual values -- we care whether, for example, $u_1 < u_2$, but not the exact difference between them.

The variables are independent and identically distributed, so all possible rankings are equally likely.
(This is because of symmetry -- every variable is the same, so none of them can be "special" or favoured above the others.)

This means that each permutation of the indices $\\{1, \ldots, n\\}$ is equally likely.
There are $n!$ such permutations, so each occurs with probability $1/n!$.

Because every permutation is equally likely, the probability that a particular $k$-subset will be selected is a simple fraction:

$$
\begin{equation*}
\text{probability of selecting this }k\text{-subset}
=
\frac{\text{# of permutations where this }k\text{-subset is smallest}}
{\text{# of permutations}}
\end{equation*}
$$

How many permutations are there where this $k$-subset is smallest?
There are $k!$ ways to arrange this $k$-subset as the first $k$ digits, and $(n-k)!$ ways to arrange the remaining digits.
This means there are $k!\left(n-k\right)!$ permutations that match, and so:

$$
\begin{equation*}
\text{probability of selecting this }k\text{-subset}
=
\frac{k!\left(n-k\right)!}{n!}
\end{equation*}
$$

This probability is the same for every $k$-subset, so each one is equally likely -- which is the thing we care about.

This was enough to give me the confidence to try implementing Algorithm&nbsp;L.





## Implementing Algorithm L in an efficient way

If we don't know $n$ upfront, we could save all the items and only then generate the random variables $u_1, \ldots, u_n \sim U[0,1]$ -- but that's precisely the sort of inefficiency I'm trying to avoid!

Fortunately, we don't need to: the nice thing about this algorithm is that we only need to track the $k$ smallest items we've seen so far.
Once an item is larger than the $k$ smallest, we can safely discard it because we know it'll never be used.

Here's the approach I took:

1.  Create an empty "reservoir" of $k$ items.

2.  As you get items, assign each one a "weight" and start filling the reservoir.
    If you run out of items before you fill the reservoir, you're done.

    Track the largest weight in the reservoir.

3.  Once the reservoir is full, go through the remaining items one-by-one.

    For each item, assign it a weight.
    *   If the weight of this new item is larger than the largest weight already in the reservoir, discard the item.
        It's not in the $k$ smallest so we don't care about it.
    *   If the weight of this new item is smaller than the largest weight already in the resevoir, then add it to the reservoir and remove the previously-largest item.
        Recalculate the largest weight in the reservoir.

This approach means we only have to hold a fixed number of items/weights in memory at a time -- much more efficient, and it should scale to an arbitrarily large number of inputs.
It's a bit too much code to include here, but you can read my Rust implementation [on GitHub](https://github.com/alexwlchan/randline/blob/66df6d72aafeacfb637ffdc1da3980271fc2b28b/src/sampling.rs).
I wrote some tests, which include a statistical test -- I run the sampling code 10,000 times, and check the results are the uniform distribution I want.

The Wikipedia article outlines some "simplifications", but I didn't implement any of them.
(I thought the basic idea was simple enough, and they actually made it more complicated.)





## What did I learn about Rust?

This is only about 250 lines of Rust, but it was still good practice, and I learnt a few new things.



### Working with generics

I've used [generics] in other languages, and I'd read about them in the Rust Book, but I'd never written my own code using generics in Rust.
I used a generic to write my sampling function:

<pre><code>fn reservoir_sample<strong>&lt;T&gt;</strong>(
    mut items: impl Iterator<strong>&lt;Item = T&gt;</strong>,
    k: usize) -> Vec<strong>&lt;T&gt;</strong> { … }</code></pre>

It was straightforward, and there were no big surprises.

[generics]: https://doc.rust-lang.org/book/ch10-01-syntax.html



### The difference between `.iter()` and `.into_iter()`


**This is the first time I used [generics](https://doc.rust-lang.org/book/ch10-01-syntax.html) in Rust.**
I've used them in a few other languages, and read about them in Rust, but never written them myself.
It was straightforward; there were no big surprises.

**I better understand the difference between `Vec.iter()` and `Vec.into_iter().`**
I knew that one is giving you a view over an array while the other consumes it, but I hadn't thought about how that affects the types.
Consider the following example:

```rust
fn reservoir_sample<T>(
    mut items: impl Iterator<Item = T>,
    k: usize) -> Vec<T> { … }

let letters = vec!["A", "A", "A"];

let result1 = reservoir_sample(letters.iter(), 1);
assert_eq!(result1, vec!["A"]);

let result2 = reservoir_sample(letters.into_iter(), 1);
assert_eq!(result2, vec!["A"]);
```

This code doesn't compile.

When I call `.iter()`, I get an iterator of *references* to the elements of the array, rather than the array itself.
The array `letters` is `Vec<&str>`, and calling `.iter()` gives me an `Iterator<&&str>` -- then `result1` becomes a `Vec<&&str>`.
This can't be compared to the expected result which is a `Vec<&str>`, so the code won't compile.

When I call `.into_iter()`, I get an iterator of *values* from the array.
This means calling `.into_iter()` on `letters` gives me an `Iterator<&str>`, and `result2` is a `Vec<&str>`.

This distinction is described in the documentation, but I don't think I really understood it before.
I'd read it, but I hadn't internalised it.

**Rust arrays are indexed with `usize`.**
I encountered this when trying to pick a type for `k`, the size of the random sample.
This needs to be a positive integer, but what's the difference between a `u32` and `usize` in this scenario?

I looked to [`Vec::with_capacity`][with_capacity] for inspiration -- it takes a `capacity: usize`.
I did a bit more reading, and it seems to be because Rust arrays are [indexed with `usize`][usize].
This isn't mentioned in the [description of `usize`][desc], but it seems useful to know.

[with_capacity]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.with_capacity
[usize]: https://doc.rust-lang.org/reference/expressions/array-expr.html#array-and-slice-indexing-expressions
[desc]: https://doc.rust-lang.org/std/primitive.usize.html

**There's a lot of cool stuff in [`std::collections`](https://doc.rust-lang.org/std/collections/index.html).**
At the core of this tool, I'm holding a reservoir of weighted elements, and I want to be able to identify the element with the biggest weight when it gets replaced.
This is a perfect fit for a [`BinaryHeap`][BinaryHeap], and using it out of the standard library saved me writing a bunch of fiddly code.

Here's the broad strokes:

```rust
struct WeightedItem<T> {
    item: T,
    weight: f64,
}

let mut reservoir: BinaryHeap<WeightedItem<T>> =
    BinaryHeap::with_capacity(k);
```

I did have to implement `Eq` and `Ord` for my `WeightedItem` struct, but that wasn't difficult -- I was able to do it from the helpful compiler error messages telling me what to do next.

The `collections` module is a superpower in Python, and the same seems to be true in Rust.
There's a handy [When should you use which collection?][which_collection] section at the top of the docs, so I should take a closer look at this library.
I'm sure there are other useful things in here.

[BinaryHeap]: https://doc.rust-lang.org/std/collections/binary_heap/struct.BinaryHeap.html
[which_collection]: https://doc.rust-lang.org/std/collections/index.html#when-should-you-use-which-collection

---

This whole tool is less than 250 lines of Rust, including tests.
It's also pretty niche and I doubt anybody else will want to use it -- there are plenty of other tools that do it, including the venerable `shuf`, which learnt how to do reservoir sampling [nearly twelve years ago][shuf_reservoir].
That's what most people should use.
But just in case anybody is interested, I've put all the code [on GitHub][github].

I've learnt every programming language in tiny steps -- a little at a time, growing slowly until I have something approximating "competence".
It's over eight years since I wrote my first Rust, and I'm still a beginner, but I'm having fun learning, and I'm having fun writing it down as I go.

[shuf_reservoir]: https://github.com/coreutils/coreutils/commit/20d7bce0f7e57d9a98f0ee811e31c757e9fedfff
[github]: https://github.com/alexwlchan/randline
