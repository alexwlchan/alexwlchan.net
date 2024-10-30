require 'net/http'
require 'test/unit'

def get_url(url)
  uri = URI(url)
  Net::HTTP.get_response(uri)
end

# Basic tests for my website.
class TestSite < Test::Unit::TestCase
  # Load the alexwlchan.net homepage
  def test_load_homepage
    resp = get_url('https://alexwlchan.net')

    assert_equal resp.code, '200'
    assert resp.body.include? 'This website is a place to share stuff I find interesting or fun.'
  end

  # Load my articles page
  def test_load_articles_page
    resp = get_url('https://alexwlchan.net/articles/')

    assert_equal resp.code, '200'
    assert resp.body.include? 'Articles'
  end

  # Load a static file
  def test_load_images
    resp = get_url('https://alexwlchan.net/images/profile_green_square_1x.jpg')

    assert_equal resp.code, '200'
  end
end
