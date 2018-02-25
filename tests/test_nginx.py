# -*- encoding: utf-8

import requests
import pytest


@pytest.mark.parametrize('path', [
    '/tools/specktre',
    '/tools/specktre/foo',
    '/experiments/specktre',
    '/experiments/specktre/foo',
    '/experiments/rss/bbfc.xml',
    '/experiments/gtd/gtd_YQJdL.xml',
    '/experiments/gtd/gtd_YQJdL_1.xml',
    '/experiments/gtd/gtd_YQJdL_2.xml',
    '/experiments/gtd/cover2.jpg',
    '/podcasts/podramble-feed.xml',
    '/podcasts/podramble.png',
    '/podcasts/overcast-red.png',
])
def test_nginx_is_removed(nginx_hostname, path):
    resp = requests.get('http://%s%s' % (nginx_hostname, path))
    assert resp.status_code == 410


@pytest.mark.parametrize('path, expected_location', [
    ('/feeds/all.atom.xml', '/atom.xml'),
    ('/favicon.ico', '/theme/favicon.ico'),
    ('/view/img/favicon.ico', '/theme/favicon.ico'),
    ('/apple-touch-icon.png', '/theme/apple-touch-icon.png'),
    ('/apple-touch-icon-precomposed.png', '/theme/apple-touch-icon.png'),

    # Redirects work with and without the slash
    ('/tag/os', '/tags/#tag__os-x/'),
    ('/tag/os/', '/tags/#tag__os-x/'),
    ('/tag/x/', '/tags/#tag__os-x/'),
    ('/tag/pycon/', '/tags/#tag__pyconuk/'),

    # The tag redirects for February 2018 work correctly
    ('/tag', '/tags/'),
    ('/tag/', '/tags/'),
    ('/tag/python', '/tags/#tag__python'),
])
def test_nginx_resolves_correctly(nginx_hostname, path, expected_location):
    resp = requests.head('http://%s%s' % (nginx_hostname, path))
    assert resp.status_code == 301
    expected_location = 'https://alexwlchan.net' + expected_location
    assert resp.headers['Location'] == expected_location
