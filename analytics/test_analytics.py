# -*- encoding: utf-8

import pytest

import reports


@pytest.mark.parametrize('log_line', [
    # Unusual methods
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "HEAD /example HTTP/1.0" 200 0 "http://referrer.org" "Example user agent" "1.2.3.4"',
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "OPTIONS /example HTTP/1.0" 200 0 "http://referrer.org" "Example user agent" "1.2.3.4"',
    
    # Referrer is empty
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "GET /example HTTP/1.0" 200 0 "" "Example user agent" "1.2.3.4"',
])
def test_nginx_regex(log_line):
    assert reports.NGINX_LOG_REGEX.match(log_line) is not None


log_line_params = {
    'forwarded_host': '1.2.3.4',
    'datetime': '01/Jan/2001:00:00:00 +0000',
    'method': 'GET',
    'url': '/',
    'status': '200',
    'bytes_sent': '0',
    'referrer': 'http://referrer.org',
    'user_agent': 'WebKit',
}


@pytest.mark.parametrize('override_params, expected_result', [
    ({'referrer': 'http://yandex.ru'}, True),
    ({'referrer': '-'}, False),
])
def test_should_be_rejected(override_params, expected_result):
    params = log_line_params.copy()
    params.update(override_params)
    line = reports.LogLine(**params)
    assert reports.should_be_rejected(line) is expected_result
