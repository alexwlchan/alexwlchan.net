#!/usr/bin/env python3
"""
Compare two TOML files created by ``save_dns_records_as_toml.py``.
"""

import itertools
import sys

import toml


if __name__ == "__main__":
    try:
        saved_path = sys.argv[1]
        live_path = sys.argv[2]
    except IndexError:
        sys.exit(f"Usage: {__file__} SAVED_PATH LIVE_PATH")

    with open(saved_path) as in_file:
        saved_records = {k: set(v) for k, v in toml.load(in_file).items()}

    with open(live_path) as in_file:
        live_records = {k: set(v) for k, v in toml.load(in_file).items()}

    if saved_records == live_records:
        print("The DNS records match :D")
        sys.exit(0)
    else:
        print("The DNS records don't match D:", file=sys.stderr)

        for k in sorted(set(itertools.chain(saved_records, live_records))):
            if saved_records.get(k) != live_records.get(k):
                print("")
                print(f"-- {k}:")
                print(f"        saved: {saved_records.get(k)}")
                print(f"        life:  {live_records.get(k)}")

        sys.exit(1)
