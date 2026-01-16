"""
Build a complete copy of the site.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site


if __name__ == "__main__":
    site = Site(css_path=Path("css/style.css"), out_dir=Path("_out"))
    site.build_site()
