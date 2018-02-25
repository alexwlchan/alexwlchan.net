# Various text cleanups.

module Jekyll
  module CleanupsFilter
    def cleanup_text(input)
      # Replace mentions of RFCs with a non-breaking space version.
      text = input.gsub(/RFC (\d+)/, 'RFC&nbsp;\1')

      # Display "LaTeX" in a nice way, if you have CSS enabled
      text = text.gsub(
        "LaTeX",
        "<span class=\"latex\">L<sup>a</sup>T<sub>e</sub>X</span>")

      text
    end
  end
end

Liquid::Template::register_filter(Jekyll::CleanupsFilter)
