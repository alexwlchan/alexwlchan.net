# This plugin allows me to annotate code blocks with line numbers
# and a link to their source.
#
# You need to supply `lang` and `src` attributes, and optionally `start_line`
# if your code snippet doesn't start on line 1:
#
#     {% code lang="python" %}
#     def greet():
#         print("hello world!")
#     {% endcode %}
#
# Other supported attributes:
#
#   - names="1:name 2:name 3:name" ~ variable definitions to highlight in blue
#   - debug="true" ~ show the index of all variables, to help me write `names`
#
#   - wrap="true" ~ whether to add `white-space: pre-wrap` so all the code
#     gets wrapped at the screen edge
#

require 'uri'

require_relative 'cleanup_text'
require_relative 'utils/attrs'

def dedent(str)
  # Find the smallest common indentation (excluding empty lines)
  indent = str.scan(/^[ \t]*(?=\S)/).min_by(&:length)
  str.gsub(/^#{indent}/, '')
end

module Jekyll
  class CodeBlock < Liquid::Block
    def initialize(tag_name, params_string, tokens)
      super
      @params_string = params_string
      @attrs = parse_attrs(params_string)
    end

    def render(context)
      site = context.registers[:site]

      # Work out what the common indent is, if any, then dedent the
      # code snippet
      dedent = super.match(/\n(\s*)/)[1]
      if dedent == ''
        code_snippet = super.strip
      else
        code_snippet = super.gsub("\n#{dedent}", "\n").strip
      end

      # Hard-coded fixes for some languages
      lang = @attrs['lang']
      if lang == 'pycon'
        lang = 'console?lang=python&prompt=>>>,...'
      end

      # Work out what variable names (if any) are defined in this block.
      names_to_highlight = (@attrs['names'] || '').split.to_h { |ns| ns.split(':') }.transform_keys(&:to_i)

      # Send the code through the default Markdown renderer, which
      # gets us a `<pre>` with all the syntax highlighting classes.
      #
      # Insert the current time as a Unix timestamp as a cache buster.
      # This prevents Jekyll::Converters from doing any cache busting,
      # which can cause the debug name numbers to be double-printed
      # when doing local dev.
      now = Time.now.to_i
      raw_code = "<!-- t=#{now} -->```#{lang}\n#{code_snippet}\n```"
      html = site.find_converter_instance(Jekyll::Converters::Markdown)
                 .convert(raw_code)

      # Replace dotted imports in Python with names broken down by
      # namespace, so the dots get grey punctuation
      if html.include?('concurrent.futures') && (lang == 'python')
        html = html.gsub(
          '<span class="kn">import</span> <span class="n">concurrent.futures</span>',
          '<span class="kn">import</span> <span class="n">concurrent</span><span class="p">.</span><span class="n">futures</span>'
        )
      end

      # Find all the names which are highlighted as part of this code
      name_matches = html
                     .to_enum(:scan, %r{<span class="n[a-z0]?">(?<varname>[^<]+)</span>})
                     .map { Regexp.last_match }

      # Go through and un-highlight any names that aren't explicitly
      # labelled as new
      name_matches.reverse_each.with_index do |m, idx|
        idx = name_matches.length - idx - 1
        varname = m.named_captures['varname']

        unless @attrs['debug'].nil?
          html[m.begin(0)..(m.end(0) - 1)] = m[0] + "[#{idx}]"
        end

        # If this isn't one of the names we want to highlight, remove the
        # <span class="n*"> and continue
        #
        # TODO: I'm replacing this with `n0`, a non-existent class, because
        # otherwise consecutive builds in a `jekyll serve` fail -- this gets
        # the post-processed HTML on subsequent builds, not the raw MD.
        if names_to_highlight[idx].nil?
          if %w[html css].include?(lang)
            next
          end

          if m[0].start_with? '<span class="no">'
            next
          end

          html[m.begin(0)..(m.end(0) - 1)] = "<span class=\"n0\">#{varname}</span>"
          next
        end

        # If this is one of the names we want to highlight but the variable
        # name doesn't match, throw an error.
        if names_to_highlight[idx] != varname
          raise "got bad name at #{idx}: want #{names_to_highlight[idx]}, got #{varname}"
        end

        # Re-wrap in <span class="n">, so any previously ignored names
        # come back.
        html[m.begin(0)..(m.end(0) - 1)] = "<span class=\"n\">#{varname}</span>"
      end

      # Highlight Rust booleans as .kc (keyword-constant) rather than
      # .k (keyword).
      if lang == 'rust'
        html = html.gsub('<span class="k">true</span>', '<span class="kc">true</span>')
        html = html.gsub('<span class="k">false</span>', '<span class="kc">false</span>')
      end

      # Only highlight the string portion of a CSS url()
      if lang == 'css'
        html = html.gsub(
          %r{<span class="sx">url\(([^>)]+)\)</span>},
          'url(<span class="sx">\\1</span>)'
        )
      end

      # Python: highlight ellipsis as punctuation, not a builtin keyword.
      if lang == 'python'
        html = html.gsub(
          '<span class="bp">...</span>',
          '<span class="p">...</span>'
        )
      end

      # Shell: line continuation characters are punctuation, not escapes.
      if lang == 'shell'
        html = html.gsub(
          %r{<span class="se">\\</span>\n},
          "<span class=\"p\">\\</span>\n"
        )
      end

      # Ruby: double colon between parts of a class name are punctuation.
      if lang == 'ruby'
        html = html.gsub(
          '<span class="o">::</span>',
          '<span class="p">::</span>'
        )
      end

      # Ruby: class names are not constants.
      if lang == 'ruby'
        html = html.gsub(
          %r{<span class="no">([A-Z][a-zA-Z_]+)</span>},
          '\\1'
        )
      end

      html = html.gsub(%r{<span class="k">([^>]+)</span>}, '\\1')
      html = html.gsub(%r{<span class="kn">([^>]+)</span>}, '\\1')
      html = html.gsub(%r{<span class="o">([^>]+)</span>}, '\\1')

      # Remove the cache-busting comment we included earlier
      html = html.gsub("<!-- t=#{now} -->\n", '')

      # Clean up the syntax highlighter classes, remove the wrapper <div>
      html = cleanup_syntax_highlighter_classes(html)

      # If wrap="true", add some CSS to wrap at the screen edge, rather
      # than on the line breaks.
      if @attrs['wrap'] == 'true'
        html = html.sub('<pre', '<pre style="white-space: pre-wrap;"')
      end

      # Restore the dedent to every line except the first.  This is
      # important when we're in indented Markdown
      html.gsub("\n", "\n#{dedent}")
    end
  end
end

Liquid::Template.register_tag('code', Jekyll::CodeBlock)
