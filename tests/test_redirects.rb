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

  # The `til.alexwlchan.net` domain redirects to `alexwlchan.net`.
  def test_til_redirect
    target = get_redirect_target('https://til.alexwlchan.net/')

    assert_equal target, 'https://alexwlchan.net/til/'
  end

  # A post on `til.alexwlchan.net` redirects to the appropriate page
  # on `alexwlchan.net`
  def test_til_post_redirect
    target = get_redirect_target('https://til.alexwlchan.net/animate-svg-elements-with-animate/')

    assert_equal target, 'https://alexwlchan.net/til/2024/animate-svg-elements-with-animate/'
  end
  
  # The old /all-posts URL redirects to /articles
  def test_all_posts_redirect
    target = get_redirect_target('https://alexwlchan.net/all-posts')
    
    assert_equal target, 'https://alexwlchan.net/articles/'
    
    target = get_redirect_target('https://alexwlchan.net/all-posts/')
    
    assert_equal target, 'https://alexwlchan.net/articles/'
  end
end
