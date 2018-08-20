# -*- encoding: utf-8
"""
I get a bunch of requests that are uninteresting for some reason -- maybe
somebody trying to find a PHP admin page, or crawling for vulnerable WordPress
instances.  Any such request can immediately be rejected as uninteresting
for my analytics.
"""

from urllib.parse import urlparse

import toml


config = toml.loads(open('rejections.toml').read())


def should_be_rejected(log_line):
    parts = urlparse(log_line.url.lower())

    if parts.path in config['bad_paths']:
        return True

    if parts.path.startswith(tuple(config['bad_path_prefixes'])):
        return True

    if parts.path.endswith(tuple([s.lower() for s in config['bad_path_suffixes']])):
        return True

    if any(u in log_line.user_agent for u in config['bad_user_agents']):
        return True

    if log_line.referrer in config['bad_referrers']:
        return True

    if (
        log_line.referrer is not None and
        any(r in log_line.referrer.lower() for r in config['bad_referrer_components'])
    ):
        return True

    return False
