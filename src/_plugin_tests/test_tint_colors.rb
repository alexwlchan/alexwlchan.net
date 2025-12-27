# frozen_string_literal: true

require 'test/unit'

require 'color'

require_relative '../_plugins/utils/tint_colors'

class TestTintColors < Test::Unit::TestCase
  def test_get_lightness_for_delta
    lab = Color::RGB.by_hex('#d01c11').to_lab
    assert_in_delta get_lightness_for_delta(lab, 'lighter', 6), 50.735, 0.01
  end

  def test_get_colours_like_grey_are_all_grey
    colours = get_colours_like('#292929')
    100.times do
      c = colours.next
      assert_equal(c.to_hsl.saturation, 0)
    end
  end
end
