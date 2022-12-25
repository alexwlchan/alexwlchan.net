require 'rszr'
require 'shellwords'

module Jekyll
  class PictureTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      # First parse the params string, which is designed to be written
      # with a similar syntax to HTML attributes, e.g.
      #
      #     {% picture src="IMG_5744.jpg" alt="A black steam engine" %}
      #
      @attrs = {}
      params_string.scan(/(?<key>[a-z_]+)(="(?<value>[^"]+)")?/).each { |k, v|
        @attrs[k] = v
      }
      
      # Now extract a couple of parameters that are required.  This will
      # leave the `@attrs` dict as just containing any extras.
      @src = @attrs.delete("src")
      if @src.nil?
        raise SyntaxError, "Error in `picture` tag: missing required `src` parameter"
      end
      
      @alt = @attrs.delete("alt")
      if @alt.nil?
        raise SyntaxError, "Error in `picture` tag: missing required `alt` parameter"
      end
      
      @target_width = @attrs.delete("target_width").gsub(/px/, '').to_i
      if @target_width.nil?
        raise SyntaxError, "Error in `picture` tag: missing required `target_width` parameter"
      end
      
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

      source_path = "#{src}/_images/#{year}/#{@src}"
      dst_prefix = "#{dst}/images/#{year}/#{File.basename(@src, ".*")}"
      
      sources = prepare_images(source_path, dst_prefix, @target_width)
      
      im_format = get_format(source_path)
      
      inner_html = <<-EOF
<picture>
  <source
    srcset="#{sources["image/webp"].join(",\n            ")}"
    type="image/webp"
  >
  <source
    srcset="#{sources[im_format[:mime_type]].join(",\n            ")}"
    type="#{im_format[:mime_type]}"
  >
  <img
    src="#{sources[im_format[:mime_type]][0].gsub(" 1x", "")}"
    alt="#{@alt}"
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
    
    def prepare_images(source_path, dst_prefix, target_width)
      image_width = get_width(source_path)
      im_format = get_format(source_path)
      
      sources = Hash.new { [] }
      
      for pixel_density in 1..4
        width = pixel_density * target_width

        if image_width >= width
          out_path = "#{dst_prefix}_#{pixel_density}x#{im_format[:extension]}"
          
          if !File.exist? out_path || File.mtime(out_path) < File.mtime(source_path)
            `convert #{Shellwords.escape(source_path)} -resize #{width}x #{Shellwords.escape(out_path)}`
          end

          sources[im_format[:mime_type]] <<= "#{out_path.gsub(/_site/, '')} #{pixel_density}x"

          webp_path = "#{dst_prefix}_#{pixel_density}x.webp"
          
          if !File.exist? webp_path || File.mtime(webp_path) < File.mtime(source_path)
            `convert #{Shellwords.escape(source_path)} -resize #{width}x #{Shellwords.escape(webp_path)}`
          end

          sources["image/webp"] <<= "#{webp_path.gsub(/_site/, '')} #{pixel_density}x"
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
          {:extension => ".png", :mime_type => "image/png", :label => "PNG"}
        when ".jpeg", ".jpg"
          {:extension => ".jpg", :mime_type => "image/jpeg", :label => "JPEG"}
        else
          raise Error, "Unrecognised image extension: #{File.extname(path)}"
      end
    end
  end
end

Liquid::Template.register_tag("picture", Jekyll::PictureTag)
