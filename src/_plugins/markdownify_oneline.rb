# Render a single line of text as Markdown.
#
# This is used to render HTML in post titles and page descriptions.
# Unlike Jekyll's `markdownify` filter, this won't wrap the output
# in paragraph <p> tags.
#
# Note that `markdownify` will also run SmartyPants to do smart quotes
# and the like, so calling `markdownify_oneline | smartify` is redundant.
#
# == Example ==
#
#     {{ "Five *shocking* facts" | markdownify }}
#     <p>Five <em>shocking</em> facts</p>
#
#     {{ "Five" *shocking* facts | markdownify_oneline }}
#     Five <em>shocking</em> facts
#
#     {{ "Isn't this nice" | markdownify_oneline }}
#     Isn’t this nice
#

module Jekyll
  module MarkdownifyOnlineFilter
    def markdownify_oneline(input)
      cache = Jekyll::Cache.new('MarkdownifyOnline')

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
