# This plugin allows me to annotate code blocks with line numbers
# and a link to their source.
#
# You need to supply `lang` and `src` attributes, and optionally `start_line`
# if your code snippet doesn't start on line 1:
#
#     {% annotatedhighlight
#       lang="python"
#       start_line="7"
#       src="https://github.com/example/example-repo/blob/10539c4/greet.py#L7"
#     %}
#     def greet():
#         print("hello world!")
#     {% endannotatedhighlight %}
#

require 'uri'

require_relative 'utils/attrs'

module Jekyll
  class AnnotatedHighlightBlock < Liquid::Block
    def initialize(tag_name, params_string, tokens)
      super
      @attrs = parse_attrs(params_string)
    end

    def render(context)
      site = context.registers[:site]

      # Send the code through the default Markdown renderer, which
      # gets us a `<pre>` with all the syntax highlighting classes.
      code_snippet = super.strip
      raw_code = "```#{@attrs['lang']}\n#{code_snippet}\n```"
      code_pre = site.find_converter_instance(Jekyll::Converters::Markdown)
                     .convert(raw_code)

      # If I didn't pass any line numbers for this code block, default
      # the line numbers to 1-N, where N is the number of lines.
      if @attrs['line_numbers'].nil?
        line_count = code_snippet.split("\n").length
        @attrs['line_numbers'] = "1-#{line_count}"
      end

      # Parse a range like 1-3,7-9 as a complete list of line numbers,
      # i.e. [1,2,3,7,8,9]
      line_numbers = @attrs['line_numbers'].split(',').map do |r|
        line_start, line_end = r.split('-')
        (line_start..line_end).to_a
      end
      .flatten

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
      #     def greet():
      #         print("hello world!")
      #     </pre>
      #
      # We look for lines which are just ellipsis, which I often use
      # in code snippets to indicate there's more text that I omitted.
      prefix, code_open, code_post = code_pre.partition('<code>')
      inner_code, code_close, suffix = code_post.partition('</code>')

      lineno_idx = 0

      inner_code = inner_code.split("\n")
                             .each_with_index
                             .map do |ln, idx|
        line_is_ellipsis = code_snippet.split("\n")[idx].strip == '...'
        all_line_numbers_used = lineno_idx >= line_numbers.length

        if line_is_ellipsis || all_line_numbers_used
          "<span class=\"ln empty\">#{code_snippet.split("\n")[idx]}</span>"
        else
          this_lineno = line_numbers[lineno_idx]
          lineno_idx += 1
          "<span class=\"ln\" style=\"--ln: #{this_lineno}\">#{ln}</span>"
        end
      end
        .join("\n")

      code_pre = "#{prefix}#{code_open}#{inner_code}#{code_close}#{suffix}"

      # Work out how many digits there are in the line numbers.
      lineno_digits = line_numbers.map { |ln| ln.to_s.length }.max

      # Create a <figcaption> to indicate the source of this code,
      # if a source URL was specified.
      #
      # This assumes this is a GitHub link
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
            From <a href="#{@attrs['src']}">#{filename}</a>, lines #{line_numbers.min}–#{line_numbers.max}, in <a href="https://github.com/#{organization}/#{repository}/">#{organization}/#{repository}</a>
          </figcaption>
HTML
      end

      # Now construct a <figure> element which wraps the two <pre> elements.
      <<~HTML
        <figure
          class="annotated_highlight"
          style="--lineno-digits: #{lineno_digits}">
            #{code_pre}
            #{figcaption}
        </figure>
      HTML
    end
  end
end

Liquid::Template.register_tag('annotatedhighlight', Jekyll::AnnotatedHighlightBlock)
