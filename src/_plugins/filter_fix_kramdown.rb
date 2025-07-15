# frozen_string_literal: true

# This works around a few weirdnesses in Kramdown, where it "helpfully" adds
# a closing slash to <img> and <source> tags in my <picture> blocks,
# which get flagged as errors by HTML validators.

module Jekyll
  module FixKramdownFilters
    def fix_kramdown(html)
      cache = Jekyll::Cache.new('FixKramdown')

      cache.getset(html) do
        if html.include? '<img'
          html = html.gsub(%r{<img (src=".+[^\s])\s*/>}, '<img \1>')
        end

        if html.include? '<source'
          html = html.gsub(%r{<source (srcset=".+[^\s])\s*/>}, '<source \1>')
        end

        html
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::FixKramdownFilters)
