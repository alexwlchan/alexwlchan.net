# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/utils/picture'

class TestGetColourProfiles < Test::Unit::TestCase
  def test_it_finds_multiple_files
    actual = get_colour_profiles('src/_tests/images')

    expected = {
      'src/_tests/images/gradient-with-p3.png' => 'Display P3'
    }

    assert_equal(actual, expected)
  end
end
