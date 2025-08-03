# This plugin renders a table of contents at the top of a post.
#
# Just add the following to the post:
#
#     {% table_of_contents %}
#
# The TOC appears in a coloured block, with anchor links to each of the
# <h2> or <h3> headings in the post.
#
# TODO: Detect nested headings, and indent the TOC entries accordingly.

require 'nokogiri'

module Jekyll
  class TableOfContentsTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @text = text
    end

    def render(context)
      site = context.registers[:site]
      page = context.registers[:page]

      markdown = page.content
      html = site.find_converter_instance(Jekyll::Converters::Markdown)
                 .convert(markdown)

      doc = Nokogiri::HTML5.fragment(html)

      toc_entries = []

      doc.xpath('.//h2|h3').each do |heading|
        if heading.node_name == 'h2'
          toc_entries.append({
                               'label' => heading.inner_html,
                               'id' => heading.attribute('id').value,
                               'sub_headings' => []
                             })
        elsif heading.node_name == 'h3'
          toc_entries.last['sub_headings'].append({
                                                    'label' => heading.inner_html,
                                                    'id' => heading.attribute('id').value
                                                  })
        else
          raise "Unrecognised heading level: #{heading.node_name}"
        end
      end

      tpl = Liquid::Template.parse(File.read('src/_includes/table_of_contents.html'))
      tpl.render!('toc_entries' => toc_entries)
    end
  end
end

Liquid::Template.register_tag('table_of_contents', Jekyll::TableOfContentsTag)
