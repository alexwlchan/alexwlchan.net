#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: add_referrer_alias.py <ORIGINAL> <ALIAS>
"""

import docopt
import toml


args = docopt.docopt(__doc__)

original = args["<ORIGINAL>"]
alias = args["<ALIAS>"]

referrers = toml.load(open("referrers.toml"))

if original.startswith("https://t.co/"):
    referrers["twitter"][original] = alias
else:
    referrers["aliases"][original] = alias

toml.dump(referrers, open("referrers.toml", "w"))
