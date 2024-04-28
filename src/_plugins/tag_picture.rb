# Creates a <picture> tag for images in blog posts.
#
# This is more than a simple <img> tag; it also handles creating
# multiple formats and resolutions, to minimise the amount of data
# transfer for images in posts.
#
# This includes:
#
#     * Creating copies at different widths from the original, which are
#       used with the `srcset` attribute to send copies appropriate for
#       different screen resolutions.
#
#     * Creating copies in different formats, including WebP, which have
#       better compression and can further reduce data transfer in browsers
#       with appropriate support.
#
#     * Creating the HTML markup with the <picture> and <source> tags which
#       allows browsers to select an appropriate image.
#
# See:
# https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset
# https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
#
# == Example ==
#
# This is a minimal example:
#
#     {%
#       picture
#       filename="IMG_5744.jpg"
#       alt="A black steam engine with a boxy shape."
#       width="622"
#     %}
#
# It includes the following mandatory parameters:
#
#     * `filename` is the name of the oriignal image.  This should be in
#       the same per-year directory as the post.
#     * `alt` is the alt text for the image, which must be supplied on
#       all posts (which is checked by the linter plugin).
#     * `width`, which is used to pick the sizes for the different
#       resolutions.  This is a rough guide.
#
# It will look for the image in `/images/#{year}/#{filename}`, so if this
# was a post from 2022, it will look in `/images/2022/IMG_5744.jpg`.
#
# Other parameters:
#
#     * `link_to_original` -- if added, the final <picture> tag will be
#       wrapped in an <a> that links to the full-sized image.  Useful for
#       gallery-type posts.
#
#     * `link_to="https://example.com/some/page"` -- causes the <a> to link
#       to somewhere other than the full-sized image.
#
#     * `parent="/images"` -- looks for an image in somewhere other than
#       the per-year directory.
#
# Any other attribute (e.g. `style`, `class`) will be passed directly to
# the  underlying <img> tag, which allows you to apply styles or behaviours
# not covered by this plugin.
#
# == How it works ==
#
# Creating images is slow, so rather than doing it one-at-a-time, we batch
# up all the images and then process them all at once.
#
#   1.  Remove the file `.missing_images.json` (if it exists)
#   2.  Render the site.  Add any missing images to this file.
#   3.  Call the external script `create_resized_images.py`, which does the
#       image resizing concurrently.  I'm sure it's possible to do concurrent
#       stuff in Ruby, but I can't work out how.
#

require 'fileutils'
require 'json'
require 'pathname'
require 'shell/executer'

require_relative 'pillow/convert_image'
require_relative 'pillow/get_image_info'
require_relative 'utils/attrs'

class ImageFormat
  AVIF = { extension: '.avif', mime_type: 'image/avif' }

  WEBP = { extension: '.webp', mime_type: 'image/webp' }

  JPEG = { extension: '.jpg',  mime_type: 'image/jpeg' }
  PNG  = { extension: '.png',  mime_type: 'image/png' }
end

module Jekyll
  class PictureTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      @attrs = parse_attrs(params_string)

      @filename = get_required_attribute(
        @attrs, { tag: 'picture', attribute: 'filename' }
      )

      width = @attrs.delete('width')
      height = @attrs.delete('height')

      if width.nil? && height.nil?
        raise "Picture #{@filename} does not specify a width or a height"
      end

      width = width.to_i unless width.nil?
      height = height.to_i unless height.nil?

      @bounding_box = { width:, height: }

      @parent = @attrs.delete('parent')

      @max_width = @attrs.delete('max_width')
      @max_width = @max_width.to_i unless @max_width.nil?

      @link_to_original = @attrs.include? 'link_to_original'
      @attrs.delete('link_to_original')

      @link_to = @attrs.delete('link_to')
    end

    def render(context)
      # This allows us to deduce the source path of the image
      site = context.registers[:site]
      dst = site.config['destination']

      source_path = get_source_path(context)
      dst_prefix = get_dst_prefix(context, source_path)

      raise "Image #{source_path} does not exist" unless File.exist? source_path

      image = get_single_image_info(source_path)
      im_format = get_format(source_path, image)

      # Using the bounding box supplied, work out the target width based
      # on the actual image dimensions.
      if !@bounding_box[:width].nil? && !@bounding_box[:height].nil?
        raise "Picture #{@filename} supplies both width/height; this is unsupported"
      elsif !@bounding_box[:width].nil?
        @width = @bounding_box[:width]
      elsif !@bounding_box[:height].nil?
        @width = (image['width'] * @bounding_box[:height] / image['height']).to_i
      end

      if image['width'] < @width
        raise "Image #{File.basename(source_path)} is only #{image['width']}px wide, less than visible width #{@width}px"
      end

      # These two attributes allow the browser to completely determine
      # the space that will be taken up by this image before it actually
      # loads, so it won't have to rearrange the page later.  The fancy
      # term for this is "Cumulative Layout Shift".
      #
      # See https://web.dev/optimize-cls/
      @attrs['width'] = @width
      aspect_ratio = Rational(image['width'], image['height'])
      @attrs['style'] = "aspect-ratio: #{aspect_ratio}; #{@attrs['style'] || ''}".strip

      # I'm not a fan of the way AVIF and WebP introduce artefacts into
      # PNG screenshots -- it makes text look mucky and pixellated.  Boo!
      #
      # Since screenshots are typically text files that are small, it's
      # okay not to serve them in the optimised formats -- I'll sacrifice
      # a bit of bandwidth for quality.
      desired_formats = if (@attrs['class'] || '').include? 'screenshot'
                          [im_format]
                        else
                          [im_format, ImageFormat::AVIF, ImageFormat::WEBP]
                        end

      sources = prepare_images(source_path, desired_formats, dst_prefix, @width, @max_width)

      dark_path = File.join(
        File.dirname(source_path),
        "#{File.basename(source_path, File.extname(source_path))}.dark#{File.extname(source_path)}"
      )

      if File.exist? dark_path
        dark_image = get_single_image_info(dark_path)

        if (dark_image['width'] != image['width']) || (dark_image['height'] != image['height'])
          raise "Dark-variant #{File.basename(dark_path)} has different dimensions to #{File.basename(source_path)}"
        end

        dark_sources = prepare_images(
          dark_path, desired_formats, "#{dst_prefix}.dark", @width, @max_width
        )
      else
        dark_sources = nil
      end

      default_image = sources[im_format]
                      .map { |im| im.split[0] }
                      .find { |path| path.end_with? "_1x#{im_format[:extension]}" }

      # This creates a `sizes` attribute like
      #
      #     (max-width: 450px) 100vw, 450px
      #
      # which tells the browser an image is an exact width (450px) unless
      # the entire viewport is narrower than that, in which case it fills
      # the screen (100vw).
      #
      # This isn't perfect, e.g. it doesn't account for margins or wrapping,
      # but it's good enough and better than relying on screen density alone.
      dark_html = if dark_sources.nil?
                    ''
                  else
                    avif_source = if desired_formats.include? ImageFormat::AVIF
                                    <<~HTML
                                      <source
                                        srcset="#{dark_sources[ImageFormat::AVIF].join(', ')}"
                                        sizes="(max-width: #{@width}px) 100vw, #{@width}px"
                                        type="image/avif"
                                        media="(prefers-color-scheme: dark)"
                                      >
                                    HTML
                                  else
                                    ''
                                  end

                    webp_source = if desired_formats.include? ImageFormat::WEBP
                                    <<~HTML
                                      <source
                                        srcset="#{dark_sources[ImageFormat::WEBP].join(', ')}"
                                        sizes="(max-width: #{@width}px) 100vw, #{@width}px"
                                        type="image/webp"
                                        media="(prefers-color-scheme: dark)"
                                      >
                                    HTML
                                  else
                                    ''
                                  end

                    original_source = <<~HTML
                      <source
                        srcset="#{dark_sources[im_format].join(', ')}"
                        sizes="(max-width: #{@width}px) 100vw, #{@width}px"
                        type="#{im_format[:mime_type]}"
                        media="(prefers-color-scheme: dark)"
                      >
                    HTML

                    <<~HTML
                      #{avif_source}
                      #{webp_source}
                      #{original_source}
                    HTML
                  end

      # Make sure the CSS doesn't through a white background behind
      # this dark-aware image.
      unless dark_sources.nil?
        @attrs['class'] = "#{@attrs['class']} dark_aware".strip
      end

      extra_attributes = @attrs.map { |k, v| "#{k}=\"#{v}\"" }.join(' ')

      avif_source = if desired_formats.include? ImageFormat::AVIF
                      <<~HTML
                        <source
                          srcset="#{sources[ImageFormat::AVIF].join(', ')}"
                          sizes="(max-width: #{@width}px) 100vw, #{@width}px"
                          type="image/avif"
                        >
                      HTML
                    else
                      ''
                    end

      webp_source = if desired_formats.include? ImageFormat::WEBP
                      <<~HTML
                        <source
                          srcset="#{sources[ImageFormat::WEBP].join(', ')}"
                          sizes="(max-width: #{@width}px) 100vw, #{@width}px"
                          type="image/webp"
                        >
                      HTML
                    else
                      ''
                    end

      original_source = <<~HTML
        <source
          srcset="#{sources[im_format].join(', ')}"
          sizes="(max-width: #{@width}px) 100vw, #{@width}px"
          type="#{im_format[:mime_type]}"
        >
      HTML

      inner_html = <<~HTML
        <picture>
          #{dark_html}
          #{avif_source}
          #{webp_source}
          #{original_source}
          <img
            src="#{default_image}"
            #{extra_attributes}
          >
        </picture>
      HTML

      # Be careful about whitespace here; if you're not careful Kramdown
      # will interpret the indentation as a literal source block, and then
      # HTML markup appears in the page instead of the image!
      #
      # e.g. /2022/egyptian-mixtape/
      html = if @link_to_original
               <<~HTML
                 <a href="#{dst_prefix.gsub('_site', '')}#{im_format[:extension]}">#{inner_html.split("\n").map(&:strip).join(' ')}</a>
               HTML
             elsif @link_to
               <<~HTML
                 <a href="#{@link_to}">#{inner_html.split("\n").map(&:strip).join(' ')}</a>
               HTML
             else
               inner_html
             end

      html.strip
    end

    def prepare_images(source_path, desired_formats, dst_prefix, width, max_width)
      sources = Hash.new { [] }

      image = get_single_image_info(source_path)

      # Pick how many widths we're going to cut this image at.
      #
      # Generally 1x/2x/3x is fine, but for specific images I can pick
      # extra sizes and have them added to the list.
      widths = (1..3)
               .map { |pixel_density| pixel_density * width }
               .filter { |w| w <= image['width'] }
               .filter { |w| max_width.nil? || w <= max_width }
               .sort!

      widths.each do |this_width|
        desired_formats.each do |out_format|
          # I already have lots of images cut with the _1x, _2x, _3x names,
          # so I retain those when picking names to avoid breaking links or
          # losing Google juice, then switch to _500w, _640w, and so on
          # for larger sizes.
          out_path = if (this_width % width).zero?
                       "#{dst_prefix}_#{this_width / width}x#{out_format[:extension]}"
                     else
                       "#{dst_prefix}_#{this_width}w#{out_format[:extension]}"
                     end

          request = { 'in_path' => source_path, 'out_path' => out_path, 'target_width' => this_width }
          convert_image(request)

          sources[out_format] <<= "#{out_path.gsub('_site', '')} #{this_width}w"
        end
      end

      sources
    end

    # Find the path to the source image.
    #
    # This can happen in two ways:
    #
    #   - Setting the `parent` and `filename` attributes, in which case
    #     look for an image with matching filename in the `parent` directory.
    #   - Setting the `filename` attribute, in which case look for an image
    #     in the per-year directory for this page.
    #
    def get_source_path(context)
      site = context.registers[:site]
      src = site.config['source']

      if @parent.nil?
        # If this tag is called in the context of a blog post, we have access
        # to the post date -- and images are filed in per-year directories
        # to match posts.
        page = context.registers[:page]
        year = page['date'].year

        "#{src}/_images/#{year}/#{@filename}"
      else
        "#{src}/#{@parent}/#{@filename}".gsub('/images/', '/_images/').gsub('//', '/')
      end
    end

    # Choose the prefix for all the derivative images of a given source image.
    #
    # e.g. if an image is from `src/_images/2021/green.jpg`, all the derivatives
    # will be of the form `_site/images/2021/green.*`
    #
    def get_dst_prefix(context, source_path)
      site = context.registers[:site]
      src = site.config['source']
      dst = site.config['destination']

      source_path = Pathname.new(source_path)
      source_prefix = Pathname.new("#{src}/_images")

      suffix = source_path.relative_path_from source_prefix

      # Note that images in the top-level images directory get "/./"
      # for `File.dirname(suffix)`, which we want to remove.
      Pathname.new("#{dst}/images/#{File.dirname(suffix)}/#{File.basename(suffix, '.*')}").cleanpath.to_s
    end

    # Get some useful info about the file format
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
  end
end

Liquid::Template.register_tag('picture', Jekyll::PictureTag)
