require_relative "alexwlchan_base"


def render_slide(deck, slide, alt_text, caption_text)
  path = get_slide_path(deck, slide)

  md_content = caption_text.strip
  caption = if md_content
     "<figcaption>#{markdown_converter.convert(md_content)}</figcaption>"
  else
    ""
  end

<<-EOT
<figure class="slide">
<a href="#{path}"><img src="#{path}" alt="#{alt_text}" title="#{alt_text}"></a>
#{caption}
</figure>
EOT
end


module Jekyll

  module SlideBase
    def bind_params(params)
      @deck = params[:deck] or raise SyntaxError, "Error in tag 'better_slide', :deck parameter is required"
      @slide = params[:slide] or raise SyntaxError, "Error in tag 'better_slide', :slide parameter is required"
      @alt = params[:alt] or raise SyntaxError, "Error in tag 'better_slide', :alt parameter is required"
    end
  end

  class BetterSlideBlock < Alexwlchan::Block
    include SlideBase

    def internal_render
      render_slide(@deck, @slide, @alt, @text)
    end
  end

  class BetterSlideTag < Alexwlchan::Tag
    include SlideBase

    def internal_render
      render_slide(@deck, @slide, @alt, "")
    end
  end
end


Liquid::Template.register_tag("better_slide", Jekyll::BetterSlideBlock)
Liquid::Template.register_tag("slide_image", Jekyll::BetterSlideTag)



# This is a plugin for embedding slide images.
#
# Each image needs to be both an image, and a link to the fullsized image.
#
# To embed a slide, place a Liquid tag of the following form anywhere in a
# source file:
#
#     {% slide docopt 1 %}
#
# You can also use slide_captioned if you want a <figcaption> on the slide
# (e.g. to add image attribution):
#
#     {% slide_captioned docopt 2 %}
#       This slide uses an image from https://example.org/
#     {% endslide_captioned %}
#

module Jekyll
  class SlideTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @deck = text.split(" ").first
      @number = text.split(" ").last.to_i


    end

    def render(context)
      path = get_slide_path(@deck, @number)

<<-EOT
<figure class="slide">
  <a href="#{path}"><img src="#{path}"></a>
</figure>
EOT
    end
  end

  class CaptionedSlideBlock < Liquid::Block
    def initialize(tag_name, text, tokens)
      @deck = text.split(" ").first
      @number = text.split(" ").last.to_i
      super
    end

    def render(context)
      site = context.registers[:site]
      converter = site.find_converter_instance(::Jekyll::Converters::Markdown)

      md_content = super.strip
      html_content = converter.convert(md_content)

      path = get_slide_path(@deck, @number)

<<-EOT
<figure class="slide">
  <a href="#{path}"><img src="#{path}"></a>
  <figcaption>#{html_content}</figcaption>
</figure>
EOT
    end
  end
end

Liquid::Template.register_tag('slide', Jekyll::SlideTag)
Liquid::Template.register_tag("slide_captioned", Jekyll::CaptionedSlideBlock)


# Slides can be rendered as either PNG or JPEG (depending on whether
# they're text heavy or image heavy) -- this helps keep the file size
# of the page down.
#
# Rather than requiring the user to specify the file format in the
# page, we look to see which file exists.  To save doing lots of
# OS calls to check for file existence, we grab every image file
# in the slides directory upfront.
#
# NOTE: we don't have access to the 'site' context here, so I'm
# hard-coding the source directory.
$src = "src"


def rebuild_slide_files
  $slide_files = Dir["#{$src}/_slides/**/*"].map {
    |f| f.sub("#{$src}/_slides/", "")
  }
end


rebuild_slide_files()


def get_slide_path(deck_name, slide_number)
  name = "#{deck_name}/#{deck_name}.#{slide_number.to_s.rjust(3, '0')}"

  path = if $slide_files.include? "#{name}.png"
    "/slides/#{name}.png"
  elsif $slide_files.include? "#{name}.jpeg"
    "/slides/#{name}.jpeg"
  elsif $slide_files.include? "#{name}.jpg"
    "/slides/#{name}.jpg"
  else
    rebuild_slide_files()
    raise RuntimeError, "Unable to find slide for #{name}"
  end
end
