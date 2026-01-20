"""
Compare my current DNS records to a checked-in TOML file.
"""

from pathlib import Path

import dns.resolver
import tomllib


DOMAINS_TO_CHECK = {
    # alexwlchan.net
    "alexwlchan.net": ["NS", "MX", "A", "TXT"],
    "_acme-challenge.analytics.alexwlchan.net": ["TXT"],
    "analytics.alexwlchan.net": ["A"],
    "books.alexwlchan.net": ["A"],
    "social.alexwlchan.net": ["CNAME"],
    "til.alexwlchan.net": ["A"],
    "www.alexwlchan.net": ["A"],
    "fm1._domainkey.alexwlchan.net": ["CNAME"],
    "fm2._domainkey.alexwlchan.net": ["CNAME"],
    "fm3._domainkey.alexwlchan.net": ["CNAME"],
    "_dmarc.alexwlchan.net": ["TXT"],
    "_atproto.alexwlchan.net": ["TXT"],
    #
    # alexwlchan.com
    "alexwlchan.com": ["NS", "A", "MX"],
    "*.alexwlchan.com": ["A"],
    "mail.alexwlchan.com": ["CNAME"],
    #
    # alexwlchan.co.uk
    "alexwlchan.co.uk": ["NS", "A", "MX"],
    "*.alexwlchan.co.uk": ["A"],
    "mail.alexwlchan.co.uk": ["CNAME"],
    #
    # finduntaggedtumblrposts.com
    "finduntaggedtumblrposts.com": ["NS", "A", "MX", "TXT"],
    "fm1._domainkey.finduntaggedtumblrposts.com": ["CNAME"],
    "fm2._domainkey.finduntaggedtumblrposts.com": ["CNAME"],
    "fm3._domainkey.finduntaggedtumblrposts.com": ["CNAME"],
    #
    # bijouopera.co.uk
    "bijouopera.co.uk": ["NS", "MX", "TXT"],
    "fm1._domainkey.bijouopera.co.uk": ["CNAME"],
    "fm2._domainkey.bijouopera.co.uk": ["CNAME"],
    "fm3._domainkey.bijouopera.co.uk": ["CNAME"],
}


def get_dns_records(domain: str, record_type: str) -> set[str]:
    """
    Look up the DNS records for a single domain.
    """
    answers = dns.resolver.resolve(domain, record_type)
    return {rdata.to_text() for rdata in answers}


def test_dns_records_match_expected() -> None:
    """
    My current DNS records match my checked-in snapshot.
    """
    actual = {
        f"{domain} {rt}": get_dns_records(domain, rt)
        for domain, record_types in DOMAINS_TO_CHECK.items()
        for rt in record_types
    }

    dns_dir = Path(__file__).parent
    with open(dns_dir / "dns_records.toml", "rb") as f:
        expected = {key: set(val) for key, val in tomllib.load(f).items()}

    assert actual == expected
