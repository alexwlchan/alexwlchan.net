"""
Build the site and serve it at http://localhost:5757, then rebuild
it whenever something changes.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import time
import threading

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site
from mosaic import caddy
from mosaic.site import BuildOptions
from watch_for_changed_files import watch_for_changed_files


rebuild_event = threading.Event()


class RebuildHandler(BaseHTTPRequestHandler):
    """
    An HTTP handler that sends one of two responses.

    Either:

    *   200 OK -- the site has changed, reload the page, or
    *   204 No Content -- nothing has changed recently, make a new GET request

    """

    def do_GET(self) -> None:
        """
        Handle a new GET request from a browser.
        """
        try:
            has_changes = rebuild_event.wait(timeout=20)

            if has_changes:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                self.wfile.write(b"reload\n")
            else:
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
        except BrokenPipeError:
            pass


def rebuild(site: Site, changeset: set[Path]) -> None:
    """
    Build a new version of the site.
    """
    has_changes = False
    has_src_changes = False

    root = Path(".").absolute()

    for p in changeset:
        if p == root / "topics.json":
            has_changes = True

        if p.is_relative_to(root / "src"):
            has_src_changes = True
            has_changes = True

        if p.is_relative_to(root / "css") or p.is_relative_to(root / "templates"):
            has_changes = True

    if not has_changes:
        return

    options = BuildOptions(
        copy_static_files=has_src_changes,
        cleanup_leftover_files=False,
        incremental_read=True,
        profile="--profile" in sys.argv,
        livereload=True,
    )

    try:
        print("🔨 Rebuilding site...")
        now = time.time()
        site.build_site(options)
        elapsed = time.time() - now
        print(f"✅ Build successful in {elapsed:.3f}s")

        # Trigger the reload event, so any waiting browsers will refresh
        rebuild_event.set()
        rebuild_event.clear()

    except Exception as e:
        print(f"❌ Build failed with error: {e}", file=sys.stderr)


if __name__ == "__main__":
    server_address = ("localhost", 5555)
    server = ThreadingHTTPServer(server_address, RebuildHandler)

    threading.Thread(target=server.serve_forever, daemon=True).start()

    with caddy.local_webserver(out_dir=Path("_out")) as base_url:
        print(f"🌐 Listening on {base_url}")

        site = Site()

        try:
            now = time.time()
            try:
                site.build_site(options=BuildOptions(profile=True, livereload=True))
            except Exception as e:
                print(f"❌ Initial build failed with error: {e}", file=sys.stderr)
                sys.exit(1)
            else:
                elapsed = time.time() - now
                print(f"✅ Initial build successful in {elapsed:.3f}s")

            for changeset in watch_for_changed_files():
                rebuild(site, changeset)

        except Exception as e:  # noqa: E722
            print(f"❌ Incremental build failed with error: {e}", file=sys.stderr)
            server.shutdown()
        except KeyboardInterrupt:
            print("^C detected, stopping...")
            server.shutdown()
        except SystemExit:
            server.shutdown()
