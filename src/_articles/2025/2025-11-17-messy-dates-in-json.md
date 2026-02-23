---
layout: article
date: 2025-11-17 08:52:48 +00:00
title: Cleaning up messy dates in JSON
summary: I wrote a Python script to help me get timestamps in a consistent format in my JSON.
topics:
  - Python
  - Datetime shenanigans
---
I've been cleaning up some messy data, and it includes timestamps written by a variety of humans and machines, which don't use a consistent format.

Here are a few examples:

```
2025-10-14T05:34:07+0000
2015-03-01 23:34:39 +00:00
2013-9-21 13:43:00Z
2024-08-30
```

All of these timestamps are machine-readable, but it would be easier for the downstream code if there weren't as many different formats.
For example, the downstream code uses the JavaScript [`Date()` constructor][js_date], which rejects some of the timestamps as invalid.

I wrote a Python script to help me find, validate, and normalise all my timestamps, so the rest of my code can deal with a more consistent set.

[js_date]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date

{% table_of_contents %}

## Finding all the date strings

All the messy data is in JSON, and the structure is quite inconsistent -- a lot of heavily nested objects, differently-named fields, varying models and schemas.
This project is about tidying it up.

One saving gracing is that the timestamps are named fairly consistently -- they're all stored inside JSON objects, with keys that start with `date_`, and values which are strings.
Here's an example:

```json
{
  "doc1": {"id": "1", "date_created": "2025-10-14T05:34:07+0000"},
  "shapes": [
  	{"color": "blue", "date_saved": "2015-03-01 23:34:39 +00:00"},
  	{"color": "yellow", "date_saved": "2013-9-21 13:43:00Z", "is_square": true},
  	{"color": "green", "date_saved": null}
  ],
  "date_verified": "2024-08-30"
}
```

The first thing I want to do is find all the key-value pairs which combine a `date_` and a string.

I wrote a Python function to recursively walk the JSON and pull out matching pairs.
I'm sure there are libraries for this, but JSON is simple enough that I can write it by hand.
It only has a few types, and even fewer that matter here:

*   If it's a JSON object: inspect its keys, then recurse into each value
*   If it's a JSON array: recurse into each element
*   If it's a string, number, bool, or null: ignore it

Here's my code:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"typing","5":"Any","6":"find_all_dates","7":"json_value","19":"key","20":"value","39":"value"}}
from collections.abc import Iterator
from typing import Any


def find_all_dates(json_value: Any) -> Iterator[tuple[dict[str, Any], str, str]]:
    """
    Find all the timestamps in a heavily nested JSON object.

    This function looks for any JSON objects with a key-value pair
    where the key starts with `date_` and the value is a string, and
    emits a 3-tuple:

    *   the JSON object
    *   the key
    *   the value

    """
    # Case 1: JSON objects
    if isinstance(json_value, dict):
        for key, value in json_value.items():
            if (
                isinstance(key, str)
                and key.startswith("date_")
                and isinstance(value, str)
            ):
                yield json_value, key, value
            else:
                yield from find_all_dates(value)

    # Case 2: JSON arrays
    elif isinstance(json_value, list):
        for value in json_value:
            yield from find_all_dates(value)

    # Case 3: other JSON types
    elif isinstance(json_value, (str, int, bool)) or json_value is None:
        return

    # Case 4: handle unexpected types
    else:
        raise TypeError(f"Unexpected type: {type(json_value)}")
```

There are branches for all the builtin JSON types, then a catch-all branch for anything else.

I added a catch-all `TypeError` branch to catch list- or dict-like inputs that aren't actually JSON types -- things like `dict.values()` or custom container classes.
Without this check, they'd fall through to the "ignore" case and quietly drop nested data.
An explicit error makes the failure obvious, and the fix is easy: wrap the input in `list()` or `dict()`.

For each timestamp it finds, the function emits a tuple with the nested object, the key and the value.
For the example above, here's the first tuple it returns:

```python
({"id": "1", "date_created": "2025-10-14T05:34:07+0000"},
 "date_created",
 "2025-10-14T05:34:07+0000")
```

This return type allows me to both read and modify the JSON with the same function:

```python {"names":{"3":"date_string","8":"json_obj","9":"key","10":"date_string"}}
# Reading the timestamps
for _, _, date_string in find_all_dates(json_value):
    print(date_string)

# Modifying the timestamps
for json_obj, key, date_string in find_all_dates(json_value):
    json_obj[key] = run_fixup(date_string)
```

The latter works because `json_obj` points to the actual dictionary from the nested JSON, not a copy, so when we assign `json_obj[key] = …`, we modify the original JSON structure in-place.

Now we can find all the timestamps, we need to check if they use a consistent datetime format.

## Checking if a date string matches a given format

I normally parse timestamps in Python with the [`datetime.strptime` function][strptime].
This is quite a strict function, because you have to pass it a [format string][strptime_fmt_code] that describes exactly how you expect the timestamp to be formatted.

If you want a more flexible approach, you can use the [`python-dateutil` module][dateutil], which has a [generic parser][parser] that guesses how to read the timestamp, rather than asking you to specify.

I prefer strict parsing, because I (usually!) know exactly how timestamps will be formatted, and inconsistent formats can hide bugs.
There's no room for ambiguity, and no risk of a timestamp being guessed incorrectly.

The `strptime` function takes two arguments: the string you want to parse, and the format string.
Here's an example:

```pycon {"names":{"1":"datetime","2":"datetime"}}
>>> from datetime import datetime
>>> datetime.strptime("2001-02-03T04:05:06+00:00", "%Y-%m-%dT%H:%M:%S%z")
datetime.datetime(2001, 2, 3, 4, 5, 6, tzinfo=datetime.timezone.utc)
```

If you pass a timestamp that doesn't match the format string, it throws a ValueError:

```pycon
>>> datetime.strptime("2001-02-03", "%Y-%m-%dT%H:%M:%S%z")
ValueError: time data '2001-02-03' does not match format '%Y-%m-%dT%H:%M:%S%z'
```

It also checks that the whole string is parsed, and throws a ValueError if it's an incomplete match:

```pycon
>>> datetime.strptime("2001-02-03T04:05:06+00:00", "%Y-%m-%d")
ValueError: unconverted data remains: T04:05:06+00:00
```

This allows us to write a function that checks if a timestamp matches a given format:

```python {"names":{"1":"datetime","2":"datetime","3":"date_matches_format","4":"date_string","6":"format"}}
from datetime import datetime


def date_matches_format(date_string: str, format: str) -> bool:
    """
    Returns True if `date_string` can be parsed as a datetime
    using `format`, False otherwise.
    """
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False
```

The `format` can be any format code supported by `strptime()`.
The [Python docs](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) have a list of all the accepted format codes.
That list includes a couple of non-standard format codes which only have partial support, which is part of why I want to clean up these date strings.

If we want to allow multiple formats, we can wrap this function [using `any()`][any]:

```python {"names":{"1":"date_matches_any_format","2":"date_string","4":"formats","12":"fmt"}}
def date_matches_any_format(date_string: str, formats: tuple[str]) -> bool:
    """
    Returns True if `date_string` can be parsed as a datetime
    with any of the `formats`, False otherwise.
    """
    return any(
        date_matches_format(date_string, fmt)
        for fmt in formats
    )
```

Here's how we can use this function to find any timestamps that don't match our allowed formats:

```python {"names":{"1":"allowed_formats","4":"date_string"}}
allowed_formats = (
    # 2001-02-03T04:05:06+07:00
    "%Y-%m-%dT%H:%M:%S%z",
    #
    # 2001-02-03
    "%Y-%m-%d",
)

for _, _, date_string in find_all_dates(json_value):
    if not date_matches_any_format(date_string, allowed_formats):
        print(date_string)
```

[strptime]: https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
[strptime_fmt_code]: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
[dateutil]: https://dateutil.readthedocs.io/en/stable/index.html
[parser]: https://dateutil.readthedocs.io/en/stable/parser.html
[any]: https://docs.python.org/3/library/functions.html#any

## Testing that all of my timestamps use consistent formats

With these two functions in hand, I wrote a test I can run with pytest to tell me about any timestamps that don't match my allowed formats:

```python {"names":{"1":"test_all_timestamps_are_consistent","2":"allowed_formats","3":"bad_date_strings","7":"date_string"}}
def test_all_timestamps_are_consistent():
    """
    All the timestamps in my JSON use a consistent format.

    See https://alexwlchan.net/2025/messy-dates-in-json/
    """
    allowed_formats = (
        # 2001-02-03T04:05:06+07:00
        "%Y-%m-%dT%H:%M:%S%z",
        #
        # 2001-02-03
        "%Y-%m-%d",
    )

    bad_date_strings = {
        date_string
        for _, _, date_string in find_all_dates(JSON_DATA)
        if not date_matches_any_format(date_string, allowed_formats)
    }

    assert bad_date_strings == set()
```

If you only allow a single format, you could simplify this slightly by using `date_matches_format`.

If the test passes, all your timestamps match the allowed formats.
If the test fails, pytest prints the ones that don't.
Running it on our original example shows two disallowed timestamps:

```
AssertionError: assert {'2013-9-21 1...34:39 +00:00'} == set()

  Extra items in the left set:
  '2015-03-01 23:34:39 +00:00'
  '2013-9-21 13:43:00Z'
```

As with the test I wrote [in my last post](/2025/detecting-av1-videos/#writing-a-test-to-find-videos-with-the-av1-codec), I like to report on all the failing values, not just the first one.
This allows me to see the scale of the problem, and see patterns in the failing output -- if I see a bad timestamp, is it a one-off issue I should fix by hand, or does it affect thousands of values that need an automatic cleanup?

When I first ran this test, it failed with thousands of errors.
I cleaned up the data and re-ran the test until it passed, and now I can keep running it to ensure no unexpected values sneak back in.

## Changing the format of date strings in bulk

This test revealed thousands of errors, and I didn't want to fix them all by hand.
That would be slow, tedious, and prone to manual errors.
But among the timestamps I wanted to change, there were pockets of consistency -- each tool that contributed to this data would write timestamps in a single format, and I could convert all the timestamps from that tool in one go.

I wrote one-off fixer scripts to perform these conversions.
Each script would read the JSON file, look for date strings in a given format, convert them to my preferred format, then write the result back to my JSON file:
Here's one example:

```python {"names":{"1":"json","2":"old_format","3":"new_format","5":"in_file","6":"json_data","10":"json_obj","11":"key","12":"date_string","18":"d","29":"out_file"}}
import json


# e.g. 2001-02-03 04:05:06 +07:00
old_format = "%Y-%m-%d %H:%M:%S %z"

# e.g. 2001-02-03T04:05:06+07:00 (datetime.isoformat())
new_format = "%Y-%m-%dT%H:%M:%S%z"


with open("my_data.json") as in_file:
    json_data = json.load(in_file)

for json_obj, key, date_string in find_all_dates(json_data):
    if date_matches_format(date_string, old_format):
        d = datetime.strptime(date_string, old_format)
        json_obj[key] = d.strftime(new_format)

with open("my_data.json", "w") as out_file:
    out_file.write(json.dumps(json_data, indent=2))
```

I keep my JSON data files in Git, and I committed every time I ran a successful script.
That made it easy to see the changes from each fix-up, and to revert them if I made a mistake.

The nice thing about this approach is that each script is quite small and simple, because it's only trying to fix one thing at a time.
But each script adds up, and [salami slicing] eventually ends up with dramatically cleaner data.
I didn't fix everything this way (some typos were quicker to fix by hand), but scripting fixed the majority of issues.

[salami slicing]: https://en.wikipedia.org/wiki/Salami_slicing



## Putting it all together

Here's what we've done in this post:

*   Written a recursive function to find all the timestamps in a JSON value
*   Chosen the timestamp formats we allow, and added helpers to check them
*   Added a test to find and prevent unexpected formats
*   Written one-off migration scripts to clean up old timestamps

Here's the final test which ties this all together.
I've saved it as `test_date_formats.py`:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"datetime","5":"datetime","6":"typing","7":"Any","8":"find_all_dates","9":"json_value","21":"key","22":"value","41":"value","54":"date_matches_format","55":"date_string","57":"format","65":"date_matches_any_format","66":"date_string","68":"formats","76":"fmt","78":"test_all_timestamps_are_consistent","79":"allowed_formats","80":"bad_date_strings","84":"date_string"}}
from collections.abc import Iterator
from datetime import datetime
from typing import Any


def find_all_dates(json_value: Any) -> Iterator[tuple[dict[str, Any], str, str]]:
    """
    Find all the timestamps in a heavily nested JSON object.

    This function looks for any JSON objects with a key-value pair
    where the key starts with `date_` and the value is a string, and
    emits a 3-tuple:

    *   the JSON object
    *   the key
    *   the value

    """
    # Case 1: JSON objects
    if isinstance(json_value, dict):
        for key, value in json_value.items():
            if (
                isinstance(key, str)
                and key.startswith("date_")
                and isinstance(value, str)
            ):
                yield json_value, key, value
            else:
                yield from find_all_dates(value)

    # Case 2: JSON arrays
    elif isinstance(json_value, list):
        for value in json_value:
            yield from find_all_dates(value)

    # Case 3: other JSON types
    elif isinstance(json_value, (str, int, bool)) or json_value is None:
        return []

    # Case 4: handle unexpected types
    else:
        raise TypeError(f"Unexpected type: {type(json_value)}")


def date_matches_format(date_string: str, format: str) -> bool:
    """
    Returns True if `date_string` can be parsed as a datetime
    using `format`, False otherwise.
    """
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False


def date_matches_any_format(date_string: str, formats: tuple[str]) -> bool:
    """
    Returns True if `date_string` can be parsed as a datetime
    with any of the `formats`, False otherwise.
    """
    return any(
        date_matches_format(date_string, fmt)
        for fmt in formats
    )


def test_all_timestamps_are_consistent():
    """
    All the timestamps in my JSON use a consistent format.

    See https://alexwlchan.net/2025/messy-dates-in-json/
    """
    # TODO: Write code for reading JSON_DATA

    allowed_formats = (
        # 2001-02-03T04:05:06+07:00
        "%Y-%m-%dT%H:%M:%S%z",
        #
        # 2001-02-03
        "%Y-%m-%d",
    )

    bad_date_strings = {
        date_string
        for _, _, date_string in find_all_dates(JSON_DATA)
        if not date_matches_any_format(date_string, allowed_formats)
    }

    assert bad_date_strings == set()
```

If you want to use this test, you'll need to modify it to read your JSON data, and to specify the list of timestamp formats you accept.

Although I've since cleaned up the data so it has a more consistent structure, this test has remained as-is.
I could write a more specific test that knows about my JSON schema and looks for timestamps in specific fields, but I quite like having a generic test that doesn't need to change when I change my data model.
The flexibility also means it's easy to copy across projects, and I've reused this test almost unmodified in several tests already.
