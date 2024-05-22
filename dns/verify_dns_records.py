"""
This script tries to produce a JSON file that lists all my DNS records.

There's no easy way to list all the DNS records for a domain, and its
subdomains, so I have to hard-code the list of what to look for.
Fortunately I don't add subdomains that often, so this is close to
exhaustive.

I produced the initial list by looking through DNS records in my
Hover dashboard.
"""

import collections
import datetime
import itertools
import sys

import dns.resolver
import toml


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
        ("_dmarc.alexwlchan.net", ["TXT"]),
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

    live_records = collections.defaultdict(list)

    for domain, rdtype, server in get_dns_records():
        live_records[f"{domain} {rdtype}"].append(str(server))

    with open(f"dns_records.{now}.toml", "x") as out_file:
        out_file.write(toml.dumps(live_records))

    with open("dns_records.toml") as in_file:
        saved_records = toml.load(in_file)

    if saved_records == live_records:
        print("Saved DNS records are up-to-date :D")
        sys.exit(0)
    else:
        print("Saved DNS records don't match what's configured D:", file=sys.stderr)

        for k in sorted(set(itertools.chain(saved_records, live_records))):
            if saved_records.get(k) != live_records.get(k):
                print("")
                print(f"-- {k}:")
                print(f"        saved: {saved_records.get(k)}")
                print(f"        live:  {live_records.get(k)}")

        sys.exit(1)
