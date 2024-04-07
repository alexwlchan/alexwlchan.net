# frozen_string_literal: true

require 'tmpdir'
require 'test/unit'

require_relative '../_plugins/pillow/convert_image'

class TestPillow < Test::Unit::TestCase
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
