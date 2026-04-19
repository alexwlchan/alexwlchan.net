"""
Build the site and serve it at http://localhost:5757, then rebuild
it whenever something changes.
"""

from collections.abc import Callable
from pathlib import Path
import sys
import time
from typing import Literal

from livereload import Server

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site
from mosaic.site import BuildOptions


SITE = Site()


def build_and_reload(
    reason: Literal["css", "src", "templates", "topics"],
) -> Callable[[], None]:
    """
    Build a new version of the site.
    """
    options = BuildOptions(
        copy_static_files=reason == "src",
        cleanup_leftover_files=False,
        incremental_read=True,
    )

    def build() -> None:
        try:
            print("🔨 Rebuilding site...")
            now = time.time()
            SITE.build_site(options)
            elapsed = time.time() - now
            print(f"✅ Build successful in {elapsed:.2f}s")
        except Exception as e:
            print(f"❌ Build failed with error: {e}", file=sys.stderr)

    return build


if __name__ == "__main__":
    now = time.time()
    SITE.build_site()
    elapsed = time.time() - now
    print(f"✅ Initial build successful in {elapsed:.2f}s")

    server = Server()

    server.watch("css/", build_and_reload("css"))
    server.watch("src/", build_and_reload("src"))
    server.watch("templates/", build_and_reload("templates"))
    server.watch("topics.json", build_and_reload("topics"))

    server.serve(root=SITE.out_dir, port=5757, restart_delay=0)
