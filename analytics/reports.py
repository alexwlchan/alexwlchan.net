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
import os
import re
import shutil
import subprocess
import tempfile
from urllib.parse import parse_qs, urlparse

import attr
import docopt


NGINX_LOG_REGEX = re.compile(
    r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - '
    r'\[(?P<datetime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] '
    r'"(?P<method>OPTIONS|HEAD|GET|POST) (?P<url>.+) HTTP/1\.[01]" '
    r'(?P<status>\d{3}) '
    r'(?P<bytes_sent>\d+) '
    r'"(?:(\-)|([^"]*))" '  # referrer
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
    def referrer(self):
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
        'https://t.co/Z5C8w9WWRl': 'https://twitter.com/alexwlchan/status/938925459324264448',
    }

    if parts.netloc == 't.co':
        for u, v in tco_urls.items():
            if referrer.startswith(u):
                return v

    if 'facebook.com' in parts.netloc:
        return 'https://www.facebook.com/'

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
        _normalise_referrer(l.referrer) or None for l in log_lines)
    del c[None]
    return c.most_common(limit)


def print_banner(s):
    print('')
    print('-' * len(s))
    print(s)
    print('-' * len(s))


def summarise_paths(lines, limit):
    c = collections.Counter((l.url, l.status) for l in lines)
    return c.most_common(limit)


def run_report(tracking_lines, not_found_lines, error_lines, limit):
    low  = min([l for l in tracking_lines], key=lambda l: l.datetime).date
    high = max([l for l in tracking_lines], key=lambda l: l.datetime).date

    print_banner(f'Overview from {low} to {high}')
    print(f'{page_views(tracking_lines):#4d} page views')
    print(f'{unique_ips(tracking_lines):#4d} unique IPs')

    print_banner('Top Pages')
    for title, count in top_pages(tracking_lines, limit):
        print(f'{count:#4d} : {title}')

    print_banner('Traffic by Date')
    for date, count in traffic_by_date(tracking_lines):
        print(f'{date} : {count:#4d}')

    print_banner('Referrers')
    for referrer, count in get_referrers(tracking_lines, limit):
        print(f'{count:#4d} : {referrer}')
    
    if any(not_found_lines):
        print_banner('404 errors')
        for path, count in summarise_paths(not_found_lines, limit):
            print(f'{count:#4d} : {path}')

    if any(error_lines):
        print_banner('Server errors')
        for (path, status), count in summarise_paths(error_lines, limit):
            print(f'{count:#4d} : {path} [{status}]')


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
    if (l.referrer is not None) and ('yandex.ru' in l.referrer):
        return True
    return False


def docker_logs(container_name, days):
    """Read log lines from a running container."""
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, 'docker_logs.log')
    os.makedirs(log_dir, exist_ok=True)
    
    start_date = dt.date.today() - dt.timedelta(days=days)
    
    cmd = ['docker', 'logs']
    if days is not None:
        cmd += ['--since', start_date.isoformat() + 'T00:00:00']
    cmd += [container_name]
    
    with open(log_file, 'w') as pipe:
        subprocess.check_call(cmd, stdout=pipe, stderr=pipe)
    
    for line in open(log_file):
        
        # TODO: Handle this sort of line properly.
        if '[error]' in line:
            continue
        
        m = NGINX_LOG_REGEX.match(line)
        assert m is not None, line
        yield LogLine(**m.groupdict())
    
    shutil.rmtree(log_dir)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    days = int_or_none(args['--days'])
    limit = int_or_none(args['--limit'])
    container_name = args['--container'] or 'infra_alexwlchan_1'
    
    tracking_lines = []
    not_found_lines = []
    error_lines = []
    
    for line in docker_logs(container_name=container_name, days=days):
        if should_be_rejected(line):
            continue

        if '/analytics/a.gif?url=' in line.url:
            tracking_lines.append(line)

        # We ignore certain lines for the purposes of errors; they're people
        # crawling the site in ways that are totally uninteresting.
        if any(u in line.url for u in [
            'wp-login.php',
            'wp-content',
            'license.php',
        ]):
            continue

        if line.status == 404:
            not_found_lines.append(line)
        
        if (
            line.status >= 400 and
            line.status != 404 and
            line.status != 410
        ):
            error_lines.append(line)

    run_report(
        tracking_lines=tracking_lines,
        not_found_lines=not_found_lines,
        error_lines=error_lines,
        limit=limit)
