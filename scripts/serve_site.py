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
from watch_folders import watch_folders


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


def rebuild(site: Site, changed_folder: Path) -> None:
    """
    Build a new version of the site.
    """
    has_changes = False

    if any(changed_folder.is_relative_to(p) for p in ("css", "src", "templates")):
        has_changes = True

    if (
        changed_folder == Path(".")
        and Path("topics.json").stat().st_mtime > time.time() - 60
    ):
        has_changes = True

    if not has_changes:
        return

    print(f"detected changes in {changed_folder}")

    options = BuildOptions(
        copy_static_files=changed_folder.is_relative_to("src"),
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
        print(f"✅ Build successful in {elapsed:.2f}s")

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
            site.build_site(options=BuildOptions(profile=True, livereload=True))
            elapsed = time.time() - now
            print(f"✅ Initial build successful in {elapsed:.2f}s")

            for changed_folder in watch_folders():
                rebuild(site, changed_folder)
        except KeyboardInterrupt:
            reload_server.shutdown()
