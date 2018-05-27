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

from rejections import should_be_rejected


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
    tco_urls = {
        'https://t.co/6R9gyKJfqu': 'https://twitter.com/alexwlchan/status/928389714998104065',
        'https://t.co/qOIaNK1Rmd': 'https://twitter.com/alexwlchan',
        'https://t.co/EY119V2Ga8': 'https://twitter.com/alexwlchan/status/928748092039487490',
        'https://t.co/L5qP7Gsavd': 'https://twitter.com/alexwlchan/status/932634229309100034',
        'https://t.co/E0hBiiizkD': 'https://twitter.com/alexwlchan/status/933416262675451904',
        'https://t.co/Cp9qdEULDR': 'https://twitter.com/alexwlchan/status/935277634568818688',
        'https://t.co/Z5C8w9WWRl': 'https://twitter.com/alexwlchan/status/938925459324264448',
        'https://t.co/ZHOBF3nyGf': 'https://twitter.com/alexwlchan/status/940194916835254272',
        'https://t.co/jrMPDhM7A1': 'https://twitter.com/TheDataLeek/status/940644325553086464',
        'https://t.co/tQhrqJx1Ze': 'https://twitter.com/DRMacIver/status/942685827926241280',
        'https://t.co/lBmTfF24A8': 'https://twitter.com/alexwlchan/status/942680331852877825',
        'https://t.co/lgbeHfos1i': 'https://twitter.com/alexwlchan/status/942918614570676224',
        'https://t.co/86xD9zoYMT': 'https://twitter.com/alexwlchan/status/926418492559065088',
        'https://t.co/8zefP9tssh': 'https://twitter.com/alexwlchan/status/946115070416818177',
        'https://t.co/pIeLZl5gau': 'https://twitter.com/alexwlchan/status/956658216485695491',
        'https://t.co/qM4AMkfML6': 'https://twitter.com/alexwlchan/status/967296057070800897',
        'https://t.co/7xx0yY4vuq': 'https://twitter.com/Ramblin_Dave/status/971171990152384512',
        'https://t.co/brwETm5fGC': 'https://twitter.com/alexwlchan/status/973511842805972993',
        'https://t.co/TCdCkkCQtU': 'https://twitter.com/woodybrood/status/974027386869239810',
        'https://t.co/Vi4b0Xz5dI': 'https://twitter.com/lobsters/status/980237109993730048',
        'https://t.co/ygOyrLcGzr': 'https://twitter.com/foxyjackfox/status/980487168022818816',
        'https://t.co/qOkzmDrlAo': 'https://twitter.com/tabatkins/status/979097435443097601',
        'https://t.co/dYOQOLziei': 'https://twitter.com/alexwlchan',
        'https://t.co/5mHQbayZlz': 'https://twitter.com/alexwlchan/status/986694596402073600',
        'https://t.co/pKCsANyfBW': 'https://twitter.com/larsr_h/status/986936075909238785',
        'https://t.co/Es1aqnxxsl': 'https://twitter.com/alexwlchan/status/992415563266879488',
        'https://t.co/N8dOThXq0I': 'https://twitter.com/alexwlchan/status/996272399531302912',
    }

    if parts.netloc == 't.co':
        for u, v in tco_urls.items():
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

    aliases = {
        'https://uk.search.yahoo.com/': 'https://search.yahoo.com/',
        'http://t.umblr.com/': 'https://tumblr.com/',
        'https://t.umblr.com/': 'https://tumblr.com/',
        'http://usepanda.com/app/': 'https://usepanda.com/app/',
        'https://finduntaggedtumblrposts.com/about/': 'https://finduntaggedtumblrposts.com/',
        'http://forums.xkcd.com/viewtopic.php?f=12&t=124608': 'http://forums.xkcd.com/viewtopic.php?p=4340242',
        'http://forums.xkcd.com/viewtopic.php?f=12&t=124608&p=4340573': 'http://forums.xkcd.com/viewtopic.php?p=4340242',
        'https://github.com/PunkUnicorn/The-Return-of-Tom-Thumb/tree/master': 'https://github.com/PunkUnicorn/The-Return-of-Tom-Thumb',
    }

    return aliases.get(referrer, referrer)


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
    ] or referrer.startswith((
        'http://alert.scansafe.net/alert/',
    ))


def _is_rss_subscriber(referrer):
    return referrer in [
        'https://usepanda.com/',
        'https://www.inoreader.com/',
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
            'wp-content',
            '404.html',
            '/wp-admin',
            '/wp-includes',
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
            '/.git/HEAD'
            'wrapper_format=drupal_ajax',
            '/gen204?invalidResponse',
            '/ws_ftp.ini',
            '/winscp.ini',
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
