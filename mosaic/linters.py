"""
Linter rules for verifying the final website output.
"""

from bs4 import BeautifulSoup
import hyperlink


def check_no_localhost_links(html: BeautifulSoup) -> list[str]:
    """
    Check an HTML file doesn't have any links to localhost URLs.
    """
    errors = []

    for anchor in html.find_all("a"):
        try:
            url = anchor.attrs["href"]
        except KeyError:
            continue
        assert isinstance(url, str)

        u = hyperlink.parse(url)
        if u.host == "localhost" and u.port == 5757:
            errors.append(f"linking to localhost URL: {url}")

    return errors
