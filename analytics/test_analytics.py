# -*- encoding: utf-8

import pytest

from reports import NGINX_LOG_REGEX


@pytest.mark.parametrize('log_line', [
    # Unusual methods
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "HEAD /example HTTP/1.0" 200 0 "http://referrer.org" "Example user agent" "1.2.3.4"',
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "OPTIONS /example HTTP/1.0" 200 0 "http://referrer.org" "Example user agent" "1.2.3.4"',
    
    # Referrer is empty
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "GET /example HTTP/1.0" 200 0 "" "Example user agent" "1.2.3.4"',
])
def test_nginx_regex(log_line):
    assert NGINX_LOG_REGEX.match(log_line) is not None
