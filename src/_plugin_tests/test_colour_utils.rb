# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/utils/colour'

class TestColourUtils < Test::Unit::TestCase
  def test_acpa_contrast
    test_cases = [
      { txt_hex: '#000000', bg_hex: '#ffffff', contrast: 106.041 },
      { txt_hex: '#ffffff', bg_hex: '#000000', contrast: -107.884 },
      { txt_hex: '#ff0000', bg_hex: '#000000', contrast: -37.545 },
      { txt_hex: '#000000', bg_hex: '#00ff00', contrast: 86.527 }
    ]

    test_cases.each do |tt|
      actual = Alexwlchan::ColourUtils.calculate_apca_contrast(tt[:txt_hex], tt[:bg_hex])
      expected = tt[:contrast]

      assert_block("actual = #{actual}, expected = #{expected}") do
        (actual - expected).abs < 0.001
      end
    end
  end
end
