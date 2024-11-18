require 'net/http'
require 'test/unit'

def get_redirect_target(url)
  uri = URI(url)
  resp = Net::HTTP.get_response(uri)

  assert_equal resp.code, '301'
  resp.headers['location']
end

class TestRedirects < Test::Unit::TestCase
  def test_redirect_without_slash
    target = get_redirect_target(
      'https://alexwlchan.net/2021/06/s3-deprecates-bittorrent'
    )

    assert_equal target, 'https://alexwlchan.net/2021/s3-deprecates-bittorrent/'
  end

  def test_redirect_with_slash
    target = get_redirect_target(
      'https://alexwlchan.net/2021/06/s3-deprecates-bittorrent/'
    )

    assert_equal target, 'https://alexwlchan.net/2021/s3-deprecates-bittorrent/'
  end
end
