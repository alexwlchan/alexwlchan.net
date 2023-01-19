# Render a single line of text as Markdown.
#
# This is used to render HTML in post titles and page descriptions.
# Unlike Jekyll's `markdownify` filter, this won't wrap the output
# in paragraph <p> tags.
#
# == Example ==
#
#     {{ "Five *shocking* facts" | markdownify }}
#     <p>Five <em>shocking</em> facts</p>
#
#     {{ "Five" *shocking* facts | markdownify_oneline }}
#     Five <em>shocking</em> facts
#

module Jekyll
  module MarkdownifyOnlineFilter
    def cache
      @@cache ||= Jekyll::Cache.new('MarkdownifyOnline')
    end

    def markdownify_oneline(input)
      cache.getset(input) do
        @context.registers[:site]
                .find_converter_instance(Jekyll::Converters::Markdown)
                .convert(input)
                .sub('<p>', '')
                .sub('</p>', '')
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::MarkdownifyOnlineFilter)
