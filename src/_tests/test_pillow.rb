# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/pillow/get_color_profiles'
require_relative '../_plugins/pillow/get_image_info'

class TestPillow < Test::Unit::TestCase
  def test_get_image_info
    output = get_image_info(['src/_tests/images/gradient-with-p3.png'])
    assert_equal(output, { 'src/_tests/images/gradient-with-p3.png' => { 'width' => 250, 'height' => 250, 'format' => 'PNG' } })
  end

  def test_get_color_profiles
    actual = get_color_profiles('src/_tests/images')

    expected = {
      'src/_tests/images/gradient-with-p3.png' => 'Display P3',
      'src/_tests/images/gradient-with-srgb.png' => nil,
    }

    assert_equal(actual, expected)
  end
end
