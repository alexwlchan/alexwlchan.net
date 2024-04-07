# frozen_string_literal: true

require 'tmpdir'
require 'test/unit'

require_relative '../_plugins/pillow/convert_image'
require_relative '../_plugins/pillow/get_image_info'

class TestPillow < Test::Unit::TestCase
  def test_get_image_info
    output = get_image_info(['src/_tests/images/gradient.png'])
    assert_equal(output, { 'src/_tests/images/gradient.png' => { 'width' => 250, 'height' => 250, 'format' => 'PNG' } })
  end

  def test_convert_image
    Dir.mktmpdir do |d|
      convert_image({
                      'in_path' => 'src/_tests/images/gradient.png',
                      'out_path' => "#{d}/gradient.png",
                      'target_width' => 125
                    })
    end
  end

  def test_can_convert_image_to_avif
    Dir.mktmpdir do |d|
      convert_image({
                      'in_path' => 'src/_tests/images/gradient.png',
                      'out_path' => "#{d}/gradient.avif",
                      'target_width' => 250
                    })
    end
  end
end
