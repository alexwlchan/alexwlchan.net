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

require_relative 'utils/attrs'
require_relative 'utils/code'
require_relative 'utils/text'

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
      if lang == 'python'
        dotted_imports = [
          'concurrent.futures', 'collections.abc', 'gunicorn.glogging', 'gunicorn.http.message', 'gunicorn.http.wsgi'
        ]

        dotted_imports.each do |import|
          next unless html.include?(import)

          part0, part1 = import.split('.')
          html = html.gsub(
            "<span class=\"kn\">import</span> <span class=\"n\">#{import}</span>",
            "<span class=\"kn\">import</span> <span class=\"n\">#{part0}</span><span class=\"p\">.</span><span class=\"n\">#{part1}</span>"
          )
          html = html.gsub(
            "<span class=\"kn\">from</span> <span class=\"n\">#{import}</span>",
            "<span class=\"kn\">from</span> <span class=\"n\">#{part0}</span><span class=\"p\">.</span><span class=\"n\">#{part1}</span>"
          )
        end
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

        # If we're in debug mode, add a checkbox and a <label> that can
        # be used to opt names in-and-out.
        #
        # This allows me to build the colouring interactively.
        if @attrs['debug'] == 'true'
          form_id = "#{idx}:#{varname}"
          html[m.begin(0)..(m.end(0) - 1)] = "<label for=\"#{form_id}\">#{varname}<input class=\"codeName\" type=\"checkbox\" id=\"#{form_id}\" onChange=\"recalculateVariables()\"/></label>"
          next
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

      # If we're in debug mode, append the debugging snippet.
      #
      # This gives me a tool that lets my dynamically choose which names
      # to highlight, and constructs the `names` string I should add
      # to my code.
      if @attrs['debug'] == 'true'
        debug_snippet = <<~HTML
          <p id="debug">DEBUG: <code id="debugNames">names=""</code></p>
          <style>
            pre input[type="checkbox"] {
              display: none;
            }

            pre label {
              text-decoration: underline;
              -webkit-text-decoration-style: dashed;
            }
          #{'  '}
            pre label:has(input[type="checkbox"]:checked) {
              color: var(--blue);
            }
          #{'  '}
            #debug {
              color: red;
            }
          </style>
          <script>
            function recalculateVariables() {
              debugNames = document.querySelector("code#debugNames");
          #{'    '}
              var selectedNames = [];
          #{'    '}
              document.querySelectorAll("input.codeName")
                .forEach(checkbox => {
                  if (checkbox.checked) {
                    selectedNames.push(checkbox.id);
                  }
                });
          #{'    '}
              debugNames.innerText = `names="${selectedNames.join(" ")}"`;
            }
          </script>
        HTML
        html += debug_snippet
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

      # Python: the shebang at the top of the file is punctuation, not
      # a comment.
      if lang == 'python'
        html = html.gsub(
          "<span class=\"c1\">#!/usr/bin/env python3\n</span>",
          "<span class=\"p\">#!/usr/bin/env python3\n</span>"
        )
      end

      # Python console: don't highlight the last continuation ellipsis
      # in red, just make it blue like the rest.
      if lang == 'console?lang=python&prompt=>>>,...'
        html = html.gsub(
          "<span class=\"c\">...\n</span>",
          "<span class=\"gp\">...\n</span>"
        )
      end

      # Shell: line continuation characters are punctuation, not escapes.
      if %w[shell console].include?(lang)
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
      html = Alexwlchan::TextUtils.cleanup_syntax_highlighter_classes(html)

      # If wrap="true", add some CSS to wrap at the screen edge, rather
      # than on the line breaks.
      if @attrs['wrap'] == 'true'
        if html.include? '<pre class="'
          html = html.sub('<pre class="', '<pre class="wrap ')
        else
          html = html.sub('<pre', '<pre class="wrap"')
        end
      end

      # Optionally add line numbers to the snippet.
      if @attrs['linenos'] == 'true' || @attrs['line_numbers']
        html, first_lineno, last_lineno, lineno_digits = add_line_numbers(html, code_snippet)
      else
        lineno_digits = 0
      end

      # Optionally create a <figcaption> to indicate the source of
      # this code, if a source URL was specified.
      #
      # This assumes this is a GitHub link.
      #
      # Note: this assumes a line range because it assumes sourced code
      # will always be accompanied by line numbers.
      if @attrs['src'].nil?
        figcaption = ''
      else

        # e.g. /swiftlang/swift-org-website/blob/10539c47/index.md
        path = URI.parse(@attrs['src']).path

        # e.g. swiftlang, swift-org-website
        organization = path.split('/')[1]
        repository = path.split('/')[2]

        # e.g. "index.md"
        filename = File.basename(path)

        figcaption = <<HTML
          <figcaption>
            From <a href="#{@attrs['src']}">#{filename}</a>, lines #{first_lineno}–#{last_lineno}, in <a href="https://github.com/#{organization}/#{repository}/">#{organization}/#{repository}</a>
          </figcaption>
HTML
      end

      # If we have line numbers or attribution, wrap everything in a <figure>
      # element that includes them both.
      if lineno_digits.positive? || figcaption != ''
        html = <<~HTML
          <figure
            class="annotated_code"
            style="--lineno-digits: #{lineno_digits}">
            #{html}
            #{figcaption}
          </figure>
        HTML
      end

      html
    end

    def add_line_numbers(html, code_snippet)
      line_count = code_snippet.split("\n").length

      # If we passed linenos=true but didn't set any line numbers
      # explicitly, default the line numbers to 1–N, where N is the
      # number of lines.
      if @attrs['line_numbers'].nil?
        @attrs['line_numbers'] = "1-#{line_count}"
      end

      # Parse the line numbers attribute.
      line_numbers = Alexwlchan::CodeUtils.parse_line_numbers(
        @attrs['line_numbers']
      )

      # Check we have the correct number of line numbers to pair with
      # each line in the snippet.
      if line_numbers.length != line_count
        raise "mismatched line numbers: got #{line_numbers.length}, want #{line_count}"
      end

      # Wrap each line in a <span class="ln"> (for "line") element
      #
      # e.g. if the input is
      #
      #     <pre>
      #     def greet():
      #         print("hello world!")
      #     </pre>
      #
      # then it becomes
      #
      #     <pre>
      #     <span class="ln">def greet():</span>
      #     <span class="ln">    print("hello world!")</span>
      #     </pre>
      #
      # We look for lines which are just ellipsis, which I often use
      # in code snippets to indicate there's more text that I omitted.
      prefix, code_open, code_post = html.partition('<code>')
      inner_code, code_close, suffix = code_post.partition('</code>')

      inner_code_lines = inner_code.split("\n")
      inner_code = inner_code_lines.zip(line_numbers).map do |line, lineno|
        if lineno == '_'
          "<span class=\"ln empty\">#{line}</span>"
        else
          "<span class=\"ln\" style=\"--ln: #{lineno}\">#{line}</span>"
        end
      end
                  .join("\n")

      html = "#{prefix}#{code_open}#{inner_code}#{code_close}#{suffix}"

      # Work out how many digits there are in the line numbers.
      lineno_digits = line_numbers.map { |ln| ln.to_s.length }.max

      first_lineno = line_numbers[0]
      last_lineno = line_numbers.filter { |ln| ln != '_' }[-1]

      [html, first_lineno, last_lineno, lineno_digits]
    end
  end
end

Liquid::Template.register_tag('code', Jekyll::CodeBlock)
