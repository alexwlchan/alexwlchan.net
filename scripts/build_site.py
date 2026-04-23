"""
Build a complete copy of the site.
"""

from pathlib import Path
import sys
import time

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site
from mosaic.site import BuildOptions


if __name__ == "__main__":
    site = Site()
    now = time.time()
    result = site.build_site(BuildOptions(livereload=True, profile=True))
    elapsed = time.time() - now
    if result:
        print(f"✅ Build successful in {elapsed:.1f}s.")
    else:
        print("❌ Build failed!", file=sys.stderr)
