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
      prefix, code_open, code_post = code_pre.partition('<code>')
      inner_code, code_close, suffix = code_post.partition('</code>')

      inner_code = inner_code.split("\n").map { |ln| "<span class=\"ln\">#{ln}</span>" }.join("\n")

      code_pre = "#{prefix}#{code_open}#{inner_code}#{code_close}#{suffix}"

      # Work out what the start/end line for this annotated code block is;
      # if we don't have an explicit start line, start at 1.
      start_line = @attrs.fetch('start_line', '1').to_i
      end_line = start_line + inner_code.split("\n").length

      # Work out how many digits there are in the line numbers.
      lineno_digits = end_line.to_s.length

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

        figcaption = <<EOF
          <figcaption>
            From <a href="#{@attrs['src']}">#{filename}</a>, lines #{start_line}–#{end_line}, in <a href="https://github.com/#{organization}/#{repository}/">#{organization}/#{repository}</a>
          </figcaption>
EOF
      end

      # Now construct a <figure> element which wraps the two <pre> elements.
      <<~EOF
        <figure
          class="annotated_highlight"
          style="--start-line: #{start_line};
                 --lineno-digits: #{lineno_digits}">
            #{code_pre}
            #{figcaption}
        </figure>
      EOF
    end
  end
end

Liquid::Template.register_tag('annotatedhighlight', Jekyll::AnnotatedHighlightBlock)
