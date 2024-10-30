# Tests for some routes that are used to find my Mastodon server,
# which is at social.alexwlchan.net.
#
# My handle is "@alex@alexwlchan.net", so federating servers need
# to be able to find their way to my actual server.

require 'test/unit'

require_relative 'utils'

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
