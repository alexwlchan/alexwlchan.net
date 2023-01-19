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
  module MarkdownFilter
    MARKDOWNIFY_ONELINE_CACHE = {}

    def markdownify_oneline(input)
      MARKDOWNIFY_ONELINE_CACHE.fetch(input) do |input|
        MARKDOWNIFY_ONELINE_CACHE[input] =
          @context.registers[:site]
                  .find_converter_instance(::Jekyll::Converters::Markdown)
                  .convert(input)
                  .sub('<p>', '')
                  .sub('</p>', '')
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::MarkdownFilter)
