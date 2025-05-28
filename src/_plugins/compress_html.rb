require 'htmlcompressor'

module Jekyll
  module CompressHtmlFilter
    def compress_html(html)
      cache = Jekyll::Cache.new('CompressHtml')

      cache.getset(html) do
        # The syntax highlighter will add these classes to my HTML
        # by default, but these are unstyled code blocks -- I don't
        # need the classes.  Removing them reduces the size of the
        # final HTML, especially in the TIL index.
        html = html.gsub('<code class="language-plaintext highlighter-rouge">', '<code>')

        compressor = HtmlCompressor::Compressor.new
        html = compressor.compress(html)

        html
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CompressHtmlFilter) if defined? Liquid
