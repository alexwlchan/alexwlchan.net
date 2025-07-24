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

def add_non_breaking_spaces(input)
  text = input

  # "e.g." introduces an example; it's annoying when the example text has
  # been bumped to another line, so don't let it.
  text.gsub('e.g. ', 'e.g.&nbsp;')

  # Add a non-breaking space after words which are followed by
  # a number, e.g. 'Apollo 11' or 'RFC 456'
  prefix_words = %w[
    Apollo
    Artemis
    chapter
    HTTP
    ImageMagick
    ISO/IEC
    Issue
    issue
    iPres
    No.
    Part
    part
    Python
    RFC
    Safari
    Season
    season
    SQLite
  ].join('|')

  text = text.gsub(/(#{prefix_words}) (\d+)/, '\1&nbsp;\2')

  # Add a non-breaking space after words which are preceded by
  # a number, e.g. '1 second' or '5 bytes'
  countable_words = %w[
    bookmark
    byte
    character
    count
    GB
    hour
    inch
    kilometre
    line
    MiB
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
    'Algorithm L',
    'Algorithm R',
    'Amazon S3',
    'Apple TV+',
    'CC0 1.0',
    'CC BY 2.0',
    'CC BY 3.0',
    'CC BY 4.0',
    'CC BY-NC 2.0',
    'CC BY-NC 4.0',
    'CC BY-ND 2.0',
    'CC BY-NC-ND',
    'CC BY-SA 2.0',
    'CC BY-SA 3.0',
    'CC BY-SA 4.0',
    'CC BY-NC-SA 4.0',
    'CC BY',
    'DjangoCon US',
    'Dr. Drang',
    'ECMA-404',
    'Git LFS',
    'HTTP 200 OK',
    'iMac G3',
    'iPhone X',
    'IP address',
    'JPEG 2000',
    'Latin-1',
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
    'Silo 49',
    'System 1',
    'Windows-1252',
    'z-axis'
  ]

  phrases.each do |p|
    if text.include? p
      replacement = p.gsub(' ', '&nbsp;').gsub('-', '&#8209;')
      text = text.gsub(p, replacement)
    end
  end

  # If there's an <a> that starts with the word "a", make sure we
  # add a non-breaking space to it.
  #
  #     <a href="https://example.com">an example</a>
  #  ~> <a href="https://example.com">an&nbsp;example</a>
  #
  text = text.gsub(/<a ([^>]+)>a /, '<a \1>a&nbsp;')
  text.gsub(/<a ([^>]+)>an /, '<a \1>an&nbsp;')
end

# The syntax highlighter wraps highlighted code blocks in:
#
#     <div class="language-{language} highlighter-rouge">
#       <div class="highlight">
#         <pre>
#           …
#
# We can strip out some of these CSS classes and HTML tags.
#
def cleanup_syntax_highlighter_classes(html)
  # I never use the `highlighter-rouge` class, and I only have styles
  # for a couple of the `language-*` classes.
  %w[caddy console go irb].each do |lang|
    html = html.gsub(" class=\"language-#{lang} highlighter-rouge\"", " class=\"language-#{lang}\"")
  end

  html = html.gsub(/ class="language-[a-z]+ highlighter-rouge"/, '')

  # I never use the `highlight` class.
  #
  # If there's a `language-tag` on the outer `<div>`, move it to the `<pre>`.
  html = html.gsub(
    /<div class="language-(?<language>[a-z]+)"><div class="highlight"><pre class="highlight">/,
    '<pre class="language-\k<language>">'
  )
  html = html.gsub(
    '<div><div class="highlight"><pre class="highlight">',
    '<pre>'
  )
  html = html.gsub(%r{</pre></div>\s*</div>}, '</pre>')
  html = html.gsub(
    /<code class="language-(?<language>[a-z]+)" data-lang="[a-z]+">/,
    '<code>'
  )

  # Remove any whitespace before/after `<pre>` blocks
  html = html.gsub(/\s+<pre>/, '<pre>')
  html.gsub(%r{</pre>\s+}, '</pre>')
end

module Jekyll
  module CleanupsFilter
    def cleanup_text(input)
      cache = Jekyll::Cache.new('CleanupText')

      cache.getset(input) do
        text = add_non_breaking_spaces(input)

        if text.include? '<pre'
          text = cleanup_syntax_highlighter_classes(text)
        end

        # Display "LaTeX" in a nice way, if you have CSS enabled
        if text.include? 'TeX'
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
        end

        # Make sure that footnote markers are rendered as a text
        # arrow on iOS devices, not emoji.  For more info:
        # http://daringfireball.net/linked/2015/04/22/unicode-emoji
        text = text
               .gsub('&#8617;', '&#8617;&#xFE0E;')
               .gsub('↩', '&#8617;&#xFE0E;')

        text.strip
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CleanupsFilter) if defined? Liquid
