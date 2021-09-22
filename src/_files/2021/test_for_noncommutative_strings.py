from hypothesis import given
from hypothesis.strategies import text


@given(text())
def test_uppercase_and_reverse_are_commutable(s):
    print(repr(s))
    assert s.upper()[::-1] == s[::-1].upper()
