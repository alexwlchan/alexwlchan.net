"""
Check my HTTPS certificates are valid and not close to expiry.
"""

from contextlib import closing
from datetime import datetime
import socket
import ssl

import certifi
import pytest


def https_expiry_date(hostname: str) -> datetime:
    """
    Get the expiry date of the HTTPS certificate for a domain.
    """
    ctx = ssl.create_default_context(cafile=certifi.where())

    with closing(socket.socket(socket.AF_INET)) as sock:
        with closing(ctx.wrap_socket(sock, server_hostname=hostname)) as conn:
            conn.settimeout(5.0)
            conn.connect((hostname, 443))
            ssl_info = conn.getpeercert()
            assert ssl_info is not None

            # Example date: "Oct 17 12:32:16 2024 GMT"
            expiry_date_str = ssl_info["notAfter"]
            assert isinstance(expiry_date_str, str)
            expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")

    return expiry_date


@pytest.mark.parametrize(
    "hostname",
    [
        "alexwlchan.net",
        "books.alexwlchan.net",
        "analytics.alexwlchan.net",
        "www.alexwlchan.net",
        "alexwlchan.com",
        "www.alexwlchan.com",
        "alexwlchan.co.uk",
        "www.alexwlchan.co.uk",
    ],
)
def test_domain_is_not_close_to_expiry(hostname: str) -> None:
    """
    My domains are more than 2 weeks to expiry.
    """
    delta = https_expiry_date(hostname) - datetime.now()
    assert delta.days > 14
