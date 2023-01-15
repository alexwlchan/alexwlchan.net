# Provides a filter that "cleans up" text.
#
# In particular this inserts HTML entities to prevent text wrapping
# in unfortunate places.  e.g. 'RFC 1234' becomes 'RFC&nbsp;1234'
# Doing this in a global filter means:
#
#   1.  These rules are applied consistently
#   2.  I don't have to litter my Markdown source with non-breaking
#       HTML entities
#
# See: https://alexwlchan.net/2020/adding-non-breaking-spaces-with-jekyll/

module Jekyll
  module CleanupsFilter
    CLEANUP_TEXT_CACHE = {}

    def cleanup_text(input)
      CLEANUP_TEXT_CACHE.fetch(input) do |input|
        CLEANUP_TEXT_CACHE[input] = _do_cleanup_text(input)
      end
    end

    def _do_cleanup_text(input)
      text = input

      # Add a non-breaking space after words which are followed by
      # a number, e.g. 'Apollo 11' or 'RFC 456'
      prefix_words = %w[
        Apollo
        HTTP
        ImageMagick
        issue
        RFC
        Part
        part
        Season
        season
      ]

      prefix_words.each do |w|
        text = text.gsub(/#{w} (\d+)/, "#{w}&nbsp;" + '\1')
      end

      # Add a non-breaking space after words which are preceded by
      # a number, e.g. '1 second' or '5 bytes'
      countable_words = %w[
        second
        minute
        hour
        character
        byte
      ]

      countable_words.each do |w|
        text = text.gsub(/(\d+) #{w}/, '\1' + "&nbsp;#{w}")
      end

      # Other phrases which needed non-breaking spaces or non-breaking
      # dashes.
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
        'P-215',
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
