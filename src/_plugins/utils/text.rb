# frozen_string_literal: true

require 'json'
require 'minify_html'

alias _lib_minify_html minify_html

module Alexwlchan
  module TextUtils
    # Convert some Markdown text into HTML.
    #
    # Example:
    #
    #     markdownify("Five *shocking* facts")
    #     <p>Five <em>shocking</em> facts</p>
    #
    def self.markdownify(site, markdown)
      return nil if markdown.nil?

      site.find_converter_instance(Jekyll::Converters::Markdown)
          .convert(markdown)
    end

    # Convert a single line of Markdown text into HTML.
    #
    # The output is an HTML string, but not wrapped in <p> tags.
    #
    # Example:
    #
    #     markdownify_oneline("Five *shocking* facts")
    #     Five <em>shocking</em> facts
    #
    def self.markdownify_oneline(site, markdown)
      return nil if markdown.nil?

      site.find_converter_instance(Jekyll::Converters::Markdown)
          .convert(markdown)
          .sub('<p>', '')
          .sub('</p>', '')
          .strip
    end

    # Compress an HTML string.
    #
    # Example:
    #
    #     minify_html("<p>Hello world</p>\n  <p>The car is red</p>\n")
    #     <p>Hello world</p><p>The car is red</p>
    #
    def self.minify_html(html)
      options = {
        keep_html_and_head_opening_tags: true,
        keep_closing_tags: true,
        minify_css: true,
        minify_js: true
      }

      _lib_minify_html(html, options)
    end

    # Wrap the words "TeX" and "LaTeX" in <span> elements that allow
    # them to be displayed nicely in my HTML.
    def self.add_latex_css_classes(html)
      return html unless html.include? 'TeX'

      html = html.gsub(
        ' LaTeX',
        '<style type="x-text/scss">@use "components/latex";</style> ' \
        '<span class="visually-hidden">LaTeK</span>' \
        '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>'
      )

      html.gsub(
        ' TeX',
        '<style type="x-text/scss">@use "components/latex";</style> ' \
        '<span class="visually-hidden">TeK</span>' \
        '<span class="latex" aria-hidden="true">T<sub>e</sub>X</span>'
      )
    end

    # Force footnote markers to render as text on iOS, devices, not emoji.
    #
    # See https://mts.io/2015/04/21/unicode-symbol-render-text-emoji/
    def self.force_text_footnote_markers(html)
      return html unless html.include?('&#8617;') || html.include?('↩')

      html
        .gsub('&#8617;', '&#8617;&#xFE0E;')
        .gsub('↩', '&#8617;&#xFE0E;')
    end

    # Add non-breaking spaces and hyphens to my text.
    #
    # See https://alexwlchan.net/2020/adding-non-breaking-spaces-with-jekyll/
    def self.add_non_breaking_characters(text)
      # "e.g." introduces an example; it's annoying when the example text has
      # been bumped to another line, so don't let it.
      text.gsub('e.g. ', 'e.g.&nbsp;')

      # Add a non-breaking space after words which are followed by
      # a number or word, e.g. 'Apollo 11' or 'RFC 456'
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
        Mr.
        Mrs.
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
        GiB
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

      # Add a non-breaking space after short words if they're the first word
      # in a sentence.
      %w[A An I].each do |w|
        text = text.gsub(". #{w} ", ". #{w}&nbsp;")
        text = text.gsub(".\n#{w} ", ".\n#{w}&nbsp;")
      end

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
        'C.S. Lewis',
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
        'VS Code',
        'Windows-1252',
        'z-axis'
      ]

      phrases.each do |p|
        if text.include? p
          replacement = p.gsub(' ', '&nbsp;').gsub('-', '&#8209;')
          text = text.gsub(p, replacement)
        end
      end

      # Add non-breaking hyphens to "yt-dlp", but only if it's not part of a URL
      text = text.gsub(%r{([^\-/])yt-dlp}, '\1yt&#8209;dlp')

      # If there's an <a> that starts with the word "a", make sure we
      # add a non-breaking space to it.
      #
      #     <a href="https://example.com">an example</a>
      #  ~> <a href="https://example.com">an&nbsp;example</a>
      #
      text = text.gsub(/<a ([^>]+)>a /, '<a \1>a&nbsp;')
      text = text.gsub(/<a ([^>]+)>an /, '<a \1>an&nbsp;')

      # If there's a multiplication symbol (×) surrounded by numbers,
      # add a narrow non-breaking space either side.
      text.gsub(/([0-9])×([0-9])/, '\1&#8239;×&#8239;\2')
    end

    # The syntax highlighter wraps highlighted code blocks in:
    #
    #     <div class="language-{language} highlighter-rouge">
    #       <div class="highlight">
    #         <pre>
    #           …
    #
    # Strip out the extra CSS classes and HTML tags.
    #
    def self.cleanup_syntax_highlighter_classes(html)
      return html unless html.include? '<code'

      # I never use the `highlighter-rouge` class, and I only have styles
      # for a couple of the `language-*` classes.
      #
      # Note (2025-12-23): the 1Password browser extension has enabled
      # Prism.js syntax highlighting in web pages, and it looks for
      # any <pre> elements with a language-* class, so rename it to lng.
      %w[caddy console css diff go html irb shell xml].each do |lang|
        html = html.gsub(" class=\"language-#{lang} highlighter-rouge\"", " class=\"lng-#{lang}\"")
      end

      html = html.gsub(/ class="language-[a-z]+ highlighter-rouge"/, '')

      # I never use the `highlight` class.
      #
      # If there's a `language-tag` on the outer `<div>`, move it to the `<pre>`.
      html = html.gsub(
        /<div class="lng-(?<lang_code>[a-z]+)"><div class="highlight"><pre class="highlight">/,
        '<pre class="lng-\k<lang_code>">'
      )
      html = html.gsub(
        '<div><div class="highlight"><pre class="highlight"',
        '<pre'
      )
      html = html.gsub(%r{</pre></div>\s*</div>}, '</pre>')

      # Remove any whitespace before/after `<pre>` blocks
      html = html.gsub(/\s+<pre>/, '<pre>')
      html.gsub(%r{</pre>\s+}, '</pre>')
    end
  end
end
