# Tests for my error pages.

require 'test/unit'

require_relative 'utils'

class TestErrors < Test::Unit::TestCase
  # Loading a page that doesn't exist gets my 404 page
  def test_prebuilt_404
    resp = get_url('https://alexwlchan.net/404/')

    assert_equal resp.code, '200'
    assert resp.body.include? '404 Not Found'
  end

  def test_unknown_url_is_404
    resp = get_url('https://alexwlchan.net/doesnotexist/')

    assert_equal resp.code, '404'
    assert resp.body.include? '404 Not Found'
  end

  # Loading a page that I removed gets my 410 Gone page
  def test_removed_page_is_410
    resp = get_url('https://alexwlchan.net/2015/bbfc-podcast/')

    assert_equal resp.code, '410'
    assert resp.body.include? '410 Gone'
  end

  # Loading a page which is clearly somebody trying to hack WordPress
  # gets my minimal 400 page
  def test_wp_login_is_400
    resp = get_url('https://alexwlchan.net/wp-login.php')

    assert_equal resp.code, '400'
    assert_equal resp.body.strip, '<p>400 Bad Request</p>'
  end
end
