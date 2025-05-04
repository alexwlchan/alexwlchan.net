---
layout: post
title: Handling JSON objects with duplicate names in Python
summary: It's possible, although uncommon, for a JSON object to contain the same name multiple times. Here are some ways to handle that in Python.
tags:
  - python
  - json
---
Consider the following JSON object:

```
{
  "sides": 4,
  "colour": "red",
  "sides": 5,
  "colour": "blue"
}
```

Notice that the `sides` and `colour` names both appear twice!
This looks like it should be invalid, but I was surprised to learn recently that this is considered valid JSON -- there's nothing in the spec that forbids you doing this.

I recently encountered this in a Python project, and it got me thinking about how to handle it.



## What does the JSON spec say about duplicate names?

JSON is described by several standards, which [Wikipedia][standards] helpfully explains for us:

> After RFC 4627 had been available as its "informational" specification since 2006, JSON was first standardized in 2013, as [ECMA-404](https://ecma-international.org/publications-and-standards/standards/ecma-404/).
>
> [RFC 8259](https://ecma-international.org/publications-and-standards/standards/ecma-404/), published in 2017, is the current version of the Internet Standard STD 90, and it remains consistent with ECMA-404.
>
> That same year, JSON was also standardized as [ISO/IEC 21778:2017](https://www.iso.org/standard/71616.html).
>
> The ECMA and ISO/IEC standards describe only the allowed syntax, whereas the RFC covers some security and interoperability considerations.

All three of these standards explicitly allow the use of non-unique keys.

ECMA-404 and ISO/IEC 21778:2017 have identical text to describe the syntax of JSON objects, which says (emphasis mine):

> An object structure is represented as a pair of curly bracket tokens surrounding zero or more name/value pairs.
> […]
> The JSON syntax does not impose any restrictions on the *strings* used as names, **does not require that name *strings* be unique**, and does not assign any significance to the ordering of name/value pairs.
> These are all semantic considerations that may be defined by JSON processors or in specifications defining specific uses of JSON for data interchange.

RFC 8259 goes further and strongly recommends against duplicate names, but the use of [SHOULD][rfc_2119] means it isn't completely forbidden:

> The names within an object SHOULD be unique.

The same document describes the consequences of ignoring this recommendation, and creating an object with non-unique keys:

> An object whose names are all unique is interoperable in the sense that all software implementations receiving that object will agree on the name-value mappings.
> When the names within an object are not unique, the behavior of software that receives such an object is unpredictable.
> Many implementations report the last name/value pair only.
> Other implementations report an error or fail to parse the object, and some implementations report all of the name/value pairs, including duplicates.

So it's technically valid, but it's unusual.

I've never seen a use case for JSON objects with non-unique names, and I've never seen JSON objects where this was the expected syntax, as opposed to a mistake.
Most JSON parsers will silently discard all but the last instance of a duplicate name, including jq, JavaScript, and Python:

```pycon
>>> import json
>>> json.loads('{"sides": 4, "colour": "red", "sides": 5, "colour": "blue"}')
{'colour': 'blue', 'sides': 5}
```

What if I wanted to decode the whole object, or throw an exception if I see non-unique names?

This happened to me recently.
I had a handwritten JSON file, and I'd copy/paste objects to update the data.
I also had scripts which would read the file, make modifications, and write back the updated file.
I forgot to update the name on one of the JSON objects, so there were two name/value pairs with the same name.
When the script ran, it silently erased the first value.

I was able to recover the deleted value from the Git history, but I wondered how I could prevent this happening again.
How could I make the script fail, rather than silently delete data?

[ecma_404]: https://ecma-international.org/publications-and-standards/standards/ecma-404/
[rfc_8259]: https://datatracker.ietf.org/doc/html/rfc8259#section-4
[rfc_2119]: https://datatracker.ietf.org/doc/html/rfc2119#section-3
[standards]: https://en.wikipedia.org/wiki/JSON#Standards



## Decoding non-unique names in Python

When Python decodes a JSON object, it first parses the object as a list of name/value pairs, then it turns that list of name value pairs into a dictionary.

We can see this by looking at the [JSONObject function][JSONObject] in the CPython source code: it builds a list `pairs`, and at the end of the function, it calls `dict(pairs)` to turn the list into a dictionary.
This relies on the fact that `dict()` can take an iterable of key/value tuples and creates a dictionary:

```python
>>> dict([('sides', 4), ('colour', 'red')])
{'colour': 'red', 'sides': 4}
```

The docs tell us that `dict()` will [discard duplicate keys](https://docs.python.org/3/library/stdtypes.html#dict): "if a key occurs more than once, the last value for that key becomes the corresponding value in the new dictionary".
For example:

```python
>>> dict([('sides', 4), ('colour', 'red'), ('sides', 5), ('colour', 'blue')])
{'colour': 'blue', 'sides': 5}
```

However, we can tell Python to skip `dict()` and unpack the list of name/value pairs by defining a function `object_pairs_hook`, and passing it to `json.loads()`.
This function will be called with the list of name/value pairs, and can treat them in a different way.

For example, we can just return the literal list of name/value pairs:

```pycon
>>> import json
>>> json.loads(
...     '{"sides": 4, "colour": "red", "sides": 5, "colour": "blue"}',
...     object_pairs_hook=lambda pairs: pairs
... )
...
[('sides', 4), ('colour', 'red'), ('sides', 5), ('colour', 'blue')]
```

We could also use the [multidict library][multidict] to get a dict-like data structure, but which supports multiple values per key.
This is based on HTTP headers and URL query strings, two environments where it's common to have multiple values for a single key:

```pycon
>>> from multidict import MultiDict
>>> md = json.loads(
...     '{"sides": 4, "colour": "red", "sides": 5, "colour": "blue"}',
...     object_pairs_hook=lambda pairs: MultiDict(pairs)
... )
...
>>> md
<MultiDict('sides': 4, 'colour': 'red', 'sides': 5, 'colour': 'blue')>
>>> md['sides']
4
>>> md.getall('sides')
[4, 5]
```

If we want to throw an error when we see duplicate names, we need a slightly longer function.
Here's the code I wrote:

```python
import collections
import typing


def dict_with_unique_names(pairs: list[tuple[str, typing.Any]]) -> dict[str, typing.Any]:
    """
    Convert a list of name/value pairs to a dict, but only if the
    names are unique.

    If there are non-unique names, this function throws a ValueError.
    """
    # First try to parse the object as a dictionary; if it's the same
    # length as the pairs, then we know all the names were unique and
    # we can return immediately.
    pairs_as_dict = dict(pairs)

    if len(pairs_as_dict) == len(pairs):
        return pairs_as_dict

    # Otherwise, let's work out what the repeated name(s) were, so we
    # can throw an appropriate error message for the user.
    name_tally = collections.Counter(n for n, _ in pairs)

    repeated_names = [n for n, count in name_tally.items() if count > 1]
    assert len(repeated_names) > 0

    if len(repeated_names) == 1:
        raise ValueError(f"Found repeated name in JSON object: {repeated_names[0]}")
    else:
        raise ValueError(
            f"Found repeated names in JSON object: {', '.join(repeated_names)}"
        )
```

If I use this as my `object_pairs_hook` when parsing an object which has unique names, it returns the normal `dict` I'd expect:

```pycon
>>> json.loads(
...     '{"sides": 4, "colour": "red"}',
...     object_pairs_hook=dict_with_unique_names
... )
...
{'colour': 'red', 'sides': 4}
```

But if I use this as my `object_pairs_hook` when parsing an object with one or more repeated names, the parsing fails and I get a `ValueError`:

```pycon
>>> json.loads(
...     '{"sides": 4, "colour": "red", "sides": 5}',
...      object_pairs_hook=dict_with_unique_names
... )
Traceback (most recent call last):
[…]
ValueError: Found repeated name in JSON object: sides

>>> json.loads(
...     '{"sides": 4, "colour": "red", "sides": 5, "colour": "blue"}',
...     object_pairs_hook=dict_with_unique_names
... )
Traceback (most recent call last):
[…]
ValueError: Found repeated names in JSON object: sides, colour
```

This is precisely the behaviour I want -- throwing an exception, not silently dropping data.

[JSONObject]: https://github.com/python/cpython/blob/a247dd300ea0c839154e2e38dbc0fdc9fdff673f/Lib/json/decoder.py#L137-L219
[multidict]: https://multidict.aio-libs.org/en/stable/



## Encoding non-unique names in Python

Admittedly, I can't think of a time when I'd want to do this, but this post feels incomplete without at least a brief mention.

If you want to encode custom data structures with Python's JSON library, you can subclass [`JSONEncoder`][JSONEncoder] and implement JSON serialisation for your custom structures.
Here's a rudimentary attempt at doing that for a `MultiDict`:

```python
class MultiDictEncoder(json.JSONEncoder):

    def encode(self, o: typing.Any) -> str:
        # If this is a MultiDict, we need to construct the JSON string
        # manually -- first encode each name/value pair, then construct
        # the JSON object literal.
        if isinstance(o, MultiDict):
            name_value_pairs = [
                f'{super().encode(str(name))}: {self.encode(value)}'
                for name, value in o.items()
            ]

            return '{' + ', '.join(name_value_pairs) + '}'

        return super().encode(o)
```

and here's how you use it:

```pycon
>>> md = MultiDict([('sides', 4), ('colour', 'red'), ('sides', 5), ('colour', 'blue')])
>>> json.dumps(md, cls=MultiDictEncoder)
{"sides": 4, "colour": "red", "sides": 5, "colour": "blue"}
```

This code doesn't handle indentation and there are probably bugs in the way I'm constructing the JSON string by hand, but it gives you an idea of how something like this could work.

In practice, if I had to encode a multi-dict as JSON, I'd be more likely to encode it as a list of objects with a `key` and a `value` field.
For example:

```
[
  {"key": "sides",  "value": 4     },
  {"key": "colour", "value": "red" },
  {"key": "sides",  "value": 5     },
  {"key": "colour", "value": "blue"},
]
```

This is a much more common pattern, and is unlikely to trip up JSON parsers which aren't expecting non-unique names.

[JSONEncoder]: https://docs.python.org/3/library/json.html#json.JSONEncoder



## When will I use this code?

JSON objects with non-unique names are fairly unusual -- this is the first time I've ever encountered one, and it was a copy/paste error.
Trying to account for this edge case in every project that uses JSON feels like overkill.
It would add complexity to my code and probably never catch a single error.

I've been thinking about how this problem occurred and why it was a problem.
A human making a copy/paste error introduced the initial duplicated keys, and a program modifying the JSON file turned that into a data loss bug.

If a JSON file is exclusively modified by computers, this won't be an issue.
Most JSON libraries won't write objects with repeated names unless you explicitly tell them to do so (like writing a custom encoder), and then it would be very obvious this needs to be handled in the decoder also.

If a JSON file is exclusively modified by humans, this won't be an issue.
They're more likely to make a mistake that introduces a repeated name, but they won't delete data just because it has a duplicate name.
They'll stop, think, and work out what the right thing is to do with this data.

This is only likely to be an issue if you have a JSON file which is modified by humans and computers alike.

That's the case for some of my [static website archives](/2025/mildly-dynamic-websites/), which store metadata as JSON in JavaScript files, and it's where I made the original mistake.
I've added this error handling to my [javascript-data-files library](https://github.com/alexwlchan/javascript-data-files), but I don't anticipate adding it to other projects.
It's useful to know that JSON supports this in theory, but it's so rare in practice that I'm not overly concerned.
