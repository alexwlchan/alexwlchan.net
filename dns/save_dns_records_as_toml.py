#!/usr/bin/env python3
"""
Create a TOML file with a snapshot of my DNS records.

The TOML file will be a list of key-value pairs, where the key is
the domain name and record type, and the value is a list of records.

The script will print the name of the newly-created TOML file, which
will include the date the DNS records were retrieved.

== Example output ==

Here is some example TOML output:

    "alexwlchan.net NS" = [ "ns1.hover.com.", "ns2.hover.com.", ]
    "alexwlchan.net MX" = [ "10 in1-smtp.messagingengine.com.", ]

This represents three records for the domain ``alexwlchan.net``:

*   Two NS record with the values ``ns1.hover.com.`` and ``ns2.hover.com.``
*   One MX record with the value ``in1-smtp.messagingengine.com.`` and priority ``10``

"""

import datetime

import dns.resolver
import toml


# A list of all the domains I want to check, and the record types
# for each.  There's no good way to populate this automatically because
# you need to know about subdomains and the like -- I just create it
# based on what I see in my Hover dashboard.
DOMAIN_MAPPING = [
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
]


def get_dns_records():
    for domain, all_rdtypes in DOMAIN_MAPPING:
        for rdtype in all_rdtypes:
            yield (domain, rdtype, [str(s) for s in dns.resolver.resolve(domain, rdtype)])


if __name__ == "__main__":
    dns_records = {
        f"{domain} {rdtype}": records
        for domain, rdtype, records in get_dns_records()
    }

    from pprint import pprint; pprint(dns_records)

    now = datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
    out_path = f"dns_records.{now}.toml"

    with open(out_path, "x") as out_file:
        out_file.write(toml.dumps(dns_records))

    print(out_path, end="")
