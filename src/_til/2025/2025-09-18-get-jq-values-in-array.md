---
layout: til
title: Get a list of values in a JSON object with jq
summary: The equivalent to Python's `dict.values()` is `jq '[.[]]'`.
date: 2025-09-18 13:51:08 +01:00
tags:
  - jq
---
Here's an example:

```console
$ echo '{"1": ["one", "uno", "eins"], "2": ["two", "dos", "zwei"], "3": ["three", "tres", "drei"]}' > numbers.json

$ jq -c '[.[]]' numbers.json
[["one","uno","eins"],["two","dos","zwei"],["three","tres","drei"]]
```

How it works:

*   `.[]` is the [object value iterator](https://jqlang.org/manual/#array-object-value-iterator), which returns all the values of an object.

    ```console
    $ jq -c '.[]' numbers.json
    ["one","uno","eins"]
    ["two","dos","zwei"]
    ["three","tres","drei"]
    ```

*   `[]` [constructs an array](https://jqlang.org/manual/#array-construction) from whatever is passed in.
