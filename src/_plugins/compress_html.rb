require 'htmlcompressor'

module Jekyll
  module CompressHtmlFilter
    def compress_html(html)
      cache = Jekyll::Cache.new('CompressHtml')

      cache.getset(html) do
        # The syntax highlighter adds a couple of classes to my HTML,
        # but I don't have any CSS that targets those classes.
        #
        # Removing them reduces the size of the final HTML, especially
        # in the TIL index.
        #
        # The one class I leave behind is `language-console`, which I
        # have some special styles for.
        html = html.gsub(' class="language-console highlighter-rouge"', 'class="language-console"')
        html = html.gsub(/ class="language\-[a-z]+ highlighter\-rouge"/, '')

        compressor = HtmlCompressor::Compressor.new
        html = compressor.compress(html)

        html
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CompressHtmlFilter) if defined? Liquid
