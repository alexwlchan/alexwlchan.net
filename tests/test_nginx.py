# -*- encoding: utf-8

import requests
import pytest


@pytest.mark.parametrize('path, expected_status', [
    ('/tools/specktre', 410),
    ('/experiments/specktre', 410),
])
def test_nginx_resolves_correctly(nginx_hostname, path, expected_status):
    resp = requests.get('http://%s%s' % (nginx_hostname, path))
    assert resp.status_code == expected_status


@pytest.mark.parametrize('path, expected_location', [
    ('/feeds/all.atom.xml', '/atom.xml'),
])
def test_nginx_resolves_correctly(nginx_hostname, path, expected_location):
    resp = requests.head('http://%s%s' % (nginx_hostname, path))
    assert resp.status_code == 301
    expected_location = 'https://alexwlchan.net' + expected_location
    assert resp.headers['Location'] == expected_location
