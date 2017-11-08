#!/usr/bin/env python
# -*- encoding: utf-8

from collections import Counter
import datetime
import optparse

from peewee import *

from analytics import database
from analytics import PageView


def get_query(start, end):
    query = PageView.select()
    if start and end:
        query = query.where(PageView.timestamp.between(start, end))
    elif start:
        query = query.where(PageView.timestamp >= start)
    elif end:
        query = query.where(PageView.timestamp <= end)
    return query

def page_views(query):
    return query.count()

def unique_ips(query):
    return (query
            .select(PageView.ip)
            .group_by(PageView.ip)
            .count())

def top_pages(query, limit):
    return (query
            .select(PageView.title, fn.COUNT(PageView.id))
            .group_by(PageView.title)
            .order_by(fn.COUNT(PageView.id).desc())
            .tuples()
            .limit(limit))

def top_traffic_times(query):
    chunks = 3
    hour = fn.date_part('hour', PageView.timestamp) / chunks
    id_count = fn.COUNT(PageView.id)
    result = dict(query
                  .select(hour, id_count)
                  .group_by(hour)
                  .order_by(hour)
                  .tuples())
    total = sum(result.values())
    return [
        ('%s - %s' % (i * chunks, (i + 1) * chunks),
         result[i],
         (100. * result[i]) / total)
        for i in range(24 / chunks)]

def user_agents(query, limit):
    c = Counter(pv.headers.get('User-Agent') for pv in query)
    return c.most_common(limit)

def languages(query, limit):
    c = Counter(pv.headers.get('Accept-Language') for pv in query)
    return c.most_common(limit)

def get_paths(query, limit):
    inner = (query
             .select(PageView.ip, PageView.url)
             .order_by(PageView.timestamp))
    paths = (PageView
             .select(
                 PageView.ip,
                 fn.GROUP_CONCAT(PageView.url))
             .from_(inner.alias('t1'))
             .group_by(PageView.ip)
             .order_by(fn.COUNT(PageView.url).desc())
             .tuples()
             .limit(limit))
    return [(ip, urls.split(',')) for ip, urls in paths]

def get_low_high(query):
    base = query.select(PageView.timestamp)
    def conv(s):
        return datetime.datetime.strptime(
            s, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
    low = base.order_by(PageView.id.asc()).scalar()
    high = base.order_by(PageView.id.desc()).scalar()
    return conv(low), conv(high)

def print_banner(s):
    print('')
    print('-' * len(s))
    print(s)
    print('-' * len(s))

def run_report(start, end, limit, skip_paths=False):
    query = get_query(start, end)
    low, high = get_low_high(query)

    print_banner(f'Overview from {low} to {high}')
    print(f'{page_views(query):#4d} page views')
    print(f'{unique_ips(query):#4d} unique IPs')

    print_banner('Top Pages')
    for title, count in top_pages(query, limit):
        print(f'{count:#4d} : {title}')

    print_banner('Traffic by Hour')
    for hour, count, percent in top_traffic_times(query):
        print(f'{hour:#9d} : {count} ({round(percent, 1)}%%)')

    if not skip_paths:
        print_banner('Paths')
        for ip, path in get_paths(query, limit):
            print(ip)
            for url in path:
                print(f' * {url}')

def get_parser():
    parser = optparse.OptionParser()
    ao = parser.add_option
    ao('-n', '--days', dest='count', type='int',
       help='Number of days worth of records to analyze.')
    ao('-d', '--day', dest='day', type='int',
       help='Day to analyze.')
    ao('-m', '--month', dest='month', type='int',
       help='Month to analyze.')
    ao('-y', '--year', dest='year', type='int',
       help='Year to analyze.')
    ao('-r', '--records', dest='records', type='int', default=20,
       help='Number of records to show')
    ao('-x', '--no-paths', dest='no_paths', action='store_true',
       help='Do not print paths')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    options, args = parser.parse_args()

    database.connect()

    today = datetime.date.today()
    if options.year or options.month or options.day:
        start_date = datetime.date(today.year, 1, 1)
        if options.year:
            start_date = start_date.replace(year=options.year)
        if options.month:
            start_date = start_date.replace(month=options.month)
        if options.day:
            start_date = start_date.replace(day=options.day)
    else:
        start_date = None

    end_date = None
    if options.count:
        delta = datetime.timedelta(days=options.count)
        if start_date:
            end_date = start_date + delta
        else:
            start_date = today - delta

    run_report(start_date, end_date, options.records, options.no_paths)
    database.close()
