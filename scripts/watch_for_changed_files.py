"""
Watch a directory for changes.
"""

from collections.abc import Iterator
import os
from pathlib import Path
import selectors
import subprocess


def watch_for_changed_files(*dirs: str | Path) -> Iterator[set[Path]]:
    """
    Watch one or more directory trees for changes, and yield the paths of
    files when they change.
    """
    cmd = ["swift", "scripts/watch_for_changed_files.swift"] + [str(d) for d in dirs]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)

    assert proc.stdout is not None
    os.set_blocking(proc.stdout.fileno(), False)

    sel = selectors.DefaultSelector()
    sel.register(proc.stdout, selectors.EVENT_READ)

    try:
        while True:
            sel.select()

            captured_paths = set()

            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                captured_paths.add(Path(line.strip()))

            yield captured_paths
    finally:
        proc.terminate()
        proc.wait()
