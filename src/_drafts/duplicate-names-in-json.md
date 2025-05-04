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



## That's really valid JSON?

Yup!

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

This happened to me recently in a project.
We had a handwritten JSON file, and people would copy/paste objects to update the data.
We also had scripts which would read the file, make modifications, and write back the updated file.
Somebody forgot to update the name on one of the JSON objects, so we had two instances of the same name.
When the script ran, it silently erased the first instance of the name. 

We were able to recover the deleted value from the Git history, but I wondered how we could prevent this happening again.
How could we make the script fail, rather than throwing an explicit error? 

[ecma_404]: https://ecma-international.org/publications-and-standards/standards/ecma-404/
[rfc_8259]: https://datatracker.ietf.org/doc/html/rfc8259#section-4
[rfc_2119]: https://datatracker.ietf.org/doc/html/rfc2119#section-3
[standards]: https://en.wikipedia.org/wiki/JSON#Standards
