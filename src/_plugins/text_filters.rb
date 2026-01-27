require 'json'
require_relative 'utils/text'

module Jekyll
  module TextFilters
    # Convert Markdown text into HTML.
    def markdownify(input)
      Jekyll::Cache.new('Markdownify').getset(input) do
        site = @context.registers[:site]
        Alexwlchan::TextUtils.markdownify(site, input)
      end
    end

    # Convert a single line of Markdown text into HTML.
    def markdownify_oneline(input)
      Jekyll::Cache.new('Markdownify').getset(input) do
        site = @context.registers[:site]
        Alexwlchan::TextUtils.markdownify_oneline(site, input)
      end
    end

    # Minify a JSON string, removing any unnecessary whitespace.
    def minify_json(json_string)
      json = JSON.parse(json_string)
      JSON.dump(json)
    end

    # Apply cleanup rules to text, e.g. non-breaking characters and
    # extra CSS classes.
    def cleanup_text(input)
      cache = Jekyll::Cache.new('CleanupText')

      cache.getset(input) do
        text = Alexwlchan::TextUtils.add_non_breaking_characters(input)
        text = Alexwlchan::TextUtils.cleanup_syntax_highlighter_classes(text)
        text = Alexwlchan::TextUtils.add_latex_css_classes(text)
        text = Alexwlchan::TextUtils.force_text_footnote_markers(text)

        # Clean up the `n0` pseudo-class added by the code highlighting plugin.
        text = text.gsub(%r{<span class="n0">([^>]+)</span>}, '\\1')

        text.strip
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::TextFilters)
