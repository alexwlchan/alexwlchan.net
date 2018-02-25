# Various text cleanups.

module Jekyll
  module CleanupsFilter
    def cleanup_text(input)
      # Replace mentions of RFCs with a non-breaking space version.
      text = input.gsub(/RFC (\d+)/, 'RFC&nbsp;\1')

      text
    end
  end
end

Liquid::Template::register_filter(Jekyll::CleanupsFilter)
