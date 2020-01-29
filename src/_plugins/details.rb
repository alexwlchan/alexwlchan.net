# This plugin provides a {% details %} block, which is mostly a thin wrapper
# around the HTML 5 <details> tag.
#
# Use the block when you want to run the Markdown renderer inside the contents
# of the tag, e.g. for code rendering.
#
# This renders a Python-highlighted code block:
#
#     {% details %}
#
#     ```python
#     print("hello world")
#     ```
#
#     {% enddetails %}
#
# This only has backticks and run-together text:
#
#     <details>
#
#     ```python
#     print("hello world")
#     ```
#
#     </details>
#

require_relative "alexwlchan_base"


module Jekyll
  class DetailsBlock < Alexwlchan::Block
    def bind_params(params)
    end

    def internal_render
      <<-EOT
<details>
  #{markdown_converter.convert(@text)}
</details>
EOT
    end
  end
end


Liquid::Template.register_tag("details", Jekyll::DetailsBlock)
