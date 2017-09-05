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
