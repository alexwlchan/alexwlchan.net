require 'minify_html'

module Jekyll
  module CompressHtmlFilter
    def compress_html(html)
      cache = Jekyll::Cache.new('CompressHtml')

      cache.getset(html) do
        minify_html(html, { minify_css: true, minify_js: true })
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CompressHtmlFilter) if defined? Liquid
