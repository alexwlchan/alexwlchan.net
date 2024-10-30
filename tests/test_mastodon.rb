require 'test/unit'

require_relative 'utils'

# Tests for some routes that are used by Mastodon to find
# my social.alexwlchan.net server
class TestMastodon < Test::Unit::TestCase
  def test_host_meta
    resp = get_url('https://alexwlchan.net/.well-known/host-meta')

    assert_equal resp.code, '301'
    assert_equal resp['location'], 'https://social.alexwlchan.net/.well-known/host-meta'
  end

  def test_webfinger
    resp = get_url('https://alexwlchan.net/.well-known/webfinger')

    assert_equal resp.code, '301'
    assert_equal resp['location'], 'https://social.alexwlchan.net/.well-known/webfinger'
  end

  def test_nodeinfo
    resp = get_url('https://alexwlchan.net/.well-known/nodeinfo')

    assert_equal resp.code, '301'
    assert_equal resp['location'], 'https://social.alexwlchan.net/.well-known/nodeinfo'
  end
end
