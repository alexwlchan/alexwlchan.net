# -*- encoding: utf-8
"""
I get a bunch of requests that are uninteresting for some reason -- maybe
somebody trying to find a PHP admin page, or crawling for vulnerable WordPress
instances.  Any such request can immediately be rejected as uninteresting
for my analytics.
"""

from urllib.parse import urlparse


BAD_PATHS = [
    '/admin/',
    '/dbadmin/',
    '/myadmin/',
    '/mysqladmin/',
    '/mysql-admin/',
    '/mysqlmanager/',
    '/sqlmanager/',
    '/sqlweb/',
    '/webadmin/',
    '/webdb/',
    '/websql/',
]

BAD_EXTENSIONS = [
    '.php',
]


def should_be_rejected(log_line):
    parts = urlparse(log_line.url)

    if parts.path in BAD_PATHS:
        return True

    if parts.path.endswith(tuple(BAD_EXTENSIONS)):
        return True

    return False
