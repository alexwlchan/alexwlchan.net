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
import toml


REFERRER_CONFIG = toml.loads(open('referrers.toml').read())
REJECTIONS_CONFIG = toml.loads(open('rejections.toml').read())

NGINX_LOG_REGEX = re.compile(
    r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - '
    r'\[(?P<datetime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] '
    r'"(?P<method>OPTIONS|HEAD|GET|POST) (?P<url>.+) HTTP/1\.[01]" '
    r'(?P<status>\d{3}) '
    r'(?P<bytes_sent>\d+) '
    r'"(?:(\-)|([^"]*))" '  # referrer
    r'"(?P<user_agent>[^"]*)" '
    r'"(?P<forwarded_host>[^"]+)"', flags=re.IGNORECASE)


def _convert_to_dt(d):
    if isinstance(d, str):
        return dt.datetime.strptime(d, '%d/%b/%Y:%H:%M:%S %z')
    else:
        return d


@attr.s
class LogLine:
    forwarded_host = attr.ib()
    datetime = attr.ib(convert=_convert_to_dt)
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
        try:
            return parse_qs(urlparse(self.url).query)['t'][0]
        except KeyError:
            return None

    @property
    def date(self):
        return self.datetime.date()

    @property
    def referrer(self):
        try:
            return parse_qs(urlparse(self.url).query)['ref'][0]
        except KeyError:
            return ''

    @property
    def target_url(self):
        return parse_qs(urlparse(self.url).query)['url'][0].replace('https://alexwlchan.net', '')


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


def _normalise_referrer(log_line):
    referrer = log_line.referrer
    parts = urlparse(referrer)
    qs = parse_qs(parts.query)

    # All international flavours of Google get collapsed into a single
    # set of results, split out only if a query string is visible.
    if parts.netloc.startswith(('www.google.', 'encrypted.google.')):
        try:
            return f'Google ({qs["q"][0]})'
        except KeyError:
            return 'Google'

    if referrer == 'android-app://com.google.android.googlequicksearchbox':
        return 'Google'

    if parts.netloc.endswith('bing.com'):
        try:
            return f'Bing ({qs["q"][0]})'
        except KeyError:
            return 'Bing'

    if parts.netloc == 'duckduckgo.com':
        try:
            return f'DuckDuckGo ({qs["q"][0]})'
        except KeyError:
            return 'DuckDuckGo'

    if parts.netloc == 'nortonsafe.search.ask.com':
        try:
            return f'Norton Safe Search ({qs["q"][0]})'
        except KeyError:
            return 'Norton Safe Search'

    if referrer.startswith('https://getpocket.com/redirect'):
        try:
            new_log_line = attr.evolve(log_line, url=qs['url'][0])
            return _normalise_referrer(new_log_line)
        except KeyError:
            pass

    if ('ask.com' in parts.netloc) or ('search.myway.com' in parts.netloc):
        try:
            return f'Ask.com ({qs["searchfor"][0]})'
        except KeyError:
            pass

    if 'izito.co.uk' in parts.netloc:
        try:
            return f'Izito ({qs["q"][0]})'
        except KeyError:
            pass

    if 'search.yahoo.com' in parts.netloc:
        try:
            return f'Yahoo Search ({qs["p"][0]})'
        except KeyError:
            pass

    if 'zapmeta.co.uk' in parts.netloc:
        try:
            return f'ZapMeta ({qs["q"][0]})'
        except KeyError:
            pass

    # If the referrer was somewhere else on the site, it's not interesting.
    if parts.netloc == 'alexwlchan.net':
        return None

    # t.co URLs are unhelpful because they don't tell you which tweet
    # something came from; unpick them.  Note that some have ?amp=1 on the
    # end, which is extra annoying.
    if parts.netloc == 't.co':
        for u, v in REFERRER_CONFIG['twitter'].items():
            if referrer.startswith(u):
                return v

    if 'facebook.com' in parts.netloc:
        return 'https://www.facebook.com/'

    if parts.netloc == 'r.search.yahoo.com':
        return 'https://search.yahoo.com/'

    if any(p in referrer for p in [
        'translate.googleusercontent.com',
        'openlinkprofiler.org',
    ]):
        return None

    meetup_urls = [
        'https://www.meetup.com/CamPUG/events/246459416/',
    ]
    for m in meetup_urls:
        if referrer.startswith(m):
            return m

    lobster_urls = {
        'iesjwi': {
             'canonical': 'https://lobste.rs/s/iesjwi/plumber_s_guide_git',
             'url': '/a-plumbers-guide-to-git/',
             'date': dt.datetime(2018, 3, 31).date(),
        },
    }
    if (
        referrer.startswith('https://lobste.rs/') or
        referrer == 'https://feedly.com/i/subscription/feed%2Fhttps%3A%2F%2Flobste.rs%2Frss' or
        referrer == 'https://newsblur.com/site/1328462/lobsters'
    ):
        for short_id, data in lobster_urls.items():
            if referrer.startswith(f'https://lobste.rs/s/{short_id}'):
                return data['canonical']
            if (
                log_line.target_url == data['url'] and
                log_line.datetime.date() - data['date'] <= dt.timedelta(days=14)
            ):
                return data['canonical']

    if referrer.startswith('https://stackshare.io/news/article/343615/'):
        return 'https://stackshare.io/news/article/343615/a-plumber-s-guide-to-git'

    if (
        referrer == 'https://afreshcup.com/' or
        referrer == 'https://feedly.com/i/subscription/feed%2Fhttp%3A%2F%2Fafreshcup.com%2Fhome%2Frss.xml' or
        referrer == 'https://feedly.com/i/subscription/feed%2Fhttps%3A%2F%2Fafreshcup.com%2Ffeed.xml'
    ) and (log_line.datetime.date() - dt.datetime(2018, 4, 9).date() <= dt.timedelta(days=25)):
        return 'https://afreshcup.com/home/2018/04/09/double-shot-2071'

    if referrer.startswith('https://finduntaggedtumblrposts.com/'):
        return 'https://finduntaggedtumblrposts.com/'

    referrer = referrer.replace('blogspot.co.uk', 'blogspot.com')
    referrer = referrer.replace('blogspot.ca', 'blogspot.com')

    return REFERRER_CONFIG['aliases'].get(referrer, referrer)


def _is_search_traffic(referrer):
    return referrer in [
        'Google',
        'https://search.yahoo.com/',
        'DuckDuckGo',
        'https://results.searchlock.com/',
        'Bing',
        'https://qwant.com/',
        'https://www.qwant.com/',
        'https://www.startpage.com/',
        'Norton Safe Search',
        'https://www.discretesearch.com/',
        'https://www.startpage.com/do/search',
        'https://google.90h6.cn:1668/',
        'https://www.ixquick.com/',
        'https://www.ecosia.org/',
        'https://in.search.yahoo.com/',
        'http://adguard.com/referrer.html',
        'android-app://com.google.android.gm',
    ] or referrer.startswith((
        'http://alert.scansafe.net/alert/',
    ))


def _is_rss_subscriber(referrer):
    return referrer in [
        'https://usepanda.com/',
        'https://www.inoreader.com/',
        'https://feedly.com/i/latest',
        'https://www.newsblur.com/site/6592571/alexwlchan',
    ]


def get_referrers(log_lines, limit):
    c = collections.Counter()
    for l in log_lines:
        r = _normalise_referrer(log_line=l)
        if r:
            if _is_search_traffic(r):
                c['[Search traffic]'] += 1
            elif _is_rss_subscriber(r):
                c['[RSS subscription]'] += 1
            else:
                c[r] += 1
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
    most_traffic = max(count for _, count in traffic_by_date(tracking_lines))
    increment = most_traffic / 25
    for date, count in traffic_by_date(tracking_lines):
        bar = '█' * int(count / increment) or '▏'
        print(f'{date}: {count:#4d} {bar}')

    print_banner('Referrers')
    for referrer, count in get_referrers(tracking_lines, limit):
        print(f'{count:#4d} : {referrer}')

    if any(not_found_lines):
        print_banner('404 errors')
        for (path, _), count in summarise_paths(not_found_lines, limit):
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

        if 'conflicting parameter "/archives/"' in line:
            continue

        m = NGINX_LOG_REGEX.match(line)
        if m is None:
            print('???', line)
            continue
        yield LogLine(**m.groupdict())

    shutil.rmtree(log_dir)


def should_be_rejected(log_line):
    parts = urlparse(log_line.url.lower())

    if parts.path in REJECTIONS_CONFIG['bad_paths']:
        return True

    if parts.path.startswith(tuple(REJECTIONS_CONFIG['bad_path_prefixes'])):
        return True

    if parts.path.endswith(tuple([s.lower() for s in REJECTIONS_CONFIG['bad_path_suffixes']])):
        return True

    if any(u in log_line.user_agent for u in REJECTIONS_CONFIG['bad_user_agents']):
        return True

    if log_line.referrer in REJECTIONS_CONFIG['bad_referrers']:
        return True

    if (
        log_line.referrer is not None and
        any(r in log_line.referrer.lower() for r in REJECTIONS_CONFIG['bad_referrer_components'])
    ):
        return True

    return False


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
        if any(u.lower() in line.url.lower() for u in [
            '404.html',
            '/op69okl',
            '/phpmanager',
            '/sso/login',
            '/com_b2jcontact/',
            '/jm-ajax/',
            '/jquery-file-upload/',
            '/joomla.xml',
            '/umbraco',
            '/adminer',
            '/admin.js',
            '/CFIDE/',
            '/ArticleBookmark@2x.png',
            '/ArticleDetail',
            'wrapper_format=drupal_ajax',
            '/gen204?invalidResponse',
            '/filezilla.xml',
            '/sitemanager.xml',
            '/config/databases.yml',
            '/config/database.yml',
            '/mysql/',
        ]) or line.url.endswith('/ws'):
            continue

        # I have no idea why this is a pattern of requests, but it is.
        if (
            line.url.startswith(('/alexwlchan', '/www', '/web', '/\\xEF')) and
            line.url.endswith(('.rar', '.zip', '.tar.gz'))
        ):
            continue

        # This is a private part of the site!
        if line.url.startswith('/attic/'):
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
