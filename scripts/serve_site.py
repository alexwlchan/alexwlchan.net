"""
Build the site and serve it at http://localhost:5757, then rebuild
it whenever something changes.
"""

from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
import sys
import threading
import time
from typing import Any

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site


PORT = 5757
SOURCE_DIRS = ["src", "css", "templates"]
OUT_DIR = Path("_out")


class RebuildHandler(FileSystemEventHandler):
    """
    Triggers a rebuild when files change.
    """

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Build the site whenever there's a watchdog event.
        """
        # TODO: Can I detect a change to Mosaic here?
        site = Site(
            css_path=Path("css/style.css"), src_dir=Path("src"), out_dir=OUT_DIR
        )
        result = site.build_site(incremental=True)
        if result:
            print(f"[{time.strftime('%H:%M:%S')}] Build success!")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Build error!", file=sys.stderr)


def serve_site() -> None:
    """
    Serves the _out directory on localhost:5757.
    """

    class RootedHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=OUT_DIR, **kwargs)

    server = HTTPServer(("localhost", PORT), RootedHandler)
    print(f"Serving at http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    # Start server in background
    server_thread = threading.Thread(target=serve_site, daemon=True)
    server_thread.start()

    # Start watching source directories
    event_handler = RebuildHandler()
    observer = Observer()

    for folder in SOURCE_DIRS:
        path = Path(folder)
        if path.exists():
            observer.schedule(event_handler, str(path), recursive=True)
            print(f"Watching {folder} for changes...")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        observer.stop()
    observer.join()
