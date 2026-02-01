"""
Build a complete copy of the site.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site


if __name__ == "__main__":
    site = Site()
    result = site.build_site(incremental="--incremental" in sys.argv[1:])
    if result:
        print("success!")
    else:
        print("error!", file=sys.stderr)
