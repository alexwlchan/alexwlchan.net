#!/usr/bin/env python
# -*- encoding: utf-8
"""
Print a summary of analytics from my website.

Usage: reports.py [options]

Options:
  --days=<COUNT>        Number of days of records to analyse.
  --day=<DAY>           Day to analyse.
  --month=<MONTH>       Month to analyse.
  --year=<YEAR>         Year to analyse.
  --limit=<LIMIT>       Max number of records to show.
  --no-paths            Don't print a complete record of paths by IP.

"""

import collections
from collections import Counter
import datetime as dt
import json
import re
import subprocess
from urllib.parse import parse_qs, urlparse

import attr
import docopt
from peewee import fn

from analytics import database, PageView


NGINX_LOG_REGEX = re.compile(
    r'(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - '
    r'\[(?P<datetime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] '
    r'"(?P<method>GET|POST) (?P<url>.+) HTTP/1\.[01]" '
    r'(?P<status>\d{3}) '
    r'(?P<bytes_sent>\d+) '
    r'"(?P<referrer>(\-)|(.+))" '
    r'"(?P<user_agent>.+)"', flags=re.IGNORECASE)


@attr.s
class LogLine:
    host = attr.ib()
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
    def title(self):
        return parse_qs(urlparse(self.url).query)['t'][0]

    @property
    def date(self):
        return self.datetime.date()


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


def user_agents(query, limit):
    c = Counter(pv.headers.get('User-Agent') for pv in query)
    return c.most_common(limit)


def languages(query, limit):
    c = Counter(pv.headers.get('Accept-Language') for pv in query)
    return c.most_common(limit)


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
    c = Counter(_normalise_referrer(l.referrer) or None for l in log_lines)
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


def run_report(log_lines, limit, skip_paths=False):

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

    # if not skip_paths:
    #     print_banner('Paths')
    #     for ip, path in get_paths(log_lines, limit):
    #         print(ip)
    #         for url in path:
    #             print(f' * {url}')

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


def get_log_lines(username, host):
    """
    Creates an up-to-date log file, then scp's a copy to the local disk.
    """
    # log_file = subprocess.check_output([
    #     'ssh', f'{username}@{host}', './logs/alexwlchan_net.sh'
    # ]).decode('ascii').strip()
    #
    # subprocess.check_output([
    #     'scp', f'{username}@{host}:logs/{log_file}', log_file
    # ])
    log_file = 'alexwlchan.net_2017-11-29_21-00-12.log'

    log_lines = []

    with open(log_file) as infile:
        for line in infile:
            if 'GET /analytics/a.gif?url=' not in line:
                continue
            match = NGINX_LOG_REGEX.match(line)
            assert match is not None, line
            log_line = LogLine(**match.groupdict())

            if should_be_rejected(log_line):
                continue

            log_lines.append(log_line)

    return log_lines


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    year = int_or_none(args['--year'])
    month = int_or_none(args['--month'])
    day = int_or_none(args['--day'])

    limit = int_or_none(args['--limit'])

    today = dt.date.today()

    if year or month or day:
        start_date = dt.date(today.year, 1, 1)
        if year:
            start_date = start_date.replace(year=year)
        if month:
            start_date = start_date.replace(month=month)
        if day:
            start_date = start_date.replace(day=day)
    else:
        start_date = None

    end_date = None
    if day:
        delta = dt.timedelta(days=day)
        if start_date:
            end_date = start_date + delta
        else:
            start_date = today - delta

    log_lines = get_log_lines('alexwlchan', 'helene.linode')

    if start_date:
        log_lines = [l for l in log_lines if l.datetime >= start_date]
    if end_date:
        log_lines = [l for l in log_lines if l.datetime <= end_date]

    run_report(log_lines, limit=limit, skip_paths=args['--no-paths'])
