---
layout: til
title: How to find the longest common suffix in a list of strings in Python
date: 2024-01-14 09:27:19 +00:00
tags:
  - python
---
There are lots of ways to do this; this is my go-to implementation that pushes the heavy lifting off to `os.path.commonprefix`, and seems to have served me fairly well so far.
Plus tests!

```python
import os


def get_common_suffix(strings: list[str]) -> str:
    reversed_strings = ["".join(reversed(s)) for s in strings]
    common_prefix = os.path.commonprefix(reversed_strings)
    return "".join(reversed(common_prefix))


from hypothesis import given
from hypothesis import strategies as st
import pytest


@pytest.mark.parametrize(
    ["s1", "s2", "common_suffix"], [("", "", ""), ("", "abc", ""), ("abc", "bc", "bc")]
)
def test_get_common_suffix(s1, s2, common_suffix):
    assert get_common_suffix([s1, s2]) == common_suffix


@given(st.text())
def test_get_common_suffix_of_single_string_is_itself(s):
    assert get_common_suffix([s]) == s


@given(st.text(), st.text())
def test_by_fuzzing_get_common_suffix(s1, s2):
    suffix = get_common_suffix([s1, s2])

    if suffix == "":
        assert len(s1) == 0 or len(s2) == 0 or s1[-1] != s2[-1]
    else:
        assert s1[-len(suffix) :] == suffix
        assert s2[-len(suffix) :] == suffix

        assert (
            s1 == suffix or s2 == suffix or s1[-len(suffix) - 1] != s2[-len(suffix) - 1]
        )
```
