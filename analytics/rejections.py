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

    '/p/m/a/',
    '/pma/',
    '/pma2005/',
    '/phpmyadmin/',
    '/phpmyadmin2/',
    '/php-my-admin/',
    '/php-myadmin/',
    '/phpmy-admin/',

    # These paths don't resolve, nor is there any sensible reason to
    # expect they might resolving soon.
    '/2/favicon.ico',
    '/3/favicon.ico',
    '/home/favicon.ico',
    '/.ftpconfig',
    '/.remote-sync.json',
    '/.vscode/ftp-sync.json',
    '/deployment-config.json',
    '/sftp-config.json',
]

BAD_PATH_PREFIXES = [
    '/phpmyadmin-',
]

BAD_PATH_SUFFIXES = [
    '/uploadify/uploadify.css',

    '/phpmyadmin/',
    '/phpmyadmin',

    # File formats I don't have anywhere on the site, because I don't
    # use these technologies!
    '.asp',
    '.aspx',
    '.php',
]

# Anything on this list was polluting 404 reports with URLs that
# wouldn't be expected to work -- but it's not a human, so I don't
# care that it got an error.
BAD_USER_AGENTS = [
    'http://ahrefs.com/robot/',
    'http://megaindex.com/crawler',
    'http://mj12bot.com/',
    'http://napoveda.seznam.cz/en/seznambot-intro/',
    'http://www.baidu.com/search/spider.html',
    'http://www.similartech.com/smtbot',
    'DatabaseDriverMysqli',
    'Googlebot',
    'Newsify Feed Fetcher',
    'OpenLinkProfiler.org/bot',
    'python-requests',
]


def should_be_rejected(log_line):
    parts = urlparse(log_line.url.lower())

    if parts.path in BAD_PATHS:
        return True

    if parts.path.startswith(tuple(BAD_PATH_PREFIXES)):
        return True

    if parts.path.endswith(tuple(BAD_PATH_SUFFIXES)):
        return True

    if any(u in log_line.user_agent for u in BAD_USER_AGENTS):
        return True

    return False
