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
      src = "src"

      @files = Dir["#{src}/_slides/**/*"].map {
        |f| f.sub("#{src}/_slides/", "")
      }
    end

    def render(context)
      name = "#{@deck}/#{@deck}.#{@number.to_s.rjust(3, '0')}"

      path = if @files.include? "#{name}.png"
        "/slides/#{name}.png"
      elsif @files.include? "#{name}.jpeg"
        "/slides/#{name}.jpeg"
      elsif @files.include? "#{name}.jpg"
        "/slides/#{name}.jpg"
      else
        raise RuntimeError, "Unable to find slide for #{name}"
      end

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

      path = "/slides/#{@deck}/#{@deck}.#{@number.to_s.rjust(3, '0')}.png"

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
