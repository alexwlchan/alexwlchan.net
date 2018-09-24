# -*- encoding: utf-8

import datetime as dt
import logging
import os
from urlparse import urlparse

from http_crawler import crawl
import pytest

_responses = []


@pytest.fixture
def responses(src, baseurl):
    """
    Uses http-crawler to index every internal page, and return a list
    of associated responses.
    """
    def _all_src_paths():
        for path in os.listdir(src):
            yield path
        try:
            for path in os.listdir(os.path.join(src, '_drafts')):
                yield dt.datetime.now().strftime('%Y/%m/') + path
        except OSError:
            pass

    if not _responses:
        for rsp in crawl(baseurl, follow_external_links=False):
            _responses.append(rsp)

        # This is an attempt to pick up pages that I know exist, but which
        # aren't linked from anywhere else on the site.
        for entry in _all_src_paths():
            if not entry.endswith('.md'):
                continue

            url = baseurl + entry.replace('.md', '') + '/'
            for rsp in crawl(url, follow_external_links=False):
                _responses.append(rsp)

        for rsp in crawl(baseurl + '/theme/style-sample/', follow_external_links=False):
            _responses.append(rsp)

    # There's an analytics path which is linked from every page, but only
    # filled in on the production instance -- this avoids recording analytics
    # data in local testing!
    for rsp in _responses:
        if (
            urlparse(rsp.url).path == '/analytics/a.js' and
            rsp.status_code == 404
        ):
            _responses.remove(rsp)

    return _responses


def test_no_links_are_broken(caplog, responses):
    """
    Check that all internal links point to working pages.
    """
    # The DEBUG level logs from inside requests/urllib3 utterly spam
    # the Travis output if this test fails.  This reduces the amount
    # of logging captured by pytest.
    #
    # See https://docs.pytest.org/en/latest/logging.html#caplog-fixture
    #
    caplog.set_level(logging.INFO)

    failed_responses = [rsp for rsp in responses if rsp.status_code != 200]
    failures = set([
        '%s (%d)' % (rsp.url, rsp.status_code)
        for rsp in failed_responses
    ])
    print('\n'.join(sorted(failures)))
    assert len(failures) == 0
