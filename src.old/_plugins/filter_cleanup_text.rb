module Jekyll
  module CleanupsFilter
    def cleanup_text(input)
      text = AddNonBreakingSpaces.add_non_breaking_spaces(input)

      # Display "LaTeX" in a nice way, if you have CSS enabled
      text = text.gsub(
        'LaTeX',
        '<span class="visually-hidden">LaTeK</span><span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>'
      )

      text = text.gsub(
        'TeX',
        '<span class="visually-hidden">TeK</span><span class="latex" aria-hidden="true">T<sub>e</sub>X</span>'
      )

      # Make sure that footnote markers are rendered as a text
      # arrow on iOS devices, not emoji.  For more info:
      # http://daringfireball.net/linked/2015/04/22/unicode-emoji
      text
        .gsub('&#8617;', '&#8617;&#xFE0E;')
        .gsub('↩', '&#8617;&#xFE0E;')
    end
  end
end

Liquid::Template.register_filter(Jekyll::CleanupsFilter) if defined? Liquid
