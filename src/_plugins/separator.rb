# This plugin allows me to include a small SVG as an image as a separator.
#
# Example usage:
#
#     {% separator "scroll.svg" %}
#
#     {% text_separator "---" %}
#
# References:
#
#   - Accessible SVGs https://css-tricks.com/accessible-svgs/
#     Explains in more detail how to ensure accessibility is preserved with
#     inline SVGs.
#

module Jekyll
  class SeparatorTag < Liquid::Tag
    def initialize(_tag_name, name, _tokens)
      super
      @name = name.strip.tr! '"', ''
    end

    def render(context)
      site = context.registers[:site]
      src = site.config['source']

      svg_path = "#{src}/theme/_separators/#{@name}"

      svg_doc = File.open(svg_path) { |f| Nokogiri::XML(f) }

      # Quoting "Accessible SVGs" § 2:
      #
      #     On the <svg> tag add: role="img" (so that the SVG is not traversed
      #     by browsers that map the SVG to the group role)
      #
      # We omit the alt tag because this is just for decoration.
      svg_doc.root.set_attribute('role', 'img')

      # Render the minified version of the SVG in the HTML.
      svg =
        svg_doc.to_xml(indent: 0)
               .gsub('<?xml version="1.0" encoding="UTF-8"?>', '')
               .gsub('<?xml version="1.0"?>', '')
               .gsub('#000000', '#f0f0f0')  # $light-grey in the CSS
               .gsub('height="300px"', 'height="50px"')
               .gsub('width="300px"', 'width="50px"')

      "<center class='separator' aria-hidden='true'>" + svg + '</center>'
    end
  end

  class TextSeparatorTag < Liquid::Tag
    def initialize(_tag_name, name, _tokens)
      super
      @contents = name.strip.tr! '"', ''
    end

    def render(_)
      "<center class='separator' aria-hidden='true'>" + @contents + '</center>'
    end
  end
end

Liquid::Template.register_tag('separator', Jekyll::SeparatorTag)
Liquid::Template.register_tag('text_separator', Jekyll::TextSeparatorTag)
