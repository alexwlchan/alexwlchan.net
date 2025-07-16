class ImageFormat
  AVIF = { extension: '.avif', mime_type: 'image/avif' }

  WEBP = { extension: '.webp', mime_type: 'image/webp' }

  JPEG = { extension: '.jpg',  mime_type: 'image/jpeg' }
  PNG  = { extension: '.png',  mime_type: 'image/png' }
end

# Get basic information about a single image
def get_single_image_info(path)
  cache = Jekyll::Cache.new('ImageInfo')

  mtime = File.mtime(path).to_i

  cache.getset("#{path}--#{mtime}") do
    require 'vips'

    im = Vips::Image.new_from_file path

    verify_icc_color_profile(path, im)

    im_format = case im.get 'vips-loader'
                when 'jpegload'
                  ImageFormat::JPEG
                when 'pngload'
                  ImageFormat::PNG
                else
                  raise "Unrecognised vips loader for #{path}: #{im.get 'vips-loader'}"
                end

    {
      'width' => im.width,
      'height' => im.height,
      'format' => im_format
    }
  end
end

# Verify the ICC colour profile.
#
# We want to stick to standard sRGB or grayscale colour profiles
# that will render uniformly in all browsers; "interesting" profiles
# like Display P3 may look washed out or incorrect on non-Apple displays.
def verify_icc_color_profile(path, image)
  require 'icc_parser'

  if image.get_typeof('icc-profile-data').zero?
    return
  end

  icc_profile = ICCParser.parse(image.get('icc-profile-data'))
  icc_profile_name = icc_profile[:tags][:desc]

  if icc_profile_name == ''
    return
  end

  allowed_profile_names = Set[
    'sRGB',
    'sRGB built-in',
    'sRGB IEC61966-2.1',
    'Generic Gray Gamma 2.2 Profile'
  ]

  if allowed_profile_names.include? icc_profile_name
    return
  end

  raise "Got image with non-sRGB profile: #{path} (#{icc_profile_name})"
end

def convert_image(request)
  if File.exist? request['out_path']
    return
  end

  require 'vips'

  im = Vips::Image.new_from_file request['in_path']

  # Resize the image to match the target width
  scale = request['target_width'].to_f / im.width
  resized_im = im.resize(scale)

  # Create the parent directory, if it doesn't exist already
  FileUtils.mkdir_p File.dirname(request['out_path'])

  # Actually resize the image
  resized_im.write_to_file request['out_path']
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

# Create all the different sizes of an image.
#
# This returns a map (format) -> (srcset values).
#
# For example:
#
#     {
#       "image/avif"=>"/images/2013/example_925w.avif 925w",
#       "image/webp"=>"/images/2013/example_925.webp 925w",
#       "image/jpeg"=>"/images/2013/example_925.jpg 925w"
#     }
#
def create_image_sizes(source_path, dst_prefix, desired_formats, desired_widths, target_width)
  get_single_image_info(source_path)

  sources = Hash.new { [] }

  desired_widths.each do |this_width|
    desired_formats.each do |out_format|
      # I already have lots of images cut with the _1x, _2x, _3x names,
      # so I retain those when picking names to avoid breaking links or
      # losing Google juice, then switch to _500w, _640w, and so on
      # for larger sizes.
      #
      # This is also used downstream to choose the default image --
      # the 1x image is the default.
      suffix = if !target_width.nil? && (this_width % target_width).zero?
                 "#{this_width / target_width}x"
               else
                 "#{this_width}w"
               end

      out_path = "#{dst_prefix}_#{suffix}#{out_format[:extension]}"

      request = { 'in_path' => source_path, 'out_path' => out_path, 'target_width' => this_width }
      convert_image(request)

      sources[out_format] <<= "#{out_path.gsub('_site', '')} #{this_width}w"
    end
  end

  sources.to_h { |fmt, srcset_values| [fmt[:mime_type], srcset_values.join(',')] }
end
