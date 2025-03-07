# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/utils/pictures'

class TestGetTargetWidth < Test::Unit::TestCase
  # If the bounding box specifies a width, then that's used
  def test_chooses_width_if_specified
    im_dims = { 'width' => 1024, 'height' => 768 }
    bbox_dims = { 'width' => 100, 'height' => nil }

    target_width = get_target_width('example.png', im_dims, bbox_dims)
    assert_equal target_width, 100
  end

  # If the bounding box specifies a height, then the image width is scaled
  def test_chooses_based_on_height_if_specified
    im_dims = { 'width' => 1024, 'height' => 768 }
    bbox_dims = { 'width' => nil, 'height' => 192 } # 192 = 768 / 4

    target_width = get_target_width('example.png', im_dims, bbox_dims)
    assert_equal target_width, 256 # 256 = 1024 / 4
  end

  # It's an error to have a target width larger than the source image
  def test_fails_if_target_width_bigger_than_source_image
    im_dims = { 'width' => 1024, 'height' => 768 }
    bbox_dims = { 'width' => 2048, 'height' => nil }

    error = assert_raises RuntimeError do
      get_target_width('example.png', im_dims, bbox_dims)
    end

    assert_equal 'Picture "example.png" cannot have target width 2048 greater than source width 1024', error.message
  end

  # It's an error to have a target height larger than the source image
  def test_fails_if_target_height_bigger_than_source_image
    im_dims = { 'width' => 1024, 'height' => 768 }
    bbox_dims = { 'width' => nil, 'height' => 1536 }

    error = assert_raises RuntimeError do
      get_target_width('example.png', im_dims, bbox_dims)
    end

    assert_equal 'Picture "example.png" cannot have target height 1536 greater than source height 768', error.message
  end

  # A bounding box can't specify both width and height
  def test_fails_if_bbox_specifies_both_dimensions
    im_dims = { 'width' => 1024, 'height' => 768 }
    bbox_dims = { 'width' => 100, 'height' => 100 }

    error = assert_raises RuntimeError do
      get_target_width('example.png', im_dims, bbox_dims)
    end

    assert_equal 'Picture "example.png" cannot define both width and height', error.message
  end

  # A bounding box has to specify at least one of width and height
  def test_fails_if_bbox_specifies_neither_dimensions
    im_dims = { 'width' => 1024, 'height' => 768 }
    bbox_dims = { 'width' => nil, 'height' => nil }

    error = assert_raises RuntimeError do
      get_target_width('example.png', im_dims, bbox_dims)
    end

    assert_equal 'Picture "example.png" must define one of width/height', error.message
  end
end

def test_choose_dk_path
  dk_path = choose_dk_path('src/_images/2025/example.png')
  assert_equal dk_path, 'src/_images/2025/example.dark.png'
end
