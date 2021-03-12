# This plugin allows me to include a small SVG as an image as a separator.
#
# Example usage:
#
#     {% separator "scroll.svg" %}
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
      src = site.config["source"]

      svg_path = "#{src}/theme/_separators/#{@name}"

      svg_doc = File.open(svg_path) { |f| Nokogiri::XML(f) }

      # Quoting "Accessible SVGs" § 2:
      #
      #     On the <svg> tag add: role="img" (so that the SVG is not traversed
      #     by browsers that map the SVG to the group role)
      #
      # We omit the alt tag because this is just for decoration.
      svg_doc.root.set_attribute("role", "img")

      # Render the minified version of the SVG in the HTML.
      "<center class='separator'>" + svg_doc.to_xml(indent: 0) + "</center>"
    end
  end
end

Liquid::Template.register_tag("separator", Jekyll::SeparatorTag)
