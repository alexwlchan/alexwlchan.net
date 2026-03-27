---
layout: note
date: 2026-03-27 14:59:26 +00:00
title: Useful type hints for Python
summary: A collection of non-obvious type hints that I couldn't easily find in documentation or Google searches.
topic: Python
---
I type check most of my Python code with `mypy --strict`.
This note describes some of the non-obvious type hints that I couldn't easily find in documentation or Google searches.

## pytest parameterised tests

```python {"names":{"1":"pytest","2":"_pytest","3":"mark","4":"structures","5":"ParameterSet","6":"params"}}
import pytest
from _pytest.mark.structures import ParameterSet

params: list[ParameterSet] = [
    pytest.param("1", id="one"),
    pytest.param("2", id="two"),
    pytest.param("3", id="three"),
]
```