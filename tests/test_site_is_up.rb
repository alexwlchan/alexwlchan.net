# These are vanilla uptime tests -- load a page and check that it
# gets a 200 OK with some expected text.

require 'test/unit'

require_relative 'utils'

class TestSite < Test::Unit::TestCase
  # Load the alexwlchan.net homepage
  def test_load_homepage
    resp = get_url('https://alexwlchan.net')

    assert_equal resp.code, '200'
    assert resp.body.include? 'This website is where I share stuff I find interesting or fun'
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

  # Load the books.alexwlchan.net homepage
  def test_load_books
    resp = get_url('https://books.alexwlchan.net')

    assert_equal resp.code, '200'
    assert resp.body.include? 'Welcome to my book tracker!'
  end

  # Load the analytics.alexwlchan.net homepage
  def test_load_analytics
    resp = get_url('https://analytics.alexwlchan.net')

    assert_equal resp.code, '200'
    assert resp.body.include? 'This website hosts a tracking pixel for alexwlchan.net and its subdomains'
  end

  # Load "Ideas for Inclusive Events"
  def test_load_ideas_for_inclusive_events
    resp = get_url('https://alexwlchan.net/ideas-for-inclusive-events/')

    assert_equal resp.code, '200'
    assert resp.body.include? 'ideas for inclusive/accessible events'
  end

  def test_add_cover_to_ao3_epubs
    resp = get_url('https://alexwlchan.net/my-tools/add-cover-to-ao3-epubs/')

    assert_equal resp.code, '200'
    assert resp.body.include? 'Add cover images to EPUBs from AO3'
  end
end
