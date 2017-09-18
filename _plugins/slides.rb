# This is a plugin for embedding slide images.
#
# Each image needs to be both an image, and a link to the fullsized image.
#
# To embed a slide, place a Liquid tag of the following form anywhere in a
# source file:
#
#     {% slide docopt 1 %}
#


module Jekyll
  class SlideTag < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @deck = text.split(" ").first
      @number = text.split(" ").last.to_i
    end

    def render(context)
      path = "/slides/#{@deck}/#{@deck}.#{@number.to_s.rjust(3, '0')}.png"
<<-EOT
<figure class="slide">
  <a href="#{path}"><img src="#{path}"></a>
</figure>
EOT
    end
  end
end

Liquid::Template.register_tag('slide', Jekyll::SlideTag)
