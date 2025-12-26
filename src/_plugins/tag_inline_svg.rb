# This plugin allows me to inline the contents of an SVG from a separate file.
#
# I inline small SVG images (anything ~1 KB or less) to reduce the overhead
# of extra HTTP requests.  I don't inline them directly in the Markdown source
# because it's easier for my development flow if they're kept in separate files.
#
# Example usage:
#
#     {%
#       inline_svg
#       filename="sqs_queue_worker.svg"
#       alt="Three boxes joined by arrows"
#     %}
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

require 'fileutils'

require 'nokogiri'

require_relative 'utils/attrs'

def get_inline_svg(svg_path, alt_text, extra_attrs, dst_path)
  # This plugin only works with SVG source files -- check that's what
  # we're using, and that we haven't inadvertently copy/pasted
  # a raster image into this plugin.
  unless svg_path.end_with? '.svg'
    raise "You can only use {% inline_svg %} with SVG images; got #{svg_path}"
  end

  svg_doc = File.open(svg_path) { |f| Nokogiri::XML(f) }

  # Quoting "Accessible SVGs" § 2:
  #
  #     On the <svg> tag add: role="img" (so that the SVG is not traversed
  #     by browsers that map the SVG to the group role)
  #
  svg_doc.root.set_attribute('role', 'img')

  # Insert a title element in the SVG with the alt text.
  unless alt_text.nil?
    title = Nokogiri::XML::Node.new('title', svg_doc)
    title.content = alt_text

    # Add an ID to the title element, and the appropriate aria-labelledby
    # attribute to the root.
    svg_doc_id = "svg_#{File.basename(svg_path, '.svg')}"
    title.set_attribute('id', svg_doc_id)
    svg_doc.root.set_attribute('aria-labelledby', svg_doc_id)

    svg_doc.at('svg').add_child(title)
  end

  # Add any extra attributes on the SVG
  extra_attrs.each do |k, v|
    if k == 'class'
      svg_doc.root.append_class(v)
    else
      svg_doc.root.set_attribute(k, v)
    end
  end

  # Remove all the comments, they're not needed
  svg_doc.xpath('//comment()').remove

  # Render the minified version of the SVG in the HTML.
  xml = svg_doc
        .to_xml(indent: 0)
        .gsub('<?xml version="1.0" encoding="UTF-8"?>', '')
        .gsub('<?xml version="1.0"?>', '')
        .gsub('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '')

  # If we're told where this SVG should be linking to, create a link,
  # otherwise drop the XML directly into the page.
  if dst_path.nil?
    xml
  else
    "<a href=\"#{dst_path}\">#{xml}</a>"
  end
end

module Jekyll
  class InlineSvgTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      @attrs = parse_attrs(params_string)

      @filename = get_required_attribute(
        @attrs, { tag: 'inline_svg', attribute: 'filename' }
      )
    end

    def render(context)
      site = context.registers[:site]
      src = site.config['source']
      dst = site.config['destination']

      year = context.registers[:page]['date'].year

      src_path = "#{src}/_images/#{year}/#{@filename}"
      alt_text = @attrs.delete('alt')

      link_to_original = @attrs.delete('link_to') == 'original'

      if link_to_original
        dst_path = "/images/#{year}/#{@filename}"
        FileUtils.cp(src_path, "#{dst}#{dst_path}")
      else
        dst_path = nil
      end

      get_inline_svg(src_path, alt_text, @attrs, dst_path)
    end
  end
end

Liquid::Template.register_tag('inline_svg', Jekyll::InlineSvgTag)
