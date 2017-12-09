#!/usr/bin/env python
# -*- encoding: utf-8
"""
Print a summary of analytics from my website.

Usage: reports.py [options]

Options:
  --days=<COUNT>            Number of days of records to analyse.
  --container=<CONTAINER>   Name of the running container.
  --limit=<LIMIT>           Max number of records to show.

"""

import collections
import datetime as dt
import re
import subprocess
from urllib.parse import parse_qs, urlparse

import attr
import docopt


NGINX_LOG_REGEX = re.compile(
    r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - '
    r'\[(?P<datetime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] '
    r'"(?P<method>GET|POST) (?P<url>.+) HTTP/1\.[01]" '
    r'(?P<status>\d{3}) '
    r'(?P<bytes_sent>\d+) '
    r'"(?P<referrer>(\-)|([^"]+))" '
    r'"(?P<user_agent>[^"]+)" '
    r'"(?P<forwarded_host>[^"]+)"', flags=re.IGNORECASE)


@attr.s
class LogLine:
    forwarded_host = attr.ib()
    datetime = attr.ib(
        convert=lambda x: dt.datetime.strptime(x, '%d/%b/%Y:%H:%M:%S %z')
    )
    method = attr.ib()
    url = attr.ib()
    status = attr.ib(convert=int)
    bytes_sent = attr.ib(convert=int)
    referrer = attr.ib(convert=lambda x: x if x != '-' else None)
    user_agent = attr.ib()
    
    @property
    def host(self):
        return self.forwarded_host.split()[0]

    @property
    def title(self):
        return parse_qs(urlparse(self.url).query)['t'][0]

    @property
    def date(self):
        return self.datetime.date()

    @property
    def display_referrer(self):
        try:
            return parse_qs(urlparse(self.url).query)['ref'][0]
        except KeyError:
            return ''


def page_views(log_lines):
    return len(log_lines)


def unique_ips(log_lines):
    return len(set(l.host for l in log_lines))


def top_pages(log_lines, limit):
    counter = collections.Counter(l.title for l in log_lines)
    return counter.most_common(limit)


def traffic_by_date(log_lines):
    counter = collections.Counter(l.date for l in log_lines)
    return sorted(counter.items())


def _normalise_referrer(referrer):
    parts = urlparse(referrer)

    # All international flavours of Google get collapsed into a single
    # set of results, split out only if a query string is visible.
    if parts.netloc.startswith(('www.google.', 'encrypted.google.')):
        qs = parse_qs(parts.query)
        try:
            return f'Google ({qs["q"][0]})'
        except KeyError:
            return 'Google'

    if parts.netloc.endswith('bing.com'):
        qs = parse_qs(parts.query)
        try:
            return f'Bing ({qs["q"][0]})'
        except KeyError:
            return 'Bing'

    if parts.netloc == 'duckduckgo.com':
        qs = parse_qs(parts.query)
        try:
            return f'DuckDuckGo ({qs["q"][0]})'
        except KeyError:
            return 'DuckDuckGo'

    # If the referrer was somewhere else on the site, it's not interesting.
    if parts.netloc == 'alexwlchan.net':
        return None

    # t.co URLs are unhelpful because they don't tell you which tweet
    # something came from; unpick them.  Note that some have ?amp=1 on the
    # end, which is extra annoying.
    tco_urls = {
        'https://t.co/6R9gyKJfqu': 'https://twitter.com/alexwlchan/status/928389714998104065',
        'https://t.co/qOIaNK1Rmd': 'https://twitter.com/alexwlchan',
        'https://t.co/EY119V2Ga8': 'https://twitter.com/alexwlchan/status/928748092039487490',
        'https://t.co/L5qP7Gsavd': 'https://twitter.com/alexwlchan/status/932634229309100034',
        'https://t.co/E0hBiiizkD': 'https://twitter.com/alexwlchan/status/933416262675451904',
        'https://t.co/Cp9qdEULDR': 'https://twitter.com/alexwlchan/status/935277634568818688',
    }

    if parts.netloc == 't.co':
        for u, v in tco_urls.items():
            if referrer.startswith(u):
                return v

    if 'facebook.com' in parts.netloc:
        return 'https://www.facebook.com/'

    if parts.netloc == 'yandex.ru':
        return 'http://yandex.ru/'

    if parts.netloc == 'r.search.yahoo.com':
        return 'https://search.yahoo.com/'

    aliases = {
        'https://uk.search.yahoo.com/': 'https://search.yahoo.com/',
        'http://t.umblr.com/': 'https://tumblr.com/',
        'https://t.umblr.com/': 'https://tumblr.com/',
    }

    return aliases.get(referrer, referrer)


def get_referrers(log_lines, limit):
    c = collections.Counter(
        _normalise_referrer(l.display_referrer) or None for l in log_lines)
    del c[None]
    return c.most_common(limit)
#
#
# def get_paths(query, limit):
#     inner = (query
#              .select(PageView.ip, PageView.url)
#              .order_by(PageView.timestamp))
#     paths = (PageView
#              .select(
#                  PageView.ip,
#                  fn.GROUP_CONCAT(PageView.url))
#              .from_(inner.alias('t1'))
#              .group_by(PageView.ip)
#              .order_by(fn.COUNT(PageView.url).desc())
#              .tuples()
#              .limit(limit))
#     return [(ip, urls.split(',')) for ip, urls in paths]


def print_banner(s):
    print('')
    print('-' * len(s))
    print(s)
    print('-' * len(s))


def run_report(log_lines, limit):
    low  = min([l for l in log_lines], key=lambda l: l.datetime).date
    high = max([l for l in log_lines], key=lambda l: l.datetime).date

    print_banner(f'Overview from {low} to {high}')
    print(f'{page_views(log_lines):#4d} page views')
    print(f'{unique_ips(log_lines):#4d} unique IPs')

    print_banner('Top Pages')
    for title, count in top_pages(log_lines, limit):
        print(f'{count:#4d} : {title}')

    print_banner('Traffic by Date')
    for date, count in traffic_by_date(log_lines):
        print(f'{date} : {count:#4d}')

    print_banner('Referrers')
    for referrer, count in get_referrers(log_lines, limit):
        print(f'{count:#4d} : {referrer}')


def int_or_none(value):
    """
    Coerce a value to an int, or return None if the original value was None.
    """
    try:
        return int(value)
    except TypeError:
        assert value is None
        return None


def should_be_rejected(l):
    if l.referrer == 'https://yellowstonevisitortours.com':
        return True
    return False


def get_log_lines(container, days):
    """
    Read interesting log lines from a running container.
    """
    import tempfile, os
    log_dir = tempfile.mkdtemp(); os.makedirs(log_dir, exist_ok=True)
    cmd = ['docker', 'logs']

    print(log_dir)
    date = dt.date.today()
    date -= dt.timedelta(days=days)

    if days is not None:
        cmd.extend(['--since', date.isoformat() + 'T00:00:00'])
    cmd.append(container)
    with open(f'{log_dir}/logs.txt', 'w') as f:
        proc = subprocess.check_call(cmd,
        stdout=f,
        stderr=f)

    log_lines = []

    for line in open(f'{log_dir}/logs.txt'):
        if 'GET /analytics/a.gif?url=' not in line:
            continue
        match = NGINX_LOG_REGEX.match(line)
        assert match is not None, line
        log_line = LogLine(**match.groupdict())

        if should_be_rejected(log_line):
            continue

        log_lines.append(log_line)

    import shutil; shutil.rmtree(log_dir)
    return log_lines


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    days = int_or_none(args['--days'])

    limit = int_or_none(args['--limit'])
    
    container = args['--container'] or 'infra_alexwlchan_1'

    log_lines = get_log_lines(container=container, days=days)

    run_report(log_lines, limit=limit)
