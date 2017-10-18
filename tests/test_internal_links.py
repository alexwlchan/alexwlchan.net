# -*- encoding: utf-8

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
    if not _responses:
        for rsp in crawl(baseurl, follow_external_links=False):
            _responses.append(rsp)

        # This is an attempt to pick up pages that I know exist, but which
        # aren't linked from anywhere else on the site.
        for entry in os.listdir(src):
            if not entry.endswith('.md'):
                continue

            url = baseurl + '/%s' % entry.replace('.md', '')
            for rsp in crawl(url, follow_external_links=False):
                _responses.append(rsp)

    return _responses


def test_no_links_are_broken(responses):
    """
    Check that all internal links point to working pages.
    """
    failed_responses = [rsp for rsp in responses if rsp.status_code != 200]
    failures = [
        '%s (%d)' % (rsp.url, rsp.status_code)
        for rsp in failed_responses
    ]
    print('\n'.join(sorted(failures)))
    assert len(failures) == 0


def images_in_repo(src):
    """
    Generates paths to all the image files in the ``src`` directory.
    """
    images_dir = os.path.join(src, '_images')
    for root, _, filenames in os.walk(images_dir):
        for f in filenames:
            if f.startswith('.'):
                continue
            yield os.path.join(root, f)


def test_all_images_are_linked_somewhere(src, responses):
    """
    Check that every image in ``src/_images`` is linked somewhere on the site.
    """
    paths = [urlparse(rsp.url).path for rsp in responses]
    img_paths = {p for p in paths if p.startswith('/images/')}

    local_paths = set()
    for path in images_in_repo(src):
        local_path = path.replace(src, '').replace('_images', 'images')
        local_paths.add(local_path)

    unlinked_paths = local_paths - img_paths
    print('\n'.join(sorted(unlinked_paths)))
    assert len(unlinked_paths) == 0
