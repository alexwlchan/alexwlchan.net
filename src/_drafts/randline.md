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
This approach isn't very efficient -- it loads the whole file into memory, shuffles it, then returns.
Can we do better?

[shuf]: https://www.gnu.org/software/coreutils/manual/html_node/shuf-invocation.html#shuf-invocation
[Stack Overflow]: https://stackoverflow.com/q/9245638/1558022
[UL]: https://unix.stackexchange.com/q/108581/43183
[random.sample]: https://docs.python.org/3/library/random.html#random.sample

## Reservoir sampling

In other Python scripts, I process files as a stream -- look at one line at a time, rather than loading the whole file at once.
This doesn't do much for small files, but it pays off when you have really big files.

Taking a random sample of one or more lines feels like it could be done in a similar way.
Why not create a "buffer" to hold the items I'm going to select, and on each line decide whether to (1) replace one of the items in the buffer or (2) discard the line?
This has a smaller and more predictable memory footprint, and should scale to any size of file.

But how do you decide whether to keep or discard an item?
You can't change your mind and retrieve the item later.

I explained the problem to ChatGPT, and it pointed me in the right direction: I was describing [reservoir sampling].
It's exactly what I was thinking of, including the memory efficiency that started this line of thinking:

> Reservoir sampling is a family of randomized algorithms for choosing a simple random sample, without replacement, of *k* items from a population of unknown size *n* in a single pass over the items. The size of the population *n* is not known to the algorithm and is typically too large for all *n* items to fit into main memory. The population is revealed to the algorithm over time, and the algorithm cannot look back at previous items.

The buffer I'd imagined is called the "reservoir", and there are various algorithms for getting a uniform sample of the input items.
Perfect!

This is something I've found generative AI quite useful for: I know smart people have already thought about a problem, but I don't know the right words to look up.
Describing the problem to AI gives me the magic words I need to type into a traditional search engine.





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
The underlying principle of Algorithm&nbsp;L is pretty simple:

> If we generate $n$ random numbers $u_1, \ldots, u_n ~ U[0,1]$ independently, then the indices of the smallest $k$ of them is a uniform sample of the $k$-subsets of $\\{1, \ldots, n\\}$.

There's no proof in the Wikipedia article, but I wanted to satisfy myself that this is true.
Here's my brief attempt at a justification:

What we really care about is the relative ranking of the $u_1, \ldots, u_n$, not their actual values -- we care whether, for example, $u_1 < u_2$, but not the exact difference.
Because the variables are independent and identically distributed, all possible rankings are equally likely.
(There's a symmetry here -- every variable is the same, so none of them can be "special" or favoured above the others.)

That is each permutation of the indices $\\{1, \ldots, n\\}$ is equally likely.
There are $n!$ such permutations, so each occurs with probability $1/n!$.

$$
\begin{equation*}
\text{probability}
\left(
  \text{selecting this }k\text{-subset}
\right)
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
\text{probability}
\left(
  \text{selecting this }k\text{-subset}
\right)
=
\frac{k!\left(n-k\right)!}{n!}
\end{equation*}
$$

This is the same for every $k$-subset, so each one is equally likely -- which is the thing we care about.

That proof might not be watertight, but it was good enough to give me the confidence to try implementing Algorithm&nbsp;L.

## Implementing Algorithm L in an efficient way

If we don't know $n$ upfront, we could save all the items and only then generate the random variables $u_1, \ldots, u_n ~ U[0,1]$ -- but that's precisely the sort of inefficient thinking I'm trying to fix!

But we don't need to: the nice thing about this algorithm is that we only need to track the $k$ smallest items we've seen so far.
Once an item is larger than the $k$ smallest, we can safely discard it because we know it'll never be used.

Here's the approach I took:

1.  Create an empty "reservoir" of $k$ items

2.  As you get items, assign each one a "weight" and start filling the reservoir.
    If you run out of items before you fill the reservoir, you're done.

    Track the largest weight in the reservoir.

3.  Once the reservoir is full, for each new item assign it a weight.
    *   If the weight of this new item is larger than the largest weight already in the reservoir, discard the item.
        It's not in the $k$ smallest so we don't care about it.
    *   If the weight of this new item is smaller than the largest weight already in the resevoir, then add it to the reservoir and remove the previously-largest item.
        Recalculate the largest weight in the reservoir.

This approach means we only have to hold $k+1$ items and $k+1$ weights in memory at a time -- much more efficident, and

The Wikipedia article outlines some "simplifications"

---

We only care about the ranked order of the <em>u</em><sub>1</sub>,&nbsp;…,&nbsp;<em>u</em><sub><em>n</em></sub>, not their actual values.
Because they're all independent and identically distributed, all possible rankings are equally likely.
This means that each permutation of {1,&nbsp;,…,*n*} is equally likely.
In particular, each permutation will be selected with probability 1/*n*!.

For each *k*-subset of {1,&nbsp;,…,*n*}, there are the same number of permutations that start with those *k* numbers.



Because the
u
i
u
i
​
 's are i.i.d. uniform, all possible rankings of the
n
n values are equally likely (each permutation of
{
1
,
2
,
…
,
n
}
{1,2,…,n} is equally probable).



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