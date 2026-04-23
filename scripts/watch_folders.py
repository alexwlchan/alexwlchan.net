"""
Watch a directory for changes.
"""

from collections.abc import Iterator
from pathlib import Path
import subprocess


def watch_folders(root: str | Path = ".") -> Iterator[Path]:
    """
    Watch a folder for changes, and yield changed directories.
    """
    cmd = ["swift", "scripts/watch_folders.swift", str(root)]

    proc = subprocess.Popen(
        cmd, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True
    )

    try:
        # TODO: Implement de-bouncing or queueing.
        assert proc.stdout is not None
        for line in proc.stdout:
            yield Path(line.strip()).relative_to(Path(root).absolute())
    except KeyboardInterrupt:
        proc.terminate()
