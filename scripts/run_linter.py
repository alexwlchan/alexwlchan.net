"""
Run linting on the rendered site.
"""

import collections
from pathlib import Path
import sys

from bs4 import BeautifulSoup
from lxml import etree
import termcolor
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from mosaic.fs import find_paths_under
from mosaic.linters import (
    check_all_urls_are_hackable,
    check_no_broken_html,
    check_no_localhost_links,
    check_redirects,
)


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

    all_errors: dict[str | Path, list[str]] = collections.defaultdict(list)

    html_paths = list(find_paths_under(out_dir, suffix=".html"))

    html_files = {
        p: (p.read_text(), read_single_html_file(p))
        for p in tqdm(html_paths, desc="parsing html")
    }

    for p, (html_str, soup) in tqdm(html_files.items(), desc="linting html"):
        try:
            if "testing-javascript-without-a-framework" not in p.parts:
                all_errors[p] += check_no_broken_html(html_str)
            all_errors[p] += check_no_localhost_links(soup)
        except Exception:
            print(p)
            raise

    redirects_path = Path("caddy/redirects.Caddyfile")
    all_errors[redirects_path] += check_redirects(redirects_path, out_dir)

    all_errors["*"] += check_all_urls_are_hackable(redirects_path, out_dir)

    # Check the RSS feeds parse as valid XML
    parser = etree.XMLParser(recover=False)

    with open(out_dir / "atom.xml", "rb") as in_file:
        try:
            etree.parse(in_file, parser=parser)
        except etree.XMLSyntaxError as err:
            all_errors["/til/atom.xml"].append(f"error parsing XML: {err}")

    with open(out_dir / "til/atom.xml", "rb") as in_file:
        try:
            etree.parse(in_file, parser=parser)
        except etree.XMLSyntaxError as err:
            all_errors["/til/atom.xml"].append(f"error parsing XML: {err}")

    # Remove paths which don't have any errors
    all_errors = {p: errors for p, errors in all_errors.items() if errors}

    if not all_errors:
        print(termcolor.colored("no errors found!", "green"))
    else:
        print("")
        print(termcolor.colored(f"found errors in {len(all_errors)} file(s):", "red"))

        for label, errors in all_errors.items():
            print("")
            print(f"{label}:")
            for e in errors:
                print(f"  - {e}")

        sys.exit(1)
