# -*- encoding: utf-8

from http_crawler import crawl


def test_no_links_are_broken(baseurl):
    """
    Check that all internal links point to working pages.
    """
    responses = []
    for rsp in crawl(baseurl, follow_external_links=False):
        responses.append(rsp)

    failed_responses = [rsp for rsp in responses if rsp.status_code != 200]
    failures = [
        '%s (%d)' % (rsp.url, rsp.status_code)
        for rsp in failed_responses
    ]
    print('\n'.join(failures))
    assert len(failures) == 0
