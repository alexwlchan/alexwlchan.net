"""
Build the site and serve it at http://localhost:5757, then rebuild
it whenever something changes.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
import sys
import time
import threading

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site
from mosaic import caddy
from mosaic.site import BuildOptions
from watch_for_changed_files import watch_for_changed_files


# All waiting pages are told to reload when this event is set to true
reload_event = threading.Event()


class WaitForReloadHandler(SimpleHTTPRequestHandler):
    """
    A basic server that only serves the `/wait-for-reload` endpoint.

    The page can long poll this endpoint for either:

    - a 200 OK with 'reload' (refresh to pick up changes), or
    - a 204 No Content (no changes in the last 30 seconds).
    """

    def do_GET(self) -> None:
        """
        Handle GET requests.
        """
        if self.path != "/wait-for-reload":
            self.send_response(404)
            self.end_headers()
            return

        # We've received a request from a web browser.
        #
        # Wait until reload_event is set, or 30 seconds have passed.
        # The choice of 30 seconds is arbitrary; we just don't want the
        # browser to time out the connection if nothing changes.
        changed = reload_event.wait(timeout=30)

        if changed:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            try:
                self.wfile.write(b"reload")
            except BrokenPipeError:
                pass
        else:
            self.send_response(204)
            self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    An HTTP server where each "hanging" fetch request runs in its own thread.
    """

    daemon_threads = True


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
        reload_event.set()
        reload_event.clear()

    except Exception as e:
        print(f"❌ Build failed with error: {e}", file=sys.stderr)


if __name__ == "__main__":
    reload_server = ThreadedHTTPServer(("localhost", 5656), WaitForReloadHandler)
    threading.Thread(target=reload_server.serve_forever, daemon=True).start()

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
            reload_server.shutdown()
        except KeyboardInterrupt:
            print("^C detected, stopping...")
            reload_server.shutdown()
        except SystemExit:
            reload_server.shutdown()
