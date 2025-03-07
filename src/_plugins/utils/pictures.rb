class ImageFormat
  AVIF = { extension: '.avif', mime_type: 'image/avif' }

  WEBP = { extension: '.webp', mime_type: 'image/webp' }

  JPEG = { extension: '.jpg',  mime_type: 'image/jpeg' }
  PNG  = { extension: '.png',  mime_type: 'image/png' }
end

def get_format(image_path, image)
  case image['format']
  when 'PNG'
    ImageFormat::PNG
  when 'JPEG'
    ImageFormat::JPEG
  else
    raise "Unrecognised image extension in #{image_path} (#{image['format']})"
  end
end

def create_source_elements(sources, source_im_format, options)
  format_order = [ImageFormat::AVIF, ImageFormat::WEBP, source_im_format]
                 .reject { |im_format| sources[im_format].nil? }
                 .filter { |im_format| options[:desired_formats].include? im_format }

  source_elements = format_order.map do |im_format|
    if options[:dark_mode]
      <<~HTML
        <source
          srcset="#{sources[im_format].join(', ')}"
          sizes="#{options[:sizes]}"
          type="#{im_format[:mime_type]}"
          media="(prefers-color-scheme: dark)"
        >
      HTML
    else
      <<~HTML
        <source
          srcset="#{sources[im_format].join(', ')}"
          sizes="#{options[:sizes]}"
          type="#{im_format[:mime_type]}"
        >
      HTML
    end
  end

  source_elements.join
end

# Using the bounding box supplied, work out the target width based
# on the actual image dimensions.
#
# Parameters:
#
#   - filename: str, used for error messages only
#   - im_dims and bbox_dims are a set of dimensions, both should
#     be objects with integer width/height attributes
#
# This can happen in two ways:
#
#   - Setting the `width` attribute, which is used directly
#   - Setting the `height` attribute, and then the width is scaled to match
#
def get_target_width(filename, im_dims, bbox_dims)
  # The bounding box has to specify exactly one of width/height.
  if !bbox_dims['width'].nil? && !bbox_dims['height'].nil?
    raise "Picture \"#{filename}\" cannot define both width and height"
  end

  if bbox_dims['width'].nil? & bbox_dims['height'].nil?
    raise "Picture \"#{filename}\" must define one of width/height"
  end

  has_width = !bbox_dims['width'].nil?
  has_height = !bbox_dims['height'].nil?

  # If the bounding box specifies a width, use that directly.
  if has_width
    if im_dims['width'] < bbox_dims['width']
      raise "Picture \"#{filename}\" cannot have target width #{bbox_dims['width']} greater than source width #{im_dims['width']}"
    end

    return bbox_dims['width']
  end

  # If the bounding box specifies a height, scale the width of the
  # source image based on the target height.
  if has_height
    if im_dims['height'] < bbox_dims['height']
      raise "Picture \"#{filename}\" cannot have target height #{bbox_dims['height']} greater than source height #{im_dims['height']}"
    end

    return (im_dims['width'] * bbox_dims['height'] / im_dims['height']).to_i
  end

  # Every image should have a width/height or already be rejected, so
  # this should be unreachable.
  raise 'Unreachable'
end
