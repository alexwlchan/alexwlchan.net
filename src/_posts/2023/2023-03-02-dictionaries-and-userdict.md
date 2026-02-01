---
layout: post
date: 2023-03-02 15:51:47 +00:00
title: Creating a Python dictionary with multiple, equivalent keys
summary: Using collections.UserDict, we can create a dictionary where dict[key1] and dict[key2] always point to the same value.
tags:
  - python
colors:
  index_light: "#035e96"
  index_dark:  "#6fd0fd"
card_attribution: Cover image is CC0, by stevepb, from https://pixabay.com/photos/dictionary-reference-book-learning-1619740/
---

In [my previous post][groups], I was creating groups of students, and I wanted to track how many times students had worked together.
I created a nested dictionary to track the pairs:

```python
pairs = {
  'Alice': {'Bryony': 3, 'Caroline': 1, 'Danielle': 0, …},
  'Bryony': {'Alice': 3, 'Caroline': 2, …},
  …
}
```

To find out how many times Alice and Bryony had worked together, you'd look up `pairs['Alice']['Bryony']` or `pairs['Bryony']['Alice']`.
This was fine for a one-off project, but it's inefficient and prone to error -- every time I modify the dictionary, I have to remember to update two keys.
It's also a bit fiddly and hard to explain.
Wouldn't it be nice if the data structure could handle it for us?

What I wanted was a dictionary where `pairs[('Alice', 'Bryony')]` and `pairs[('Bryony', 'Alice')]` are always the same -- and the more I thought about it, the more I thought that sort of dictionary might be useful.

As I tried to actually implement this, I learnt a couple of new things about the collections module.

[groups]: /2023/balancing-act/

---

The idea I came up with is to have a dictionary that normalises keys.
This normalised key is used internally, but callers can use the un-normalised version and still get the value associated with the normalised key.
For example, if you pass it a tuple as a key, it could normalise by sorting the entries of the tuple.
Then a caller could use both `pairs[('Alice', 'Bryony')]` and `pairs[('Bryony', 'Alice')]`, but internally the key would always be normalised to `('Alice', 'Bryony')`.

My initial plan was to subclass [MutableMapping] in the [collections.abc module][abc], something like this:

```python
import collections.abc

class NormalisedKeyDictionary(collections.abc.MutableMapping):
    def __init__(self, data, *, normalise):
        self.data = data
        self.normalise = normalise
```

and then define get/set/del methods that call the underlying dictionary with normalised keys.

But as I was writing this post, I discovered that wrapping a dictionary is such a common operation, there's a [collections.UserDict class][UserDict] we can use instead.
This is slightly nicer than MutableMapping, because it implements [a bunch of dictionary-like methods][impl] like `__repr__` and `copy`.

(You might wonder why I'm subclassing from the collections module, and not directly subclassing dict.
The reason is that MutableMapping and UserDict are meant to be subclassed, whereas dict isn't -- certain methods don't play well when you subclass, e.g. `dict.update`.)

When we subclass UserDict, we can intercept the get/set/del methods and make them use normalised keys, like so:

```python
class NormalisedKeyDictionary(collections.UserDict):
    def __init__(self, data=None, *, normalise):
        self.normalise = normalise
    
        # normalise any keys that are being passed in 
        data = data or {}
        super().__init__({normalise(k): v for k, v in data.items()})

    def __getitem__(self, key):
        return super().__getitem__(self.normalise(key))

    def __setitem__(self, key, value):
        return super().__setitem__(self.normalise(key), value)

    def __delitem__(self, key):
        return super().__delitem__(self.normalise(key))
```

Here's what it looks like in use:

```python
pairs = NormalisedKeyDictionary(
    {('Alice', 'Bryony'): 1},
    normalise=lambda key: tuple(sorted(key))
)

# We can set keys...
pairs[('Alice', 'Carol')] = 2

# ...and retrieve them in normalised or not-normalised form
pairs[('Alice', 'Carol')]  # 2
pairs[('Carol', 'Alice')]  # 2

# We can iterate over the keys/values/items
for (key, value) in pairs.items():
    print(key, value)
    # ('Alice', 'Bryony') 2
    # ('Alice', 'Carol')  1

# And we can remove key/value pairs
pairs.keys()  # ('Alice', 'Bryony') ('Alice', 'Carol')
del pairs[('Bryony', 'Alice')]
pairs.keys()  # ('Alice', 'Carol')
```

If you want to play with this yourself, you can download the code (and tests!):

{% download filename="normalised_key_dictionary.py" %}

So now we have something that looks and behaves remarkably like a dictionary, but we can use alternative forms of the same key.
This simplifies our calling code -- we don't need to worry about normalising keys, or updating multiple values in the dictionary -- we use any form of the key, and it'll do the right thing.

This is a double-edged sword: it can be more convenient, but also more confusing.
Because it looks so much like an ordinary dictionary, its behaviour would be surprising if you're not expecting it to muck around with the keys.
I'd be careful about using this in a large, shared codebase.

One interesting use of this approach would be to create a dictionary with unusual key types.
Dictionary keys need to be hashable and immutable, which rules out certain types of key -- for example, you can't use a list as a dict key.
But you could use a list as a normalised dict key, if you convert it to an immutable tuple first:

```python
regular_dict = {}
regular_dict[['one', 'two']] = 'o'  # TypeError: unhashable type: 'list'

common_letters = NormalisedKeyDictionary(normalise=lambda k: tuple(k))

common_letters[['one', 'two']] = 'o'
common_letters[['two', 'three']] = 't'

common_letters[['one', 'two']]  # 'o'
```

This could still be confusing, but because lists as keys are illegal in regular Python, it might be more of a clue that this is a special dictionary.

I don't know if I'll ever actually use this code, but I'm glad to learn about [collections.UserDict][UserDict] (and corresponding classes UserList and UserString).
That feels like quite a useful class, and I only found it by writing this post.

[abc]: https://docs.python.org/3/library/collections.abc.html
[MutableMapping]: https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping
[UserDict]: https://docs.python.org/3/library/collections.html?highlight=userdict#collections.UserDict
[impl]: https://github.com/python/cpython/blob/ed55c69ebd74178115cd8b080f7f8e7588cd5fda/Lib/collections/__init__.py#L1149-L1199
