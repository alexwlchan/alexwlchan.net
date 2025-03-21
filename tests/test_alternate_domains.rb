# I have a variety of alternative domains and subdomains which all
# redirect to my main website.
#
# e.g. www.alexwlchan.net and alexwlchan.com
#
# These tests check that all of these domains are redirecting to
# my website correctly, including over HTTP and HTTPS.

require 'test/unit'

require_relative 'utils'

class TestAlternateDomains < Test::Unit::TestCase
  # My website redirects from HTTP to HTTPS
  def test_http_redirects_to_https
    resp = get_url('http://alexwlchan.net')

    assert_equal resp.code, '308'
    assert_equal resp['location'], 'https://alexwlchan.net/'
  end

  # If you look at a sub-path over HTTP, you're redirected to the same path
  # but at the HTTPS site
  def test_http_redirects_to_https_with_path
    resp = get_url('http://alexwlchan.net/contact/')

    assert_equal resp.code, '308'
    assert_equal resp['location'], 'https://alexwlchan.net/contact/'
  end

  # www.alexwlchan.net redirects to alexwlchan.net (HTTPS)
  def test_www_redirects_to_apex
    resp = get_url('https://www.alexwlchan.net')

    assert_equal resp.code, '301'
    assert_equal resp['location'], 'https://alexwlchan.net/'
  end

  # www.alexwlchan.net redirects from HTTP to HTTPS
  #
  # TODO: This should redirect directly to the apex domain
  def test_www_http_redirects_to_apex
    resp = get_url('http://www.alexwlchan.net')

    assert_equal resp.code, '308'
    assert_equal resp['location'], 'https://www.alexwlchan.net/'
  end

  # alexwlchan.com redirects to alexwlchan.net
  def test_dotcom_redirects_to_apex
    resp = get_url('https://alexwlchan.com')

    assert_equal resp.code, '301'
    assert_equal resp['location'], 'https://alexwlchan.net/'
  end

  def test_dotcom_http_redirects_to_apex
    resp = get_url('http://alexwlchan.com')

    assert_equal resp.code, '308'
    assert_equal resp['location'], 'https://alexwlchan.com/'
  end

  # alexwlchan.co.uk redirects to alexwlchan.net
  def test_dotcouk_redirects_to_apex
    resp = get_url('https://alexwlchan.co.uk')

    assert_equal resp.code, '301'
    assert_equal resp['location'], 'https://alexwlchan.net/'
  end

  def test_dotcouk_http_redirects_to_apex
    resp = get_url('http://alexwlchan.co.uk')

    assert_equal resp.code, '308'
    assert_equal resp['location'], 'https://alexwlchan.co.uk/'
  end
end
