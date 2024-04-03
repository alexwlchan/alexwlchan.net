# frozen_string_literal: true

#
# Replaces <hr> instances with a slightly prettier version.
#
# Based on https://www.sarasoueidan.com/blog/horizontal-rules/

SEPARATOR = <<~HTML
  <svg viewBox="0 0 17 1" width="100px" role="separator">
    <rect        width="1" height="1"/>
    <rect x="4"  width="1" height="1"/>
    <rect x="8"  width="1" height="1"/>
    <rect x="12" width="1" height="1"/>
    <rect x="16" width="1" height="1"/>
  </svg>
HTML

module Jekyll
  module HorizontalRuleFilters
    def pretty_hr(html)
      cache = Jekyll::Cache.new('HorizontalRule')

      cache.getset(html) do
        html.gsub(%r{<hr\s*/?>}, SEPARATOR)
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::HorizontalRuleFilters)
