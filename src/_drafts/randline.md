---
layout: post
title: "randline: get a random selection of lines in a file using reservoir sampling"
summary: I wrote a tiny Rust tool to get random samples in a memory-efficient way, and I learnt a lot while doing it.
tags:
  - my tools
  - rust
---
I've posted another command-line tool on GitHub: [randline], which gives you a random selection of lines in a file:

```console
$ randline < /usr/share/dict/words
ultraluxurious

$ randline 3 < /usr/share/dict/words
unexceptionably
baselessness
salinity
```

There are lots of tools that solve this problem; I wrote my own as a way to get some more Rust practice and try a new-to-me algorithm called [reservoir sampling].

[randline]: https://github.com/alexwlchan/randline
[reservoir sampling]: https://en.wikipedia.org/wiki/Reservoir_sampling





## Existing approaches

There's a [`shuf` command][shuf] in coreutils which is designed to do this exact thing:

```console
$ shuf -n 3 /usr/share/dict/words
brimstone
melody's
reimbursed
```

But I don't have coreutils on my Mac, so I can't use `shuf`.

You can do this in lots of other ways using tools like `awk`, `sort` and `perl`.
If you're interested, check out these [Stack Overflow] and [Unix & Linux Stack Exchange][UL] threads for examples.

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

(I'm not sure why my past self decided not to use [random.sample].
I suspect I'd forgotten about it.)

This script has worked fine, but I stumbled across it recently and it got me thinking.
This approach isn't very efficient -- it has to load the whole file into memory.
Can we do better?

[shuf]: https://www.gnu.org/software/coreutils/manual/html_node/shuf-invocation.html#shuf-invocation
[Stack Overflow]: https://stackoverflow.com/q/9245638/1558022
[UL]: https://unix.stackexchange.com/q/108581/43183
[random.sample]: https://docs.python.org/3/library/random.html#random.sample





## Reservoir sampling

In other Python scripts, I process files as a stream -- look at one line at a time, rather than loading the whole file at once.
This doesn't make much difference for small files, but it pays off when you have really big files.

I couldn't think of a good way to take a random sample of a file using streaming, and still get a uniform distribution -- but smart people have already thought about this.
I did some reading and I found a technique called *reservoir sampling*.
The introduction in [the Wikipedia article][wikipedia] makes it clear this is exactly what I want:

> Reservoir sampling is a family of randomized algorithms for choosing a simple random sample, without replacement, of *k* items from a population of unknown size *n* in a single pass over the items. The size of the population *n* is not known to the algorithm and is typically too large for all *n* items to fit into main memory. The population is revealed to the algorithm over time, and the algorithm cannot look back at previous items.

The basic idea is that rather than holding the whole file in memory at once, I can keep a fixed-sized buffer -- or "reservoir" -- of the items I've selected.
As I go line-by-line through the file, I can add or remove items in this resevoir, and it will always use about the same amount of memory.
I'm only holding a line in memory if it's in the reservoir, not every line in the file.

[wikipedia]: https://en.wikipedia.org/wiki/Reservoir_sampling





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

The [Wikipedia article][reservoir sampling] describes several algorithms, including a simple Algorithm R and an optimal Algorithm L.
The underlying principle of Algorithm L is pretty concise:

> If we generate $n$ random numbers $u_1, \ldots, u_n \sim U[0,1]$ independently, then the indices of the smallest $k$ of them is a uniform sample of the $k$-subsets of $\\{1, \ldots, n\\}$.

There's no proof in the Wikipedia article, but I wanted to satisfy myself that this is true.
If you're happy to take it as given, you can skip the maths and go to the next section.

Here's my attempt at a justification:

What we really care about is the relative ranking of the $u_1, \ldots, u_n$, not their actual values -- we care whether, for example, $u_1 < u_2$, but not the exact difference between them.

Because the variables are independent and they have the same distribution, every possible ranking is equally likely.
Every variable is the same, so none of them can be "special" or favoured above the others.
This means that each permutation of the indices $\\{1, \ldots, n\\}$ is equally likely.
There are $n!$ such permutations, so each occurs with probability $1/n!$.

For a given $k$-subset, we're interested in permuations where this subset is the first $k$ items.
This means the probability that a particular $k$-subset will be selected is a simple fraction:

$$
\begin{equation*}
\text{probability of selecting this }k\text{-subset}
=
\frac{\text{# of permutations where this subset is the first }k\text{ items}}
{\text{# of permutations}}
\end{equation*}
$$

How many permutations are there where this $k$-subset is the first $k$ items?
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

Fortunately, we don't need to: the nice thing about this algorithm is that we only need to track the $k$ smallest values of $u_1, \ldots, u_i$ we've seen so far.
Once a value is larger than the $k$ smallest, we can safely discard it because we know it'll never be used.

Here's the approach I took:

1.  Create an empty "reservoir" of $k$ items.

2.  As you get items, assign each one a "weight" and start filling the reservoir.
    (These weights are the random variables $u_1, \ldots, u_n$.)

    If you run out of items before you fill the reservoir, go to step 4.

    If you fill the reservoir and there are more items, calculate the largest weight of the items in the reservoir, and go to step 3.

3.  Once the reservoir is full, go through the remaining items one-by-one.

    For each item, assign it a weight.
    *   If the weight of this new item is larger than the largest weight already in the reservoir, discard the item.
        This weight isn't in the $k$ smallest, so we don't care about it.
    *   If the weight of this new item is smaller than the largest weight in the resevoir, then add the item to the reservoir and remove the item with the previously-largest weight.
        Recalculate the largest weight of the items in the reservoir.

    When you run out of items, go to step 4.

4.  Return the items in the reservoir.
    This is your random sample.

This approach means we only have to hold a fixed number of items/weights in memory at a time -- much more efficient, and it should scale to an arbitrarily large number of inputs.
It's a bit too much code to include here, but you can read my Rust implementation [on GitHub][my_code].
I wrote some tests, which include a statistical test -- I run the sampling code 10,000 times, and check the results are the uniform distribution I want.

[my_code]: https://github.com/alexwlchan/randline/blob/d5931463e1832548d7e509f3cf525b5d166850ce/src/sampling.rs





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

I've used both of these methods before, but I only understood part of the difference.

When you call `.iter()`, you're borrowing the vector, which means it can be used later.
When you call `.into_iter()`, you're consuming the vector, which means it can't be used later.
I hadn't thought about how this affects the types.

When you call `.iter()`, you get an iterator of *references*.
When you call `.into_iter()`, you get an iterator of *values*.
This caused me some confusion when I was writing a test.

Consider the following code:

```rust
fn reservoir_sample<T>(
    mut items: impl Iterator<Item = T>,
    k: usize) -> Vec<T> { … }

let letters = vec!["A", "A", "A"];
let items = letters.iter();
assert_eq!(reservoir_sample(items, 1), vec!["A"]);
```

I was trying to write a test that `reservoir_sample` would only return the number of items I asked for, and no more.
This was my first attempt, and it doesn't compile.

When I call `letters.iter()`, I'm getting an iterator of string references, that is `Iterator<&&str>`.
Then I'm comparing it to a `Vec<&str>`, but Rust doesn't know how to check equality of `&str` and `&&str`, so it refuses to compile this code.

There are two ways I could fix this:

1.  Use `.into_iter()`, so I get an iterator of string values, i.e. `Iterator<&str>`.

    ```rust
    let letters = vec!["A", "A", "A"];
    let items = letters.into_iter();
    assert_eq!(reservoir_sample(items, 1), vec!["A"]);
    ```

2.  Change the expected result so it's a `Vec<&&str>`:

    ```rust
    let letters = vec!["A", "A", "A"];
    let items = letters.iter();
    assert_eq!(reservoir_sample(items, 1), vec![&"A"]);
    ```

I used `.into_iter()` in my tests.

This sort of distinction is probably obvious to more experienced Rust programmers, but it was new to me.
I've read about these methods, but I only understand them by writing code.

###  Arrays are indexed with `usize`

I wasn't sure what type I should use for `k`, the size of the random sample.
It's a positive integer, but should I use [`u32`][u32] or [`usize`][usize]?
I read the descriptions of both, and it wasn't immediately obvious which was preferable.

I looked to [`Vec::with_capacity`][with_capacity] for inspiration, because it's one of the methods I was using and it feels similar.
It takes a single argument `capacity: usize`.
That gave me an example to follow, but I still wanted to understand why.

I did some more reading, and I learned that Rust arrays are [indexed with `usize`][indexing].
It makes sense that a pointer type is used for array indexing, but it's been a while since I used a language with pointers, and so it didn't occur to me.

[u32]: https://doc.rust-lang.org/std/primitive.u32.html
[usize]: https://doc.rust-lang.org/std/primitive.usize.html
[with_capacity]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.with_capacity
[indexing]: https://doc.rust-lang.org/reference/expressions/array-expr.html#array-and-slice-indexing-expressions

### There's a lot of cool stuff in `std::collections`

At the core of this tool, I have a reservoir of weighted items, and I want to be able to find the item with the largest weight when it gets replaced.
This sounds like [priority queue], and there's an implementation of one in the Rust standard library.
I was able to use [`BinaryHeap`][BinaryHeap] from the [`std::collections` module][collections], which saved me from writing a bunch of fiddly code myself.

Here's the broad shape of it:

```rust
struct WeightedItem<T> {
    item: T,
    weight: f64,
}

let mut reservoir: BinaryHeap<WeightedItem<T>> =
    BinaryHeap::with_capacity(k);
```

There's a bit more code to implement `Eq` and `Ord` for `WeightedItem`, but that wasn't difficult.
I didn't even need to read the documentation -- the compiler error messages were so helpful, I could just follow their suggestions to get a working solution.

In this sense, Rust feels very like Python -- both languages have a built-in `collections` module with some common data structures.
I need to spend more time exploring the Rust variant, and there's a [When should you use which collection?][which_collection] guide to help me find the useful parts.

[priority queue]: https://en.wikipedia.org/wiki/Priority_queue
[BinaryHeap]: https://doc.rust-lang.org/std/collections/binary_heap/struct.BinaryHeap.html
[collections]: https://doc.rust-lang.org/std/collections/index.html
[which_collection]: https://doc.rust-lang.org/std/collections/index.html#when-should-you-use-which-collection

---

This whole project is less than 250 lines of Rust, including tests.
There are plenty of other tools that do the same thing, so I doubt anybody else will want to use it.
Most people should use `shuf` -- to which Assaf Gordon added reservoir sampling [nearly twelve years ago][shuf_reservoir].
But in case anybody is interested, I've put all the code [on GitHub][github].

I've learnt every programming language in tiny steps -- a little at a time, growing slowly until I have something approximating skill.
This project is the latest tiny step towards learning Rust, and now I know a little bit more than I did before.
It's over eight years since I wrote my first Rust, and I'm still a beginner, but I'm having fun learning, and I'm having fun writing it down as I go.

[shuf_reservoir]: https://github.com/coreutils/coreutils/commit/20d7bce0f7e57d9a98f0ee811e31c757e9fedfff
[github]: https://github.com/alexwlchan/randline
