"""
Run linting on the rendered site.
"""

import collections
from pathlib import Path
import sys

from bs4 import BeautifulSoup
import termcolor
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from mosaic.fs import find_paths_under
from mosaic.linters import check_no_broken_html, check_no_localhost_links


def read_single_html_file(p: Path) -> BeautifulSoup:
    """
    Parse a single HTML file with beautifulsoup.
    """
    return BeautifulSoup(p.read_text(), "html.parser")


if __name__ == "__main__":
    try:
        out_dir = Path(sys.argv[1])
    except IndexError:
        sys.exit(f"Usage: {__file__} OUT_DIR")

    all_errors = collections.defaultdict(list)

    html_paths = list(find_paths_under(out_dir, suffix=".html"))

    html_files = {
        p: (p.read_text(), read_single_html_file(p))
        for p in tqdm(html_paths, desc="parsing html")
    }

    for p, (html_str, soup) in tqdm(html_files.items(), desc="linting html"):
        try:
            if "testing-javascript-without-a-framework" not in p.parts:
                for err in check_no_broken_html(html_str):
                    all_errors[p].append(err)
            for err in check_no_localhost_links(soup):
                all_errors[p].append(err)
        except Exception:
            print(p)
            raise

    if not all_errors:
        print(termcolor.colored("no errors found!", "green"))
    else:
        print("")
        print(termcolor.colored(f"found errors in {len(all_errors)} file(s):", "red"))

        for p, errors in all_errors.items():
            print("")
            print(f"{p}:")
            for err in errors:
                print(f"  - {err}")

        sys.exit(1)
