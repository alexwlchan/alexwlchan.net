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

require_relative 'utils/markdownify_oneline'

module Jekyll
  module MarkdownifyOnlineFilter
    def cache
      @@cache ||= Jekyll::Cache.new('MarkdownifyOnline')
    end

    def markdownify_oneline(input)
      if input.nil?
        nil
      else
        cache.getset(input) do
          site = @context.registers[:site]
          apply_markdownify_oneline(site, input)
        end
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::MarkdownifyOnlineFilter)
