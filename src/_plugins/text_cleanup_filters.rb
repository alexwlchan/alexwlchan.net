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
      SMARTIFY_CACHE.fetch(input) do |input|
        SMARTIFY_CACHE[input] =
          @context.registers[:site]
                  .find_converter_instance(Jekyll::Converters::SmartyPants)
                  .convert(input.to_s)
      end
    end
  end

  module CleanupsFilter
    CLEANUP_TEXT_CACHE = {}

    def cleanup_text(input)
      CLEANUP_TEXT_CACHE.fetch(input) do |input|
        CLEANUP_TEXT_CACHE[input] = _do_cleanup_text(input)
      end
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

      text = text.gsub(/issue (\d+)/, 'issue&nbsp;\1')
      text = text.gsub(/Apollo (\d{3})/, 'Apollo&nbsp;\1')

      text = text.gsub("P-215", "P&#8209;215")

      phrases = [
        '<em>k</em>-means',
        'Artemis 1',
        'CC BY 4.0',
        'CC BY',
        'CC BY-NC 4.0',
        'CC BY-NC-ND',
        'CC BY-SA 2.0',
        'CC BY-SA 4.0',
        'iMac G3',
        'iPhone X',
        'JPEG 2000',
        'Mac OS 9',
        'PyCon ',
        'Route 53'
      ]

      phrases.each do |p|
        replacement = p.gsub(' ', '&nbsp;').gsub('-', '&#8209;')
        text = text.gsub(p, replacement)
      end

      # Display "LaTeX" in a nice way, if you have CSS enabled
      text = text.gsub(
        'LaTeX',
        '<span class="latex">L<sup>a</sup>T<sub>e</sub>X</span>'
      )

      text = text.gsub(
        'TeX',
        '<span class="latex">T<sub>e</sub>X</span>'
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

Liquid::Template.register_filter(Jekyll::CleanupsFilter)
