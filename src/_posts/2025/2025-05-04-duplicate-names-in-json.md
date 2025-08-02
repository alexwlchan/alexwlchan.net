---
layout: post
date: 2025-05-04 15:17:01 +0000
title: Handling JSON objects with duplicate names in Python
summary: It's possible, although uncommon, for a JSON object to contain the same name multiple times. Here are some ways to handle that in Python.
tags:
  - python
  - json
---

Consider the following JSON object:

```
{
  "sides":  4,
  "colour": "red",
  "sides":  5,
  "colour": "blue"
}
```

Notice that `sides` and `colour` both appear twice.
This looks invalid, but I learnt recently that this is actually legal JSON syntax!
It's unusual and discouraged, but it's not completely forbidden.

This was a big surprise to me.
I think of JSON objects as key/value pairs, and I associate them with data structures like a `dict` in Python or a `Hash` in Ruby -- both of which only allow unique keys.
JSON has no such restriction, and I started thinking about how to handle it.

{% table_of_contents %}



## What does the JSON spec say about duplicate names?

JSON is described by several standards, which [Wikipedia][standards] helpfully explains for us:

> After RFC 4627 had been available as its "informational" specification since 2006, JSON was first standardized in 2013, as [ECMA-404](https://ecma-international.org/publications-and-standards/standards/ecma-404/).
>
> [RFC 8259](https://ecma-international.org/publications-and-standards/standards/ecma-404/), published in 2017, is the current version of the Internet Standard STD 90, and it remains consistent with ECMA-404.
>
> That same year, JSON was also standardized as [ISO/IEC 21778:2017](https://www.iso.org/standard/71616.html).
>
> The ECMA and ISO/IEC standards describe only the allowed syntax, whereas the RFC covers some security and interoperability considerations.

All three of these standards explicitly allow the use of duplicate names in objects.

ECMA-404 and ISO/IEC 21778:2017 have identical text to describe the syntax of JSON objects, and they say (emphasis mine):

> An object structure is represented as a pair of curly bracket tokens surrounding zero or more name/value pairs.
> […]
> The JSON syntax does not impose any restrictions on the *strings* used as names, **does not require that name *strings* be unique**, and does not assign any significance to the ordering of name/value pairs.
> These are all semantic considerations that may be defined by JSON processors or in specifications defining specific uses of JSON for data interchange.

RFC 8259 goes further and strongly recommends against duplicate names, but the use of [SHOULD][rfc_2119] means it isn't completely forbidden:

> The names within an object SHOULD be unique.

The same document warns about the consequences of ignoring this recommendation:

> An object whose names are all unique is interoperable in the sense that all software implementations receiving that object will agree on the name-value mappings.
> When the names within an object are not unique, the behavior of software that receives such an object is unpredictable.
> Many implementations report the last name/value pair only.
> Other implementations report an error or fail to parse the object, and some implementations report all of the name/value pairs, including duplicates.

So it's technically valid, but it's unusual and discouraged.

I've never heard of a use case for JSON objects with duplicate names.
I'm sure there was a good reason for it being allowed by the spec, but I can't think of it.

Most JSON parsers -- including jq, JavaScript, and Python -- will silently discard all but the last instance of a duplicate name.
Here's an example in Python:

```pycon
>>> import json
>>> json.loads('{"sides": 4, "colour": "red", "sides": 5, "colour": "blue"}')
{'colour': 'blue', 'sides': 5}
```

What if I wanted to decode the whole object, or throw an exception if I see duplicate names?

This happened to me recently.
I was editing a JSON file by hand, and I'd copy/paste objects to update the data.
I also had scripts which could update the file.
I forgot to update the name on one of the JSON objects, so there were two name/value pairs with the same name.
When I ran the script, it silently erased the first value.

I was able to recover the deleted value from the Git history, but I wondered how I could prevent this happening again.
How could I make the script fail, rather than silently delete data?

[ecma_404]: https://ecma-international.org/publications-and-standards/standards/ecma-404/
[rfc_8259]: https://datatracker.ietf.org/doc/html/rfc8259#section-4
[rfc_2119]: https://datatracker.ietf.org/doc/html/rfc2119#section-3
[standards]: https://en.wikipedia.org/wiki/JSON#Standards



## Decoding duplicate names in Python

When Python decodes a JSON object, it first parses the object as a list of name/value pairs, then it turns that list of name value pairs into a dictionary.

We can see this by looking at the [JSONObject function][JSONObject] in the CPython source code: it builds a list `pairs`, and at the end of the function, it calls `dict(pairs)` to turn the list into a dictionary.
This relies on the fact that `dict()` can take an iterable of key/value tuples and create a dictionary:

```python
>>> dict([('sides', 4), ('colour', 'red')])
{'colour': 'red', 'sides': 4}
```

The docs for `dict()` tell us that it will [discard duplicate keys](https://docs.python.org/3/library/stdtypes.html#dict): "if a key occurs more than once, the last value for that key becomes the corresponding value in the new dictionary".

```python
>>> dict([('sides', 4), ('colour', 'red'), ('sides', 5), ('colour', 'blue')])
{'colour': 'blue', 'sides': 5}
```

We can customise what Python does with the list of name/value pairs.
Rather than calling `dict()`, we can pass our own function to the `object_pairs_hook` parameter of `json.loads()`, and Python will call that function on the list of pairs.
This allows us to parse objects in a different way.

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

We could also use the [multidict library][multidict] to get a dict-like data structure which supports multiple values per key.
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



## Preventing silent data loss

If we want to throw an exception when we see duplicate names, we need a longer function.
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

If I use this as my `object_pairs_hook` when parsing an object which has all unique names, it returns the normal `dict` I'd expect:

```pycon
>>> json.loads(
...     '{"sides": 4, "colour": "red"}',
...     object_pairs_hook=dict_with_unique_names
... )
...
{'colour': 'red', 'sides': 4}
```

But if I'm parsing an object with one or more repeated names, the parsing fails and throws a `ValueError`:

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

It's hard to think of a use case, but this post feels incomplete without at least a brief mention.

If you want to encode custom data structures with Python's JSON library, you can subclass [`JSONEncoder`][JSONEncoder] and define how those structures should be serialised.
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

This is rough code, and you shouldn't use it -- it's only an example.
I'm constructing the JSON string manually, so it doesn't handle edge cases like indentation or special characters.
There are almost certainly bugs, and you'd need to be more careful if you wanted to use this for real.

In practice, if I had to encode a multi-dict as JSON, I'd encode it as a list of objects which each have a `key` and a `value` field.
For example:

```
[
  {"key": "sides",  "value": 4     },
  {"key": "colour", "value": "red" },
  {"key": "sides",  "value": 5     },
  {"key": "colour", "value": "blue"},
]
```

This is a pretty standard pattern, and it won't trip up JSON parsers which aren't expecting duplicate names.

[JSONEncoder]: https://docs.python.org/3/library/json.html#json.JSONEncoder



## Do you need to worry about this?

This isn't a big deal.
JSON objects with duplicate names are pretty unusual -- this is the first time I've ever encountered one, and it was a mistake.

Trying to account for this edge case in every project that uses JSON would be overkill.
It would add complexity to my code and probably never catch a single error.

This started when I made a copy/paste error that introduced the initial duplication, and then a script modified the JSON file and caused some data loss.
That's a somewhat unusual workflow, because most JSON files are exclusively modified by computers, and this wouldn't be an issue.

I've added this error handling to my [javascript-data-files library](https://github.com/alexwlchan/javascript-data-files), but I don't anticipate adding it to other projects.
I use that library for my [static website archives](/2025/mildly-dynamic-websites/), which is where I had this issue.

Although I won't use this code exactly, it's been good practice at writing custom encoders/decoders in Python.
That *is* something I do all the time -- I'm often encoding native Python types as JSON, and I want to get the same type back when I decode later.

I've been writing my own subclasses of `JSONEncoder` and `JSONDecoder` for a while.
Now I know a bit more about how Python decodes JSON, and `object_pairs_hook` is another tool I can consider using.
This was a fun deep dive for me, and I hope you found it helpful too.
