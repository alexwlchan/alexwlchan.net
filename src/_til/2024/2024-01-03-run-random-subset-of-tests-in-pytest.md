---
layout: til
title: Run a randomly selected subset of tests with pytest
date: 2024-01-03 17:22:34 +00:00
summary: |
  By reading the code for the `pytest-random-order` plugin, I was able to write a new plugin that runs a random subset of tests.
tags:
  - python
  - python:pytest
---
This is a question asked [by Ned Batchelder][nedbat] on Mastodon.

There's a plugin [pytest-random-order] that runs your pytest suite in random order, but it runs a complete set of tests.

I looked for a way to limit the number of tests that pytest runs, and I found [a Stack Overflow answer by hoefling][hoefling] that implements a `--limit=N` flag for pytest.
I was able to adapt it to run a random subset of tests.

Add this to `conftest.py`:

```python
import random


def pytest_addoption(parser):
    parser.addoption(
        "--random-selection",
        metavar="N",
        action="store",
        default=-1,
        type=int,
        help="Only run random selected subset of N tests.",
    )


def pytest_collection_modifyitems(session, config, items):
    random_sample_size = config.getoption("--random-selection")

    if random_sample_size >= 0:
        items[:] = random.sample(items, k=random_sample_size)
```

I created a file with 100 empty tests, and tested this new flag was working correctly:

```console
$ pytest --verbose --random-selection 5
===================== test session starts ======================
[…]
collected 100 items

test_truth.py::test_82 PASSED                            [ 20%]
test_truth.py::test_99 PASSED                            [ 40%]
test_truth.py::test_68 PASSED                            [ 60%]
test_truth.py::test_5 PASSED                             [ 80%]
test_truth.py::test_17 PASSED                            [100%]

====================== 5 passed in 0.01s =======================
```

By running it multiple times, I could see it selecting a different subset of 5 tests.

[nedbat]: https://hachyderm.io/@nedbat/111692835374984900
[pytest-random-order]: https://github.com/jbasko/pytest-random-order
[hoefling]: https://stackoverflow.com/a/56699824/1558022
