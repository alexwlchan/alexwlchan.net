# Replaces <hr> instances with a slightly prettier version.
#
# Based on https://www.sarasoueidan.com/blog/horizontal-rules/

module Jekyll
  module HorizontalRuleFilters
    def pretty_hr(input)
      separator = <<~HTML
        <svg viewBox="0 0 17 1" width="100px" role="separator">
          <rect        width="1" height="1"/>
          <rect x="4"  width="1" height="1"/>
          <rect x="8"  width="1" height="1"/>
          <rect x="12" width="1" height="1"/>
          <rect x="16" width="1" height="1"/>
        </svg>
      HTML

      input.gsub(%r{<hr\s*/>}, separator)
    end
  end
end

Liquid::Template.register_filter(Jekyll::HorizontalRuleFilters)
