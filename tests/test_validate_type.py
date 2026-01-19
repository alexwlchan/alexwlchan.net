"""
Tests for ``javascript_data_files.validate_type``.
"""

from typing import Any, Literal, TypedDict

import pytest
from pydantic import ValidationError

from mosaic.validate_type import validate_type


Shape = TypedDict("Shape", {"colour": str, "sides": int})
Circle = TypedDict("Circle", {"colour": str, "radius": int})


@pytest.mark.parametrize(
    "data",
    [
        {"colour": "red"},
        {"sides": 4},
        {"colour": "red", "sides": "four"},
        {"colour": (255, 0, 0), "sides": 4},
        {"colour": "red", "sides": 4, "angle": 36},
    ],
)
def test_validate_type_flags_incorrect_data(data: Any) -> None:
    """
    If you pass data that doesn't match the model to ``validate_type``,
    it throws a ``ValidationError``.
    """
    with pytest.raises(ValidationError):
        validate_type(data, model=Shape)


def test_validate_type_allows_valid_data() -> None:
    """
    If you pass data which matches the model to ``validate_type``,
    it passes without exception.
    """
    validate_type({"colour": "red", "sides": 4}, model=Shape)


def test_validate_type_supports_builtin_list() -> None:
    """
    You can validate a list with ``validate_type``.
    """
    validate_type([1, 2, 3], model=list[int])


def test_validate_type_supports_builtin_type() -> None:
    """
    You can validate a list with ``validate_type``.
    """
    validate_type(1, model=int)


@pytest.mark.parametrize(
    "data", [{"colour": "red", "sides": 4}, {"colour": "blue", "radius": 3}]
)
def test_validate_type_supports_union_type(data: Any) -> None:
    """
    You can validate a type which is a union of two TypedDict's.
    """
    validate_type(data, model=Shape | Circle)  # type: ignore


@pytest.mark.parametrize(
    "data",
    [
        {"colour": "red", "sides": 4, "name": "square"},
        {"colour": "red", "sides": 4, "stroke": "black", "depth": 3},
    ],
)
def test_validate_type_rejects_extra_fields(data: Any) -> None:
    """
    Adding extra keys to a TypedDict is a validation error.
    """
    with pytest.raises(ValidationError):
        validate_type(data, model=Shape)


@pytest.mark.parametrize(
    "data",
    [
        {"colour": "red", "sides": 4, "name": "square"},
        {"colour": "red", "sides": 4, "stroke": "black", "depth": 3},
    ],
)
def test_validate_type_of_union_rejects_extra_fields(data: Any) -> None:
    """
    Adding extra keys to a Union of TypedDict's is a validation error.
    """
    with pytest.raises(ValidationError):
        validate_type(data, model=Shape | Circle)  # type: ignore


def test_validate_type_does_not_change_data() -> None:
    """
    Check that ``validate_type`` does not change the value, merely make
    assertions about the type.

    This is a regression test for a bug I encountered in my bookmarks
    project -- notice that `s` does not really conform to either type.

    *   If it's UncolouredShape, it shouldn't have a "type"
    *   If it's ColouredShape, it should have a "colour"

    This appears to be caused by a bug in Pydantic, see
    https://github.com/pydantic/pydantic/issues/11328

    """

    class UncolouredShape(TypedDict):
        sides: int

    class ColouredShape(TypedDict):
        sides: str
        colour: str
        type: Literal["coloured_shape"]

    Shape = UncolouredShape | ColouredShape

    s = {
        "sides": 5,
        "type": "coloured_shape",
    }

    with pytest.raises(ValidationError):
        assert validate_type(s, model=Shape) == s  # type: ignore
