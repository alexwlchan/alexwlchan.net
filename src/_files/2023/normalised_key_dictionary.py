#!/usr/bin/env python3
"""
See https://alexwlchan.net/2023/dictionaries-and-userdict/
"""

import collections
import unittest


class NormalisedKeyDictionary(collections.UserDict):
    def __init__(self, data=None, *, normalise):
        data = data or {}
        self.normalise = normalise

        super().__init__({normalise(k): v for k, v in data.items()})

    def __getitem__(self, key):
        return super().__getitem__(self.normalise(key))

    def __setitem__(self, key, value):
        return super().__setitem__(self.normalise(key), value)

    def __delitem__(self, key):
        return super().__delitem__(self.normalise(key))


class TestNormalisedKeyDictionary(unittest.TestCase):
    def test_empty_methods(self):
        empty = NormalisedKeyDictionary(normalise=lambda key: key)
        assert len(empty) == 0
        assert repr(empty) == "{}"

    def test_can_get_and_set_by_normalised_or_not_normalised_keys(self):
        pairs = NormalisedKeyDictionary(normalise=lambda p: tuple(sorted(p)))

        # set using a normalised key
        pairs[("Alice", "Bryony")] = 1
        assert pairs[("Alice", "Bryony")] == 1
        assert pairs[("Bryony", "Alice")] == 1

        # set using a not-normalised key
        pairs[("Carol", "Alice")] = 2
        assert pairs[("Alice", "Carol")] == 2
        assert pairs[("Carol", "Alice")] == 2

        assert len(pairs) == 2

    def test_normalises_any_existing_values(self):
        shapes = NormalisedKeyDictionary(
            {"p": "pentagon", "S": "square", "t ": "triangle"},
            normalise=lambda k: k.strip().lower(),
        )

        assert shapes["t"] == "triangle"

        assert len(shapes) == 3
        assert set(shapes.items()) == {
            ("p", "pentagon"),
            ("s", "square"),
            ("t", "triangle"),
        }

    # This test breaks if you subclass from dict instead of UserDict
    def test_can_update_correctly(self):
        names = NormalisedKeyDictionary(normalise=lambda k: k.upper())

        names.update({'a': 'Alice', 'b': 'Bryony', 'c': 'Carol'})
        assert names.keys() == {'A', 'B', 'C'}

    def test_can_use_unusual_key_types(self):
        common_letters = NormalisedKeyDictionary(normalise=lambda k: tuple(k))

        common_letters[['one', 'two']] = 'o'
        common_letters[['two', 'three']] = 't'

        assert common_letters[['one', 'two']] == 'o'
