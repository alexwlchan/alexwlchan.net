"""
File-system related utilities.
"""

from collections.abc import Iterator
from pathlib import Path


def find_paths_under(root: Path, *, suffix: str = "") -> Iterator[Path]:
    """
    Generates the absolute paths to every matching file under ``root``.
    """
    if root.exists() and not root.is_dir():
        raise ValueError(f"Cannot find files under non-directory: {root!r}")

    if not root.is_dir():
        raise FileNotFoundError(root)

    for dirpath, _, filenames in root.walk():
        for f in filenames:
            p = dirpath / f

            if p.is_file() and (suffix == "" or p.suffix.lower() == suffix.lower()):
                yield p
