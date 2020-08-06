---
layout: post
date: 2020-08-06 11:14:20 +0000
title: Using fuzzy string matching to find duplicate tags
tags: python
---

I'm a big fan of [keyword tagging](https://en.wikipedia.org/wiki/Tag_(metadata)) as a way to organise my digital data.
(For an explanation why, see my post about [how I scan and store my paperwork](/2019/11/my-scanning-setup/#how-should-i-organise-my-files).)

Tags work best if I use them consistently -- same spelling, same wording, same everything.
In practice, I don't always get that right -- I make typos, mistakes, or I forget that I already have a tag for a particular concept, and I create another tag.
Here's a few similar tags from my notes folder:

```
Amazon S3
amazon-s3

books I want to read
books to read
list: books to read

books I've read
books i’ve read
```

Anybody can see that these tags mean the same thing, but if I search for any one of them I won't find anything tagged with the alternative spellings.

I could consolidate each of these into a single tag -- but I can only do that if I know I've created these similar tags.
How do I find these inconsistencies?
I often have hundreds of tags, and looking through the list by hand isn't practical.

This isn't a new problem, and I found [a great article from Seatgeek](https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/) (a ticketing platform) that solves something very similar.
They were trying to find similar descriptions of the same event.
The post explains various approaches to comparing text -- string similarity, partial string similarity, token ratios, and so on -- and then they packaged their work in a library called [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy).

There's a variant of FuzzyWuzzy called [RapidFuzz](https://pypi.org/project/rapidfuzz/), which does similar calculations but performs a lot faster -- anecdotally, I see a 10&times; speedup when using RapidFuzz over FuzzyWuzzy.

To find all possible pairs of tags in a collection, I use [itertools.combinations](https://docs.python.org/3/library/itertools.html#itertools.combinations).

Putting itertools and RapidFuzz together, here's the function I use:

```python
import itertools

from rapidfuzz import fuzz


def find_similar_pairs(tags, *, required_similarity=80):
    """
    Find pairs of similar-looking tags in the collection ``tags``.

    Increase ``required_similarity`` for stricter matching (=> less results).
    """
    for t1, t2 in itertools.combinations(sorted(tags), 2):
        if fuzz.ratio(t1, t2) > required_similarity:
            yield (t1, t2)
```

The required similarity often needs a bit of tuning.
Sometimes I do have tags that look very similar but are genuinely different (e.g. `mental health` and `dental health`), and I don't want too many of those in the results -- but I do want to find all the duplicates.
I start at 80%, but I often adjust up or down to get less or more results.

Comparing every pair is [O(<em>N</em><sup>2</sup>) complexity](https://en.wikipedia.org/wiki/Computational_complexity) in the number of tags.
This could be slow with lots of tags, but my personal collections don't have enough tags for that to be an issue.
Comparing the ~1100&nbsp;tags in my Pinboard account takes 1.5s on a fairly old laptop; it's plenty fast enough.

When I call this function, I usually have a tally-like dictionary as input.
For each similar pair, I print the number of times I've used the tag, which helps me see what the canonical spelling of a duplicate tag is.
If I've used one spelling once, and one spelling 50 times, I know which way to correct.

```python
if __name__ == "__main__":
    tags = get_tags()  # {"Amazon S3": 50, "amazon-s3": 1, …}

    for t1, t2 in find_similar_pairs(tags):
        print("%3d\t%s" % (tags[t1], t1))
        print("%3d\t%s" % (tags[t2], t2))
        print("")
```

This sort of cleanup task makes my tagging system more powerful.
Having a consistent set of tags makes it easier to find things.
Having an automated script makes this sort of cleanup task possible.

If you're dealing with a pile of messy, human-generated data, I can recommend using something like FuzzyWuzzy or RapidFuzz to cut through the noise.
