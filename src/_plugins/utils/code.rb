# frozen_string_literal: true

module Alexwlchan
  module CodeUtils
    # Parse a range like 1-3,7-9 as a complete list of line numbers,
    # i.e. [1,2,3,7,8,9]
    #
    # The line numbers can include an _ character, which indicates the
    # line should not be numbered.
    def self.parse_line_numbers(linenos)
      linenos.split(',').map do |r|
        if r.include? '-'
          line_start, line_end = r.split('-')
          (line_start..line_end).to_a
        else
          r
        end
      end
      .flatten
    end

    # Apply syntax highlighting fixes that go beyond what Rouge does,
    # based on my custom language attributes.
    #
    # This runs before the name analyser, so can be used to mark tokens
    # as names that are ignored by what Rouge does.
    def self.apply_manual_names(html, attr_lang, _rouge_lang)
      # Bash: add syntax highlighting for function names.
      #
      # I'm surprised this isn't supported natively, but maybe some
      # other shells don't have bash function syntax?
      if attr_lang == 'bash'
        html = html.gsub(
          %r{\n([a-z_]+)<span class="o">\(\)</span>},
          "\n<span class=\"nf\">\\1</span><span class=\"o\">()</span>"
        )
      end

      html
    end

    # Apply syntax highlighting fixes that go beyond what Rouge does,
    # based on my custom language attributes.
    #
    # This is hacky and manual, but it should be fine because I'm always
    # going to review the output manually.
    def self.apply_manual_fixes(html, attr_lang, rouge_lang)
      # Nested CSS: fix the highlighting of nested elements.
      #
      # This isn't as good as proper support for nesting in Rouge, but
      # that's somewhat complicated so I can do hard-coded fixes -- I'll
      # be reviewing all this code manually anyway.
      #
      # See https://github.com/rouge-ruby/rouge/issues/2101
      # See https://github.com/rouge-ruby/rouge/pull/2150
      if attr_lang == 'nested_css'

        # Reclassify nested selectors which have been labelled as properties
        html_tags = %w[figcaption img]
        html_tags.each do |tag|
          next unless html.include?(tag)

          html = html.gsub("<span class=\"n\">#{tag}</span>", "<span class=\"nt\">#{tag}</span>")
        end

        # Special case for the `a:hover` selector.
        html = html.gsub(
          '<span class="py">a</span><span class="p">:</span><span class="n">hover</span>',
          '<span class="nt">a</span><span class="nd">:hover</span>'
        )

        # Replace element names and class selectors, e.g. figcaption, .wrapper
        html = html.gsub(
          %r{<span class="err">(\.?[a-z]+)</span>},
          '<span class="nt">\\1</span>'
        )

        # Mark braces as punctuation
        html = html.gsub(
          %r{<span class="err">(\{|\})</span>},
          '<span class="p">\\1</span>'
        )
      end

      # Shebangs are punctuation, not comments.
      if rouge_lang == 'shell'
        html = html.gsub(
          '<span class="c">#!/usr/bin/env bash</span>',
          '<span class="p">#!/usr/bin/env bash</span>'
        )
      end

      # Bash: don't highlight $(…) as strings.
      if attr_lang == 'bash'
        html = html.gsub('<span class="si">$(</span>', '$(')
        html = html.gsub('<span class="si">)</span>', ')')
      end

      html
    end
  end
end
