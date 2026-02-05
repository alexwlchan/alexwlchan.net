"""
Run linting on the rendered site.
"""

import collections
import json
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
    check_images_have_alt_text,
    check_links_are_consistent,
    check_no_broken_html,
    check_no_localhost_links,
    check_redirects,
)


def read_single_html_file(p: Path) -> BeautifulSoup:
    """
    Parse a single HTML file with beautifulsoup.
    """
    return BeautifulSoup(p.read_text(), "html.parser")


def check_http_410_gone(out_dir: Path) -> list[str]:
    """
    Look at the list of pages that return HTTP 410 Gone and make sure
    none of them exist.
    """
    errors = []

    with open("caddy/gone.json") as in_file:
        gone = json.load(in_file)

    for path in gone:
        if path.endswith("/"):
            expected_path = out_dir / path.lstrip("/") / "index.html"
        else:
            expected_path = out_dir / path.lstrip("/")

        if expected_path.exists():
            errors.append(f"returning HTTP 410 for page that exists: {path}")

    return errors


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

            if "files" not in p.parts:
                all_errors[p] += check_images_have_alt_text(soup)

            all_errors[p] += check_no_localhost_links(soup)
        except Exception:
            print(p)
            raise

    redirects_path = Path("caddy/redirects.Caddyfile")
    all_errors[redirects_path] += check_redirects(redirects_path, out_dir)

    book_redirects_path = Path("caddy/book_redirects.Caddyfile")
    all_errors[book_redirects_path] += check_redirects(book_redirects_path, out_dir)

    gone_path = Path("caddy/gone.Caddyfile")
    all_errors[gone_path] = check_http_410_gone(out_dir)

    all_errors["*"] += check_all_urls_are_hackable(redirects_path, out_dir)

    link_errors = check_links_are_consistent(
        out_dir, {pth: soup for pth, (_, soup) in html_files.items()}
    )
    for pth, errors in link_errors.items():
        all_errors[pth].extend(errors)

    # Check the RSS feeds parse as valid XML. We run the parser with
    # recovery disabled so it doesn't try to fix any broken XML it finds.
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
