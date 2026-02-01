"""
Build the site and serve it at http://localhost:5757, then rebuild
it whenever something changes.
"""

from pathlib import Path
import sys

from livereload import Server

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site


SITE = Site()


def build_and_reload() -> None:
    """
    Build a new version of the site.
    """
    try:
        print("🔨 Rebuilding site...")
        SITE.build_site(incremental=True, enable_analytics=False)
        print("✅ Build successful.")
    except Exception as e:
        print(f"❌ Build failed with error: {e}")


if __name__ == "__main__":
    SITE.build_site(enable_analytics=False)

    server = Server()

    server.watch("css/", build_and_reload)
    server.watch("mosaic/", build_and_reload)
    server.watch("src/", build_and_reload)
    server.watch("templates/", build_and_reload)

    server.serve(root=SITE.out_dir, port=5757, restart_delay=0)
