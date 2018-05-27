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
    '/mysql/',
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

    '/hnap1/',

    '/hudson/script',
    '/script',

    '/https:/alexwlchan.net/',

    '/.git/HEAD',

    '/themes/default/js/showdown.js',

    '/filezilla.xml',
    '/sitemanager.xml',
    '/winscp.ini',
    '/ws_ftp.ini',

    '/simpla/',
    '/umbraco',

    '/admin/content/sitetree/',
    '/manager/',

    '/core/themes/bartik/color/preview.html',

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

    '/wp-admin',
    '/wp-content',

    '/.git',
]

BAD_PATH_SUFFIXES = [
    '/uploadify/uploadify.css',
    '/fix-ie.css',

    '/phpmyadmin/',
    '/phpmyadmin',

    '/cookies.js',

    '/joomla.xml',

    '/backgroundStripe-new.jpg',
    '/footerBackground.jpg',
    '/spacer.png',

    '/ArticleBookmark@2x.png',

    '/null',

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

BAD_REFERRERS = [
    'https://yellowstonevisitortours.com',
    'https://www.cloudsendchef.com',
    'https://www.timer4web.com/',
    'https://www.theautoprofit.ml',
]

BAD_REFERRER_COMPONENTS = [
    'blog1989.com',
    'incomekey.net',
    'yandex.ru',
]


def should_be_rejected(log_line):
    parts = urlparse(log_line.url.lower())

    if parts.path in BAD_PATHS:
        return True

    if parts.path.startswith(tuple(BAD_PATH_PREFIXES)):
        return True

    if parts.path.endswith(tuple([s.lower() for s in BAD_PATH_SUFFIXES])):
        return True

    if any(u in log_line.user_agent for u in BAD_USER_AGENTS):
        return True

    if log_line.referrer in BAD_REFERRERS:
        return True

    if (
        log_line.referrer is not None and
        any(r in log_line.referrer.lower() for r in BAD_REFERRER_COMPONENTS)
    ):
        return True

    return False
