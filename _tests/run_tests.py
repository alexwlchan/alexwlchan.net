#!/usr/bin/env python
# -*- encoding: utf-8

import pytest
import requests


@pytest.mark.parametrize('path', [
    # Check pagination is working correctly
    '/page/2/', '/page/3/',
])
def test_pages_appear_correctly(path):
    resp = requests.get(f'http://localhost:5757/{path}')
    assert resp.status_code == 200


@pytest.mark.parametrize('path, text_in_page', [
    ('2017/', 'Posts from 2017'),
    ('2017/09/', 'Posts from September 2017'),
    ('', 'Older posts')
])
def test_text_appears_in_pages(path, text_in_page):
    resp = requests.get(f'http://localhost:5757/{path}')
    assert resp.status_code == 200
    assert text_in_page in resp.text
