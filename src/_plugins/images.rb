require_relative "alexwlchan_base"
require_relative "html_tag_builder"

include ::HtmlTagBuilder::Helper


def render_image(href:, **attrs)
  tag.a(href: href) do |inner|
    inner.tag("img", **attrs)
  end
end


module Jekyll
  class PostImageTag < Alexwlchan::Tag
    def bind_params(params)
      @params = params
      params[:filename] or raise SyntaxError, "Error in tag 'image', :filename parameter is required"
      params[:alt] or raise SyntaxError, "Error in tag 'image', :alt parameter is required"
    end

    def find_matching_images(year, filename)
      base, ext = filename.split(".")
      source = @context.registers[:site].config["source"]

      # Find all the images that have the same name or have a _1x, _2x, _3x etc.
      # suffix that suggest different sizes.
      Dir["#{source}/_images/#{year}/#{base}*"]
        .map { |path| path.split("/")[-1] }
        .select { |f|
          f_base, _ = f.split(".")
          f_base == base || f_base =~ /_\dx$/
        }
    end

    def build_url(filename)
      "/images/#{@context.registers[:page]["date"].year}/#{filename.split("/")[-1]}"
    end

    def internal_render
      attrs = @params
      filename = attrs.delete(:filename)

      files = find_matching_images(@context.registers[:page]["date"].year, filename)

      # This block decides what we use as the src and srcset.  If there's only
      # image, that's what we use.  If there are multiple sizes (_1x, _2x, _3x),
      # we set a `srcset` attribute to allow high-res screens to get better images.
      if files.size == 0
        raise SyntaxError, "Cannot find file for #{filename}"
      elsif files.size == 1
        attrs[:src] = build_url(files[0])
        href = attrs[:src]
      else
        srcset = []
        files.each { |f|
          scaling = f.split("_")[-1].split(".")[0]
          if scaling =~ /^\dx$/
            srcset << "#{f} #{scaling}"
          end
        }
        srcset = srcset.sort

        # Display the smallest image by default, but link to the biggest one.
        attrs[:src] = build_url(srcset[0].split(" ")[0])
        href = build_url(srcset[-1].split(" ")[0])
        attrs[:srcset] = srcset.map { |f| build_url(f) }.join(", ")
      end

      render_image(href: href, **attrs)
    end
  end
end


Liquid::Template.register_tag("image", Jekyll::PostImageTag)
