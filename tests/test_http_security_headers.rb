# Check that all of my websites have the right HTTP Security headers.

require 'date'
require 'net/http'
require 'test/unit'

require_relative 'utils'

class TestHttpSecurityHeaders < Test::Unit::TestCase
  def test_alexwlchan
    resp = get_url('https://alexwlchan.net')

    assert_equal resp['Content-Security-Policy'],
                 "default-src 'self' 'unsafe-inline' https://youtube-nocookie.com https://www.youtube-nocookie.com; script-src 'self' 'unsafe-inline'; connect-src https://analytics.alexwlchan.net; img-src 'self' 'unsafe-inline' data:"

    assert_equal resp['Permissions-Policy'],
                 'geolocation=(), midi=(), notifications=(), push=(), sync-xhr=(), microphone=(), camera=(), magnetometer=(), gyroscope=(), vibrate=(), payment=()'

    assert_equal resp['Referrer-Policy'], 'no-referrer-when-downgrade'

    assert_equal resp['Strict-Transport-Security'], 'max-age=31536000; includeSubDomains'

    assert_equal resp['X-Content-Type-Options'], 'nosniff'

    assert_equal resp['X-Frame-Options'], 'ALLOWALL'

    assert_equal resp['X-Xss-Protection'], '1; mode=block'
  end

  def test_books
    resp = get_url('https://books.alexwlchan.net')

    assert_equal resp['Content-Security-Policy'],
                 "default-src ; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self' 'unsafe-inline' https://unpkg.com/;connect-src https://analytics.alexwlchan.net/;"

    assert_equal resp['Permissions-Policy'],
                 'geolocation=(), midi=(), notifications=(), push=(), sync-xhr=(), microphone=(), camera=(), magnetometer=(), gyroscope=(), vibrate=(), payment=()'

    assert_equal resp['Referrer-Policy'], 'no-referrer-when-downgrade'

    assert_equal resp['Strict-Transport-Security'], 'max-age=31536000; includeSubDomains'

    assert_equal resp['X-Content-Type-Options'], 'nosniff'

    assert_equal resp['X-Frame-Options'], 'DENY'

    assert_equal resp['X-Xss-Protection'], '1; mode=block'
  end
end
