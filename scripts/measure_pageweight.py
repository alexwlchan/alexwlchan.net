#!/usr/bin/env python3
"""
Print the size of the rendered HTML files.
"""

from pathlib import Path


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

    print("Homepage (/):\t\t\t", pprint_filesize(out_dir / "index.html"))
    print(
        "Articles (/articles/):\t\t", pprint_filesize(out_dir / "articles/index.html")
    )
    print("Notes (/notes/):\t\t", pprint_filesize(out_dir / "notes/index.html"))
    print(
        "Book reviews (/book-reviews/):\t",
        pprint_filesize(out_dir / "book-reviews/index.html"),
    )

    sizes = [
        p.stat().st_size for p in out_dir.rglob("*.html") if "files" not in p.parts
    ]
    average = round(sum(sizes) / len(sizes))
    print("Global average:\t\t\t", pprint_size(average))
