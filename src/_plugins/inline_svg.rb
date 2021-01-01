# This plugin allows me to inline the contents of an SVG from a separate file.
#
# I inline small SVG images (anything ~1 KB or less) to reduce the overhead
# of extra HTTP requests.  I don't inline them directly in the Markdown source
# because it's easier for my development flow if they're kept in separate files.
#
# Example usage:
#
#     {% inline_svg "_images/2020/sqs_queue_worker.svg" %}
#
# References:
#
#   - Accessible SVGs https://css-tricks.com/accessible-svgs/
#     Explains in more detail how to ensure accessibility is preserved with
#     inline SVGs.
#
#   - sdumetz/jekyll-inline-svg https://github.com/sdumetz/jekyll-inline-svg
#     Jekyll plugin for doing something similar; I'm not using it because it's
#     pinned to Jekyll 3.3, and I'm using 4.x.
#

require "nokogiri"

module Jekyll
  class InlineSvgTag < Liquid::Tag
    def initialize(_tag_name, path, _tokens)
      super
      @path = path.strip.tr! '"', ''
    end

    def render(context)
      site = context.registers[:site]
      src = site.config["source"]

      svg_path = "#{src}/#{@path}"

      svg_doc = File.open(svg_path) { |f| Nokogiri::XML(f) }

      # Quoting "Accessible SVGs" § 2:
      #
      #     On the <svg> tag add: role="img" (so that the SVG is not traversed
      #     by browsers that map the SVG to the group role)
      #
      svg_doc.root.set_attribute("role", "img")

      # Look for the <title> element inside the SVG.  This will be used as
      # the alt text; if there isn't one, error out.
      #
      # COULDDO: It should be possible to do this using ``.at_xpath("//title")``,
      # but that returns nil when I tried it.
      titles = svg_doc.root
        .children
        .select { |child| child.name == "title" }

      raise "Unable to find <title> in #{@path}" unless titles.size == 1

      title_element = titles[0]

      # Add an ID to the title element, and the appropriate aria-labelledby
      # attribute to the root.
      svg_doc_id = "svg_#{File.basename(svg_path, ".svg")}"

      title_element.set_attribute("id", svg_doc_id)
      svg_doc.root.set_attribute("aria-labelledby", svg_doc_id)

      # Render the minified version of the SVG in the HTML.
      svg_doc.to_xml(indent: 0)
    end
  end
end

Liquid::Template.register_tag("inline_svg", Jekyll::InlineSvgTag)
