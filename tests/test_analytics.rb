# I run a tracking pixel and analytics dashboard at analytics.alexwlchan.net
#
# This file has tests specific to this application.

require 'test/unit'

require_relative 'utils'

# Tests for analytics.alexwlchan.net
class TestAnalytics < Test::Unit::TestCase
  # If you try to load the dashboard as a public user, you can't see it
  def test_dashboard_is_protected
    resp = get_url('https://analytics.alexwlchan.net/dashboard/')

    assert_equal resp.code, '401'
  end
end
