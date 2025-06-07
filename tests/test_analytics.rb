# I run a tracking pixel and analytics dashboard at analytics.alexwlchan.net
#
# This file has tests specific to this application.

require 'test/unit'

require_relative 'utils'

# Tests for analytics.alexwlchan.net
class TestAnalytics < Test::Unit::TestCase
  # The analytics app is running
  def test_homepage_is_up
    resp = get_url('https://analytics.alexwlchan.net/')

    assert_equal resp.code, '200'
  end

  # If you try to load the dashboard as a public user, you can't see it
  def test_dashboard_is_protected
    resp = get_url('https://analytics.alexwlchan.net/dashboard/')

    assert_equal resp.code, '302'
  end
end
