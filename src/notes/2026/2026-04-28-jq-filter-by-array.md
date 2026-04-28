---
layout: note
date: 2026-04-28 22:52:44 +01:00
title: Filter a list of JSON object based on a list of tags
summary: Use the `arrays` filter to remove empty values, the `any(…)` filter to check for set inclusion, then wrap the whole thing in square brackets.
topic: jq
---
Here's a problem I've had several times recently: I have an array of JSON objects which have an array of string tags, and I want to filter for objects with matching tags.
Sometimes the array of tags is `null` rather than an empty list.

Here's an example:

```json
[
  {"id": "square",    "tags": ["quadrilateral", "2d"]},
  {"id": "rectangle", "tags": ["quadrilateral", "2d"]},
  {"id": "triangle",  "tags": ["2d"]},
  {"id": "blob",      "tags": null},
  {"id": "tagless"}
]
```

(The field isn't always called `tags`, but this general pattern is common.)

Here's the jq filter I need:

```shell {"wrap":true}
jq '[ .[] | select(.tags | arrays and any(. == "quadrilateral")) ]'
```

whcih returns the following output:

```json
[
  {
    "id": "square",
    "tags": [
      "quadrilateral",
      "2d"
    ]
  },
  {
    "id": "rectangle",
    "tags": [
      "quadrilateral",
      "2d"
    ]
  }
]
```

## How it works

-   `.[]` is the [array value iterator][jq-array-val-iterator], which iterates over the objects in the array.

-   the [`select(…)` function][jq-select-function] filters the array for matching objects.

-   `.tags` is an [object identifier-index][jq-obj-id-index]; it looks up the `"tags"` key in the object.

-   `arrays` is a [built-in filter][jq-arrays-filter] that filters for objects where `.tags` is an array, so it discards objects where `tags` is missing or null.

-   the [`any(…)` filter][jq-any-filter] filters for tag arrays where one of the items is equal to `"quadrilateral"`.

-   the `[…]` around the whole expression wraps the result in a new array.
    Skip them if you want one object per line.

Notably, I'm not using the [`contains(…)` filter][jq-contains-filter].
Although it sounds useful, it can only test items of the same type -- it can test if a string contains a substring, or if an array is a superset of another array, but it can't test if an array contains a string.

[jq-array-val-iterator]: https://jqlang.org/manual/#array-object-value-iterator
[jq-select-function]: https://jqlang.org/manual/#select
[jq-obj-id-index]: https://jqlang.org/manual/#object-identifier-index
[jq-arrays-filter]: https://jqlang.org/manual/#arrays-objects-iterables-booleans-numbers-normals-finites-strings-nulls-values-scalars
[jq-any-filter]: https://jqlang.org/manual/#any
[jq-contains-filter]: https://jqlang.org/manual/#contains
