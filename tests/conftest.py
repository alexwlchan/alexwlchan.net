# -*- encoding: utf-8

import os

import pytest


@pytest.fixture
def hostname():
    host = os.environ.get('HOSTNAME', 'localhost')
    port = os.environ.get('PORT', 5757)
    return '%s:%s' % (host, port)


@pytest.fixture
def nginx_hostname():
    return 'alexwlchan:80'


@pytest.fixture
def baseurl(hostname):
    return 'http://%s/' % hostname


@pytest.fixture
def repo():
    if os.environ.get('DOCKER') == 'true':
        return '/repo'
    else:
        import subprocess
        return subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()


@pytest.fixture
def src(repo):
    return os.path.join(repo, 'src')
