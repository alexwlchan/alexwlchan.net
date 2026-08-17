"""
Functions for working with Git IDs.
"""

import codecs

import pygit2


def as_hex(oid: pygit2.Oid) -> str:
    """
    Convert a Git object ID to a human-readable hex string.
    """
    return codecs.encode(oid.raw, "hex").decode("ascii")
