require 'htmlcompressor'

module Jekyll
  module CompressHtmlFilter
    def compress_html(html)
      cache = Jekyll::Cache.new('CompressHtml')

      cache.getset(html) do
        compressor = HtmlCompressor::Compressor.new({
          :compress_css => true,
          :css_compressor => CssCompressor.new(@context),
        })
        compressor.compress(html)
      end
    end
  end
end

# Use the Sass library to compress a block of CSS.
#
# In practice, this is only compressing the tint color variables
# in the <head> of the page, because all other inline <style> blocks
# are already being compressed -- but it doesn't hurt!
class CssCompressor
  def initialize(context)
    site = context.registers[:site]
    @converter = site.find_converter_instance(Jekyll::Converters::Scss)
  end
  
  def compress(source)
    @converter.convert(source)
  end
end

Liquid::Template.register_filter(Jekyll::CompressHtmlFilter) if defined? Liquid
