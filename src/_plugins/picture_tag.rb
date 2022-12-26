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
#       visible_width="622px"
#     %}
#
# It includes the following mandatory parameters:
#
#     * `filename` is the name of the oriignal image.  This should be in
#       the same per-year directory as the post.
#     * `alt` is the alt text for the image, which must be supplied on
#       all posts (which is checked by the linter plugin).
#     * `visible_width`, which is used to pick the sizes for the different
#       resolutions.  This is a rough guide.
#
# This is a more sophisticated example:
#
#     {%
#       picture
#       filename="IMG_5794.jpg"
#       alt="An engine shed with three tracks leading in."
#       visible_width="500px"
#       style="border: 1px solid red"
#       loading="lazy"
#       link_to_original
#     %}
#
# It includes the `link_to_original` attribute, which means the final
# <picture> tag will be wrapped in an <a> that links to the full-sized image.
# This is useful in gallery posts.
#
# Any other attribute (e.g. `style`) will be passed directly to the underlying
# <img> tag, which allows you to apply styles or behaviours not covered by
# this plugin.

require 'rszr'
require 'shellwords'

class ImageFormat
  AVIF = { :extension => ".avif", :mime_type => "image/avif" }

  WEBP = { :extension => ".webp", :mime_type => "image/webp" }
  
  JPEG = { :extension => ".jpg",  :mime_type => "image/jpeg" }
  PNG  = { :extension => ".png",  :mime_type => "image/png" }
end

module Jekyll
  class PictureTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      # First parse the params string, which is designed to be written
      # with a similar syntax to HTML attributes, e.g.
      #
      #     {% picture filename="IMG_5744.jpg" alt="A black steam engine" %}
      #
      @attrs = {}
      params_string.scan(/(?<key>[a-z_]+)(="(?<value>[^"]+)")?/).each { |k, v|
        @attrs[k] = v
      }
      
      # Now extract a couple of parameters that are required.  This will
      # leave the `@attrs` dict as just containing any extras.
      @filename = @attrs.delete("filename")
      if @filename.nil?
        raise SyntaxError, "Error in `picture` tag: missing required `filename` parameter"
      end
      
      @visible_width = @attrs.delete("visible_width")
      if @visible_width.nil?
        raise SyntaxError, "Error in `picture` tag: missing required `visible_width` parameter"
      end
      @visible_width = @visible_width.gsub(/px/, '').to_i
      
      @link_to_original = @attrs.include? "link_to_original"
      @attrs.delete("link_to_original")
    end
    
    def render(context)
      
      # This tag will always be called in the context of a blog post,
      # when we have access to the post date -- and images are filed
      # in per-year directories to match posts.
      year = context.registers[:page]["date"].year
      
      # This allows us to deduce the source path of the image
      site = context.registers[:site]
      src = site.config["source"]
      dst = site.config["destination"]

      source_path = "#{src}/_images/#{year}/#{@filename}"
      dst_prefix = "#{dst}/images/#{year}/#{File.basename(@filename, ".*")}"
      
      sources = prepare_images(source_path, dst_prefix, @visible_width)
      
      im_format = get_format(source_path)

      extra_attributes = @attrs.map { |k, v| "#{k}=\"#{v}\"" }.join(" ")
      
      inner_html = <<-EOF
<picture>
  <source
    srcset="#{sources[ImageFormat::AVIF].join(",\n            ")}"
    type="image/avif"
  >
  <source
    srcset="#{sources[ImageFormat::WEBP].join(",\n            ")}"
    type="image/webp"
  >
  <source
    srcset="#{sources[im_format].join(",\n            ")}"
    type="#{im_format[:mime_type]}"
  >
  <img
    src="#{sources[im_format][0].gsub(" 1x", "")}"
    #{extra_attributes}
  >
</picture>
EOF
      
      if @link_to_original
        <<-EOF
<a href="#{dst_prefix.gsub(/_site/, '')}#{im_format[:extension]}">
  #{inner_html.split("\n").map { |s| "  #{s}"}.join("\n")}
</a>
EOF
      else
        inner_html.strip
      end
    end
    
    def prepare_images(source_path, dst_prefix, visible_width)
      image_width = get_width(source_path)
      im_format = get_format(source_path)
      
      sources = Hash.new { [] }
      
      for pixel_density in 1..4
        width = pixel_density * visible_width

        if image_width >= width
          for out_format in [im_format, ImageFormat::AVIF, ImageFormat::WEBP]
            out_path = "#{dst_prefix}_#{pixel_density}x#{out_format[:extension]}"
          
            if !File.exist? out_path || File.mtime(out_path) < File.mtime(source_path)
              `convert #{Shellwords.escape(source_path)} -resize #{width}x #{Shellwords.escape(out_path)}`
            end

            sources[out_format] <<= "#{out_path.gsub(/_site/, '')} #{pixel_density}x"
          end
        end
      end
      
      sources
    end

    def get_width(path)
      image = Rszr::Image.load(path)
      image.width
    end
    
    # Get some useful info about the file format
    def get_format(path)
      case File.extname(path)
        when ".png"
          ImageFormat::PNG
        when ".jpeg", ".jpg"
          ImageFormat::JPEG
        else
          raise Error, "Unrecognised image extension: #{File.extname(path)}"
      end
    end
  end
end

Liquid::Template.register_tag("picture", Jekyll::PictureTag)
