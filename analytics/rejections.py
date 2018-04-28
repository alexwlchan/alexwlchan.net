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
    '/webdb/',
    '/websql/',
]


def should_be_rejected(log_line):
    if urlparse(log_line.url).path in BAD_PATHS:
        return True

    return False
