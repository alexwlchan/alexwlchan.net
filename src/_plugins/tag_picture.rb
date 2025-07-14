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
#     * `width` or `height`, which is used to pick the sizes for the
#       different resolutions.  This is a rough guide.
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
# The code in this file will create the different variants of each image,
# based on:
#
#     * dimensions, e.g. if the image is going to be shown at 300px wide,
#       it might resize to 300px, 600px and 900px wide versions, to be
#       shown on screens with 1x, 2x, 3px pixel density, respectively
#     * light/dark mode -- if I have an image "cat.jpg" and a second file
#       "cat.dark.jpg", then the latter is used for dark mode
#
# Then it passes all of those variants into my `picture.html` component,
# which actually renders the <picture> tag.
#

require 'fileutils'
require 'json'
require 'pathname'
require 'shell/executer'

require 'htmlcompressor'

require_relative 'pillow/convert_image'
require_relative 'pillow/get_image_info'
require_relative 'utils/attrs'
require_relative 'utils/pictures'

module Jekyll
  class PictureTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      @attrs = parse_attrs(params_string)

      @filename = get_required_attribute(
        @attrs, { tag: 'picture', attribute: 'filename' }
      )

      @bbox_dims = {
        'width' => @attrs.delete('width')&.to_i,
        'height' => @attrs.delete('height')&.to_i
      }

      @parent = @attrs.delete('parent')

      @link_to_original = @attrs.include? 'link_to_original'
      @attrs.delete('link_to_original')

      @link_to = @attrs.delete('link_to')
    end

    def render(context)
      template_args = get_template_args(context)

      tpl = Liquid::Template.parse(File.read('src/_includes/picture.html'))
      html = tpl.render!(
        'sources' => template_args[:sources],
        'default_image' => template_args[:default_image],
        'extra_attributes' => template_args[:extra_attributes],
        'link_target' => template_args[:link_target]
      )

      compressor = HtmlCompressor::Compressor.new
      compressor.compress(html)
    end

    def get_template_args(context)
      @context = context

      lt_source_path = get_source_path
      lt_dst_prefix = get_dst_prefix(lt_source_path)

      raise "Image #{lt_source_path} does not exist" unless File.exist? lt_source_path

      lt_image = get_single_image_info(lt_source_path)
      im_format = get_format(lt_source_path, lt_image)

      # Pick how many widths we're going to cut this image at.
      #
      # Generally 1x/2x/3x is fine, but for specific images I can pick
      # extra sizes and have them added to the list.
      target_width = get_target_width(@filename, lt_image, @bbox_dims)

      # These two attributes allow the browser to completely determine
      # the space that will be taken up by this image before it actually
      # loads, so it won't have to rearrange the page later.  The fancy
      # term for this is "Cumulative Layout Shift".
      #
      # See https://web.dev/optimize-cls/
      @attrs['width'] = target_width
      aspect_ratio = Rational(lt_image['width'], lt_image['height'])
      @attrs['style'] = "aspect-ratio: #{aspect_ratio}; #{@attrs['style'] || ''}".strip

      # Choose what formats I want images to be served in, and the order
      # I'd like them to be offered.
      desired_formats = choose_desired_formats(
        im_format, @attrs['class'], lt_source_path
      )

      # Is there a dark-mode version of this image?
      #
      # Check it exists and that it has the same dimensions as the light
      # variant of the image.
      dk_source_path = choose_dk_path(lt_source_path)

      if File.exist? dk_source_path
        dk_dst_prefix = get_dst_prefix(dk_source_path)
        dk_image = get_single_image_info(dk_source_path)

        if (dk_image['width'] != lt_image['width']) || (dk_image['height'] != lt_image['height'])
          raise "Dark-variant #{dk_source_path} has different dimensions to #{lt_source_path}"
        end
      else
        dk_image = nil
      end

      # I have a CSS rule that adds a white background behind any
      # images shown in dark mode, so e.g. diagrams in transparent PNGs
      # will appear properly.
      #
      # We don't need to this this if there's a dark-mode variant of
      # the image.
      unless dk_image.nil?
        @attrs['class'] = "#{@attrs['class']} dark_aware".strip
      end

      # How large do we want all the images to be?
      desired_widths = (1..3)
                       .map { |pixel_density| pixel_density * target_width }
                       .filter { |w| w <= lt_image['width'] }
                       .sort!

      # Now we have all the information about the images, go ahead and
      # create the different sizes of them.
      lt_sources = create_image_sizes(lt_source_path, lt_dst_prefix, desired_formats, desired_widths, target_width)

      if dk_image.nil?
        dk_sources = {}
      else
        dk_sources = create_image_sizes(dk_source_path, dk_dst_prefix, desired_formats, desired_widths, target_width)
      end

      # Choose the default/fallback image -- we use the 1x version of
      # the light image.  If you're running a browser which doesn't
      # know about the <picture> tag, you're unlikely to be on a
      # device with a hi-res screen or dark mode.
      default_image = lt_sources[im_format[:mime_type]].split[0]

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
      sizes_attribute = "(max-width: #{target_width}px) 100vw, #{target_width}px"

      # Now create the arguments for the picture template.
      lt_sources = lt_sources.map do |media_type, srcset|
        {
          'srcset' => srcset,
          'sizes' => sizes_attribute,
          'type' => media_type
        }
      end

      dk_sources = dk_sources.map do |media_type, srcset|
        {
          'srcset' => srcset,
          'sizes' => sizes_attribute,
          'type' => media_type,
          'media' => '(prefers-color-scheme: dark)'
        }
      end

      if @link_to_original
        dst_prefix = get_dst_prefix(lt_source_path)
        link_target = "#{dst_prefix.gsub('_site', '')}#{im_format[:extension]}"
      elsif @link_to
        link_target = @link_to
      else
        link_target = nil
      end

      {
        # We have to put dark images before light images, otherwise
        # when you load the page in dark mode, the page will load the
        # first matching light image and you won't get the nice dark variant.
        sources: dk_sources + lt_sources,
        default_image: default_image,
        extra_attributes: @attrs,
        link_target: link_target
      }
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
    def get_source_path
      site = @context.registers[:site]
      src = site.config['source']

      if @parent.nil?
        # If this tag is called in the context of a blog post, we have access
        # to the post date -- and images are filed in per-year directories
        # to match posts.
        page = @context.registers[:page]
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
    def get_dst_prefix(source_path)
      site = @context.registers[:site]
      src = site.config['source']
      dst = site.config['destination']

      source_path = Pathname.new(source_path)
      source_prefix = Pathname.new("#{src}/_images")

      suffix = source_path.relative_path_from source_prefix

      # Note that images in the top-level images directory get "/./"
      # for `File.dirname(suffix)`, which we want to remove.
      Pathname.new("#{dst}/images/#{File.dirname(suffix)}/#{File.basename(suffix, '.*')}").cleanpath.to_s
    end
  end
end

Liquid::Template.register_tag('picture', Jekyll::PictureTag)
