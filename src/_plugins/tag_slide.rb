# Creates a <picture> tag for slides in blog posts.
#
# This uses my {% picture %} tag, which is defined by another plugin --
# it gets wrapped in some presets and common values.  It reuses the logic
# from that plugin to create smaller sizes/formats to reduce page weight.
#
# == Example ==
#
# This is how to use the tag:
#
#     {%
#       slide
#       filename="slide82.png"
#       alt="A screenshot of a messaging app."
#       caption="Image from Pexels, CC0"
#     %}
#
# It looks for the image in a subdirectory of `_images` based on the
# year and slug of the post, e.g. if this is a 2018 post `anti-social-media`,
# then it looks for the image in `_images/2018/anti-social-media/slide82.png`
#
# The `caption` field is optional, and displays below the image.  It's useful
# for attribution or sourcing that doesn't fit on the slide.

require_relative 'utils/attrs'

module Jekyll
  class SlideTag < Liquid::Tag
    def initialize(_tag_name, params_string, _tokens)
      super

      @attrs = parse_attrs(params_string)
      @filename = get_required_attribute(@attrs, { tag: 'slide_image', attribute: 'filename' })
      @caption = @attrs.delete('caption')
    end

    def render(context)
      deck = context.registers[:page]['slug']
      extra_attributes = @attrs.map { |k, v| "#{k}=\"#{v}\"" }.join(' ')

      markdown_converter = context.registers[:site].find_converter_instance(::Jekyll::Converters::Markdown)

      caption = if @caption.nil?
                  ''
                else
                  "<figcaption>#{markdown_converter.convert(@caption)}</figcaption>"
                end

      input = <<~HTML
        <style type="x-text/scss">
          @use "components/slides";
        </style>
        <figure class="slide">
          {%
            picture
            filename="#{deck}/#{@filename}"
            width="450"
            loading="lazy"
            link_to="original"
            #{extra_attributes}
          %}
          #{caption}
        </figure>
      HTML

      Liquid::Template.parse(input).render!(context)
    end
  end
end

Liquid::Template.register_tag('slide', Jekyll::SlideTag)
