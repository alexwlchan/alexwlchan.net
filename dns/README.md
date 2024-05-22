# dns

This folder contains a crude way to check my DNS records are configured correctly, and track changes.

The `verify_dns_records.py` script tries to create an exhaustive listing of my DNS records.
It compares this to a saved copy of my DNS records, so I can be alerted if anything becomes misconfigured.

This check is run once a day by GitHub Actions.

The saved copy of my DNS records is saved in `dns_records.toml`.
This file includes some comments to remind me what all my DNS records are for, which are useful for debugging and if I ever want to move my domains to another DNS provider.
