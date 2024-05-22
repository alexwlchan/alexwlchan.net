"""
This script tries to produce a JSON file that lists all my DNS records.

There's no easy way to list all the DNS records for a domain, and its
subdomains, so I have to hard-code the list of what to look for.
Fortunately I don't add subdomains that often, so this is close to
exhaustive.

I produced the initial list by looking through DNS records in my
Hover dashboard.
"""

import datetime
import filecmp
import json
import sys

import dns.resolver


def get_dns_records():
    for domain, all_rdtypes in [
        #
        # alexwlchan.net
        ("alexwlchan.net", ["NS", "MX", "A", "TXT"]),
        # ("_acme-.alexwlchan.net", ["TXT"]),
        ("analytics.alexwlchan.net", ["A"]),
        ("books.alexwlchan.net", ["CNAME"]),
        ("social.alexwlchan.net", ["CNAME"]),
        ("til.alexwlchan.net", ["CNAME"]),
        ("www.alexwlchan.net", ["CNAME"]),
        ("fm1._domainkey.alexwlchan.net", ["CNAME"]),
        ("fm2._domainkey.alexwlchan.net", ["CNAME"]),
        ("fm3._domainkey.alexwlchan.net", ["CNAME"]),
        #
        # alexwlchan.com
        ("alexwlchan.com", ["NS", "A", "MX"]),
        ("*.alexwlchan.com", ["A"]),
        ("mail.alexwlchan.com", ["CNAME"]),
        #
        # alexwlchan.co.uk
        ("alexwlchan.co.uk", ["NS", "A", "MX"]),
        ("*.alexwlchan.co.uk", ["A"]),
        ("mail.alexwlchan.co.uk", ["CNAME"]),
        #
        # finduntaggedtumblrposts.com
        ("finduntaggedtumblrposts.com", ["NS", "A", "MX", "TXT"]),
        ("fm1._domainkey.finduntaggedtumblrposts.com", ["CNAME"]),
        ("fm2._domainkey.finduntaggedtumblrposts.com", ["CNAME"]),
        ("fm3._domainkey.finduntaggedtumblrposts.com", ["CNAME"]),
        #
        # bijouopera.co.uk
        ("bijouopera.co.uk", ["NS", "MX", "A", "TXT"]),
        ("fm1._domainkey.bijouopera.co.uk", ["CNAME"]),
        ("fm2._domainkey.bijouopera.co.uk", ["CNAME"]),
        ("fm3._domainkey.bijouopera.co.uk", ["CNAME"]),
    ]:
        for rdtype in all_rdtypes:
            answers = dns.resolver.resolve(domain, rdtype)
            for server in sorted(answers, key=lambda a: repr(a)):
                yield (domain, rdtype, server)


if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")

    with open(f"dns_records.{now}.json", "x") as out_file:
        for domain, rdtype, server in get_dns_records():
            line = {
                "domain": domain,
                "rdtype": rdtype,
                "server_r": repr(server),
                "server_s": str(server),
            }

            out_file.write(json.dumps(line) + "\n")

    if filecmp.cmp(f"dns_records.{now}.json", "dns_records.json", shallow=False):
        print("Saved DNS records are up-to-date :D")
        sys.exit(0)
    else:
        print("Saved DNS records don't match what's configured D:", file=sys.stderr)
        sys.exit(1)
