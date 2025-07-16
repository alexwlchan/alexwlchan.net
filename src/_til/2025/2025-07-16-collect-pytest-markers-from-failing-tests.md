---
layout: til
title: Collecting pytest markers from failing tests
summary: You can annotate tests with markers, and using the `pytest_collection_modifyitems` and `pytest_terminal_summary` hooks you can get a list of markers for tests that failed.
date: 2025-07-16 11:14:50 +0100
tags:
  - python
  - python:pytest
---
I'm using pytest to monitor some of my websites, and when the tests fail, I want to produce a human-friendly report that describes which pages are down.
Each test is checking a single website, and a single website may be checked by multiple tests.
For example, I might have a test that checks a website is up, that it has the right HTTP headers, and that its HTTPS cert isn't about to expire.

I wanted to annotate my tests [with custom markers][markers], so that I know which website is being checked by a particular test.
For example, I could mark a test that's checking my blog:

```python
@pytest.mark.blog
def test_my_blog_is_up():
    resp = httpx.get("https://alexwlchan.net/")
    assert resp.status_code == 200
```

When the tests fail, I want to gather the markers from the failing tests, and use them to build my human-friendly report.
I was able to do this with a couple of hooks that run at the end of the test.

[markers]: https://docs.pytest.org/en/stable/example/markers.html#mark-examples

## Example

Here's a simple test suite:

```python
import pytest


@pytest.mark.falsehoods
def test_A():
    assert 0 == 1


@pytest.mark.truthiness
def test_B():
    assert 1 == 1
```

If I run this test, pytest will warn me about unknown markers.
I can define the markers in my `pytest.ini` or `pyproject.toml` so pytest knows what they are:

```ini
[pytest]
markers =
    falsehoods: marks tests as describing falsehoods
    truthiness: marks tests as containing truthfulness
```

Then the important bit is in `conftest.py`, where I define two hooks:

```python
import pytest

test_marks = {}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """
    Record the marks defined on each test item.
    """
    for item in items:
        test_marks[item.nodeid] = [mark.name for mark in item.iter_markers()]


def pytest_terminal_summary(
    terminalreporter: pytest.TerminalReporter,
    exitstatus: pytest.ExitCode,
    config: pytest.Config,
) -> None:
    """
    Print a list of marks on each test that failed.
    """
    terminalreporter.write_sep("-", "Failing test marks")

    for report in terminalreporter.getreports("failed"):
        nodeid = report.nodeid
        marks = test_marks.get(nodeid, [])
        terminalreporter.write_line(f"{nodeid} -> Marks: {marks}")
```

When the test starts, I use the [`pytest_collection_modifyitems` hook][modifyitems] to build a dict mapping test IDs to their markers.
Although I have access to the markers later in `report.keywords`, they're a bit easier to get here -- the `keywords` list includes some stuff other than my markers.

When the tests are complete, I use the [`pytest_terminal_summary` hook][summary] to print some extra text in the terminal report.
In this example, I'm printing the name of each failing test and its markers:

```
my_test.py::test_A -> Marks: ['falsehoods']
```

You can obviously do more sophisticated stuff in this hook; this just shows you how to get the data.
For example, in my uptime tests, I'm gathering a list of all the markers on any failing test and using them in a message that gets posted to Slack.

[modifyitems]: https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_collection_modifyitems
[summary]: https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_terminal_summary
