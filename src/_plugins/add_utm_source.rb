# frozen_string_literal: true

require_relative 'utils/add_utm_source'

module Jekyll
  module AddUtmSourceFilter
    def add_utm_source(url)
      add_utm_source_to_url(url)
    end
  end
end

Liquid::Template.register_filter(Jekyll::AddUtmSourceFilter)
