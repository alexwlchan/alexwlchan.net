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

# Choose what formats I want images to be served in, and the order
# I'd like them to be offered.
#
# I'm not a fan of the way AVIF and WebP introduce artefacts into
# PNG screenshots -- it makes text look mucky and pixellated.  Boo!
#
# Since screenshots are typically text files that are small, it's
# okay not to serve them in the optimised formats -- I'll sacrifice
# a bit of bandwidth for quality.
#
# 18 October 2024: I've excluded a few images, because they're on
# a post that's going somewhat viral and I'm eating my bandwidth
# pretty quickly.
def choose_desired_formats(im_format, css_class, source_path)
  png_only_images = [
    'src/_images/2024/finder_website.png',
    'src/_images/2024/static-screenshots.png',
    'src/_images/2024/static-videos.png',
    'src/_images/2024/static-bookmarks.png'
  ]

  if (css_class || '').include? 'screenshot'
    [im_format]
  elsif png_only_images.include? source_path
    [im_format]
  else
    [ImageFormat::AVIF, ImageFormat::WEBP, im_format]
  end
end

# Returns the path where a dark variant of an image should be saved.
def choose_dk_path(lt_source_path)
  File.join(
    File.dirname(lt_source_path),
    "#{File.basename(lt_source_path, File.extname(lt_source_path))}.dark#{File.extname(lt_source_path)}"
  )
end
