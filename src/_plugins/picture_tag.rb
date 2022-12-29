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
# It will look for the image in `/images/#{year}/#{filename}`, so if this
# was a post from 2022, it will look in `/images/2022/IMG_5744.jpg`.
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
# This example files the image in something other than the per-year directory:
#
#     {%
#.      picture
#.      filename="profile_green.jpg"
#.      parent="/images"
#.      visible_width="750px"
#.    %}
#
# Any other attribute (e.g. `style`) will be passed directly to the underlying
# <img> tag, which allows you to apply styles or behaviours not covered by
# this plugin.
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
require 'shellwords'
require 'thread'

require 'rszr'

require_relative 'plugin_base'

class ImageFormat
  AVIF = { :extension => ".avif", :mime_type => "image/avif" }

  WEBP = { :extension => ".webp", :mime_type => "image/webp" }
  
  JPEG = { :extension => ".jpg",  :mime_type => "image/jpeg" }
  PNG  = { :extension => ".png",  :mime_type => "image/png" }
end

Jekyll::Hooks.register :site, :after_reset do |site|
  File.delete('.missing_images.json') if File.exists? '.missing_images.json'
end

Jekyll::Hooks.register :site, :post_render do |site|
  if File.exist? ".missing_images.json"  
    jobs = Queue.new

    File.readlines('.missing_images.json').uniq.each do |line|
      jobs.push(JSON.load(line))
    end

    puts "Creating images..."

    workers = (10).times.map do
      Thread.new do
        begin
          while this_job = jobs.pop(true)
            FileUtils.mkdir_p File.dirname(this_job["out_path"])
            `convert #{Shellwords.escape(this_job["source_path"])} -resize #{this_job["width"]}x#{this_job["height"]} #{Shellwords.escape(this_job["out_path"])}`          
          end
        end
      rescue ThreadError
      end
    end

    workers.map(&:join)
  end
end

module Jekyll
  class PictureTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      @attrs = parse_attrs(params_string)
      
      @filename = get_required_attribute(
        @attrs, { :tag => "picture", :attribute => "filename" }
      )
      
      @visible_width = get_required_attribute(
        @attrs, { :tag => "picture", :attribute => "visible_width" }
      ).gsub(/px/, '').to_i
      
      @parent = @attrs.delete("parent")
      
      @link_to_original = @attrs.include? "link_to_original"
      @attrs.delete("link_to_original")
    end
    
    def render(context)
      # This allows us to deduce the source path of the image
      site = context.registers[:site]
      src = site.config["source"]
      dst = site.config["destination"]
      
      if @parent.nil?      
        # If this tag is called in the context of a blog post, we have access
        # to the post date -- and images are filed in per-year directories
        # to match posts.
        year = context.registers[:page]["date"].year

        source_path = "#{src}/_images/#{year}/#{@filename}"
        dst_prefix = "#{dst}/images/#{year}/#{File.dirname(@filename)}/#{File.basename(@filename, ".*")}".gsub('/./', '/')
      else
        source_path = "#{src}/#{@parent}/#{@filename}".gsub('/images/', '/_images/').gsub('//', '/')
        dst_prefix = "#{dst}/#{@parent}/#{File.basename(@filename, ".*")}".gsub('//', '/')
      end
      
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
      im_format = get_format(source_path)
      
      sources = Hash.new { [] }

      image = Rszr::Image.load(source_path)
      
      if image.width < visible_width
        raise RuntimeError, "Image #{File.basename(source_path)} is only #{image.width}px wide, less than visible width #{visible_width}px"
      end
            
      for pixel_density in 1..3
        width = pixel_density * visible_width

        if image.width >= width
          for out_format in [im_format, ImageFormat::AVIF, ImageFormat::WEBP]
            out_path = "#{dst_prefix}_#{pixel_density}x#{out_format[:extension]}"
          
            if !File.exist? out_path
              open(".missing_images.json", "a") { |f|
                f.puts JSON.generate({
                  "out_path": out_path,
                  "source_path": source_path,
                  "width": width,
                  "height": (image.height * width / image.width).to_i,
                })
              }
            end

            sources[out_format] <<= "#{out_path.gsub(/_site/, '')} #{pixel_density}x"
          end
        end
      end
      
      sources
    end
    
    # Get some useful info about the file format
    def get_format(path)
      case File.extname(path)
        when ".png"
          ImageFormat::PNG
        when ".jpg"
          ImageFormat::JPEG
        else
          raise RuntimeError, "Unrecognised image extension: #{File.extname(path)}"
      end
    end
  end
end

Liquid::Template.register_tag("picture", Jekyll::PictureTag)
