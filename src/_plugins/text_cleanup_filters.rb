module Jekyll
  module CleanupsFilter
    def cleanup_text(input)
      # Replace mentions of RFCs with a non-breaking space version.
      text = input.gsub(/RFC (\d+)/, 'RFC&nbsp;\1')

      # Also: "part X" or "Part X"
      text = text.gsub(/([Pp]art) (\d+)/, '\1&nbsp;\2')

      # HTTP XYZ
      text = text.gsub(/HTTP (\d{3})/, 'HTTP&nbsp;\1')

      # NN minutes
      text = text.gsub(/(\d+) (second|minute|hour)/, '\1&nbsp;\2')

      text = text.sub("iPhone X", "iPhone&nbsp;X")
      text = text.sub("JPEG 2000", "JPEG&nbsp;2000")

      # Display "LaTeX" in a nice way, if you have CSS enabled
      text = text.gsub(
        "LaTeX",
        "<span class=\"latex\">L<sup>a</sup>T<sub>e</sub>X</span>"
      )

      text = text.gsub(
        "TeX",
        "<span class=\"latex\">T<sub>e</sub>X</span>"
      )

      # Replace any mention of "PyCon" with the appropriate non-breaking space
      text = text.gsub("PyCon ", "PyCon&nbsp;")

      # Get rid of the trailing space after the dollar in language-console
      # blocks.  The space is added in CSS and is unselectable.
      text = text.gsub(
        "<span class=\"gp\">$</span> ",
        "<span class=\"gp\">$</span>")

      # Make sure that footnote markers are rendered as a text
      # arrow on iOS devices, not emoji.  For more info:
      # http://daringfireball.net/linked/2015/04/22/unicode-emoji
      text = text
        .gsub("&#8617;", "&#8617;&#xFE0E;")
        .gsub("↩", "&#8617;&#xFE0E;")

      text
    end
  end
end

Liquid::Template::register_filter(Jekyll::CleanupsFilter)
