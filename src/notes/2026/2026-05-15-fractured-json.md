---
layout: note
date: 2026-05-15 08:56:07 +01:00
title: Format "human-readable" JSON with FracturedJSON
summary: Short objects and arrays are compressed onto a single line; larger objects are displayed as a table. Available in a variety of languages.
link: https://github.com/j-brooke/FracturedJson/wiki
topics:
  - Computers and code
hidden_topics:
  - JSON
---
Here's an interesting project that balances compact and human-readable JSON, automatically applying certain sensibilities that somebody might add if they were writing JSON by hand:

> FracturedJson is a family of utilities that format JSON data in a way that's easy for humans to read, but fairly compact. Arrays and objects are written on single lines, as long as they're neither too long nor too complex. When several such lines are similar in structure, they're written with fields aligned like a table. Long arrays are written with multiple items per line across multiple lines.

Here's an example of the output it produces:

```json
{
    "BasicObject"   : {
        "ModuleId"   : "armor",
        "Name"       : "",
        "Locations"  : [
            [11,  2], [11,  3], [11,  4], [11,  5], [11,  6], [11,  7], [11,  8], [11,  9],
            [11, 10], [11, 11], [11, 12], [11, 13], [11, 14], [ 1, 14], [ 1, 13], [ 1, 12],
            [ 1, 11], [ 1, 10], [ 1,  9], [ 1,  8], [ 1,  7], [ 1,  6], [ 1,  5], [ 1,  4],
            [ 1,  3], [ 1,  2], [ 4,  2], [ 5,  2], [ 6,  2], [ 7,  2], [ 8,  2], [ 8,  3],
            [ 7,  3], [ 6,  3], [ 5,  3], [ 4,  3], [ 0,  4], [ 0,  5], [ 0,  6], [ 0,  7],
            [ 0,  8], [12,  8], [12,  7], [12,  6], [12,  5], [12,  4]
        ],
        "Orientation": "Fore",
        "Seed"       : 272691529
    },
    "SimilarArrays" : {
        "Katherine": ["blue",       "lightblue", "black"       ],
        "Logan"    : ["yellow",     "blue",      "black", "red"],
        "Erik"     : ["red",        "purple"                   ],
        "Jean"     : ["lightgreen", "yellow",    "black"       ]
    },
    "SimilarObjects": [
        { "type": "turret",    "hp": 400, "loc": {"x": 47, "y":  -4}, "flags": "S"   },
        { "type": "assassin",  "hp":  80, "loc": {"x": 12, "y":   6}, "flags": "Q"   },
        { "type": "berserker", "hp": 150, "loc": {"x":  0, "y":   0}                 },
        { "type": "pittrap",              "loc": {"x": 10, "y": -14}, "flags": "S,I" }
    ]
}
```

I haven't tried the code at all, but noting so I can find the project again.

There are implementations in several languages, including .NET, JavaScript, Rust, and Python.
The Python libraries are thin wrappers around the .NET and Rust versions, or there's a [deprecated `compact-json` project][gh-compact-json] that's written in pure Python.
It also reminds me of Tailscale's [HuJSON library][gh-hujson], which lines up object keys in a similar way when you format your JSON.

For a while I've wanted something like this for [javascript-data-files][me-javascript-data-files], and I had a brief attempt at it -- but this is a much harder problem than I initially realised.
I don't want this behaviour enough to add a dependency, and it's more complicated than I want to implement or maintain on my own (even if I vendor an existing project).

[gh-compact-json]: https://github.com/masaccio/compact-json
[gh-hujson]: https://github.com/tailscale/hujson
[me-javascript-data-files]: /projects/javascript-data-files/
