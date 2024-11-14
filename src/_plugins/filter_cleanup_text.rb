# frozen_string_literal: true

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

class AddNonBreakingSpaces
  def self.add_non_breaking_spaces(input)
    text = input

    # "e.g." introduces an example; it's annoying when the example text has
    # been bumped to another line, so don't let it.
    text.gsub('e.g. ', 'e.g.&nbsp;')

    # Add a non-breaking space after words which are followed by
    # a number, e.g. 'Apollo 11' or 'RFC 456'
    prefix_words = %w[
      Apollo
      Artemis
      HTTP
      ImageMagick
      Issue
      issue
      Part
      part
      RFC
      Safari
      Season
      season
    ].join('|')

    text = text.gsub(/(#{prefix_words}) (\d+)/, '\1&nbsp;\2')

    # Add a non-breaking space after words which are preceded by
    # a number, e.g. '1 second' or '5 bytes'
    countable_words = %w[
      bookmark
      byte
      character
      count
      hour
      inch
      kilometre
      line
      million
      minute
      second
      tags
      unit
      vote
      year
    ].join('|')

    text = text.gsub(/(\d+) (#{countable_words})/, '\1&nbsp;\2')

    # Other phrases which needed non-breaking spaces or non-breaking
    # dashes.
    phrases = [
      '<em>k</em>-means',
      '26k items',
      'CC0 1.0',
      'CC BY 2.0',
      'CC BY 3.0',
      'CC BY 4.0',
      'CC BY-NC 4.0',
      'CC BY-NC-ND',
      'CC BY-SA 2.0',
      'CC BY-SA 3.0',
      'CC BY-SA 4.0',
      'CC BY',
      'Dr. Drang',
      'Git LFS',
      'HTTP 200 OK',
      'iMac G3',
      'iPhone X',
      'IP address',
      'JPEG 2000',
      'Mac OS 9',
      'Mac OS X',
      'Monki Gras',
      'MS Paint',
      'Objective-C',
      'P-215',
      'PDF 1.6',
      'PDF 1.7',
      'PyCon ',
      'Route 53',
      'System 1'
    ]

    phrases.each do |p|
      replacement = p.gsub(' ', '&nbsp;').gsub('-', '&#8209;')
      text = text.gsub(p, replacement)
    end

    text
  end
end

module Jekyll
  module CleanupsFilter
    def cleanup_text(input)
      cache = Jekyll::Cache.new('CleanupText')

      cache.getset(input) do
        text = AddNonBreakingSpaces.add_non_breaking_spaces(input)

        # Display "LaTeX" in a nice way, if you have CSS enabled
        text = text.gsub(
          ' LaTeX',
          ' <span class="visually-hidden">LaTeK</span>' \
          '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>'
        )

        text = text.gsub(
          ' TeX',
          ' <span class="visually-hidden">TeK</span>' \
          '<span class="latex" aria-hidden="true">T<sub>e</sub>X</span>'
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
end

Liquid::Template.register_filter(Jekyll::CleanupsFilter) if defined? Liquid
