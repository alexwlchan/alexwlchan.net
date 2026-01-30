#!/usr/bin/env python3
"""
Print the size of the rendered HTML files.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from mosaic.fs import find_paths_under


def pprint_filesize(path: Path) -> str:
    """
    Print the size of a file in KiB and bytes.
    """
    return pprint_size(path.stat().st_size)


def pprint_size(size: int) -> str:
    """
    Pretty-print a size in bytes.
    """
    return f"{size / 1024:6.1f} KiB ({size:7,} B)"


if __name__ == "__main__":
    out_dir = Path("_out")

    # fmt: off
    print("Homepage (/):\t\t",        pprint_filesize(out_dir / "index.html"))
    print("Articles (/articles/):\t", pprint_filesize(out_dir / "articles/index.html"))
    print("TIL (/til):\t\t",          pprint_filesize(out_dir / "til/index.html"))
    # fmt: on

    sizes = [
        p.stat().st_size
        for p in find_paths_under(out_dir, suffix=".html")
        if "files" not in p.parts
    ]
    average = round(sum(sizes) / len(sizes))
    print("Global average:\t\t", pprint_size(average))
