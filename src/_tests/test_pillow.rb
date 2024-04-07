# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/pillow/get_image_info'

class TestPillow < Test::Unit::TestCase
  def test_it_gets_image_info
    output = get_image_info(['src/_tests/images/gradient-with-p3.png'])
    assert_equal(output, { 'src/_tests/images/gradient-with-p3.png' => { 'width' => 250, 'height' => 250, 'format' => 'PNG' } })
  end
end
