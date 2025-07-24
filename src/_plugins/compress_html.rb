require 'minify_html'

def run_compress_html(html)
  options = {
    keep_html_and_head_opening_tags: true,
    keep_closing_tags: true,
    minify_css: true,
    minify_js: true
  }

  minify_html(html, options)
end

module Jekyll
  module CompressHtmlFilter
    def compress_html(html)
      cache = Jekyll::Cache.new('CompressHtml')

      cache.getset(html) do
        run_compress_html(html)
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CompressHtmlFilter) if defined? Liquid
