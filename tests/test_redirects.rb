require 'net/http'
require 'test/unit'

# Fetch a URL and return the location it redirects to.
def get_redirect_target(url)
  uri = URI(url)
  resp = Net::HTTP.get_response(uri)

  assert_equal resp.code, '301'
  resp.header['location']
end

class TestRedirects < Test::Unit::TestCase
  # Going to the old /YYYY/MM/ URLs for articles redirects to the
  # new /YYYY/ URL structure
  def test_basic_redirect
    target = get_redirect_target(
      'https://alexwlchan.net/2021/06/s3-deprecates-bittorrent/'
    )

    assert_equal target, '/2021/s3-deprecates-bittorrent/'
  end
end
