# frozen_string_literal: true

# This takes a JSON string and removes any unnecessary whitespace.

require 'json'

module Jekyll
  module CompactJsonFilter
    def compact_json(json_string)
      json = JSON.parse(json_string)
      JSON.dump(json)
    end
  end
end

Liquid::Template.register_filter(Jekyll::CompactJsonFilter)
