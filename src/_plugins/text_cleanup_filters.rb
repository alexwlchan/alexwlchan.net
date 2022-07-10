module Jekyll
  module Filters

    # Convert quotes into smart quotes.
    #
    # input - The String to convert.
    #
    # Returns the smart-quotified String.
    #
    # This is an override for the builtin Jekyll filter that caches results,
    # because I call this function in lots of places, and that means calling
    # it with the same inputs repeatedly.
    #
    # See https://github.com/jekyll/jekyll/blob/4fbbefeb7eecff17d877f14ee15cbf8b87a52a6e/lib/jekyll/filters.rb#L22-L31
    SMARTIFY_CACHE = {}

    def smartify(input)
      SMARTIFY_CACHE.fetch(input) { |input|
        SMARTIFY_CACHE[input] =
          @context.registers[:site]
            .find_converter_instance(Jekyll::Converters::SmartyPants)
            .convert(input.to_s)
      }
    end
  end

  module CleanupsFilter
    CLEANUP_TEXT_CACHE = {}

    def cleanup_text(input)
      CLEANUP_TEXT_CACHE.fetch(input) { |input|
        CLEANUP_TEXT_CACHE[input] = _do_cleanup_text(input)
      }
    end

    def _do_cleanup_text(input)

      # Replace mentions of RFCs with a non-breaking space version.
      text = input.gsub(/RFC (\d+)/, 'RFC&nbsp;\1')

      # Also: "part X", "Part X", "season X"
      text = text.gsub(/([Pp]art) (\d+)/, '\1&nbsp;\2')
      text = text.gsub(/([Ss]eason) (\d+)/, '\1&nbsp;\2')

      # HTTP XYZ
      text = text.gsub(/HTTP (\d{3})/, 'HTTP&nbsp;\1')

      # NN minutes
      text = text.gsub(/(\d+) (second|minute|hour)/, '\1&nbsp;\2')

      text = text.gsub(/Apollo (\d{3})/, 'Apollo&nbsp;\1')
      text = text.sub("iPhone X", "iPhone&nbsp;X")
      text = text.sub("JPEG 2000", "JPEG&nbsp;2000")
      text = text.sub("Route 53", "Route&nbsp;53")

      # e.g. k-means
      text = text.sub("<em>k</em>-means", "<em>k</em>&#8209;means")

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
