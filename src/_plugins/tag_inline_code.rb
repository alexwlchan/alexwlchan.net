# Can I do away with this?

# Inline a file as highlighted code.
#
# This expects to be used in the body of a post.  The original file
# should be saved in the per-year subdirectory of `_files`.
#
# Takes the filename as a single argument.
#
# The syntax highlighting to use will be inferred from the file extension.
#
# == Example ==
#
# This is a simple example:
#
#     {% inline_code filename="division1.rb" %}
#
# This is in a post written in 2022, so it will inline a file found at
# at `src/_files/2022/division1.rb`.
#
# You can override the language if desired:
#
#     {% inline_code filename="service-2.sdk-extras.json" language="text" %}
#
# This will be highlighted as text, not JSON.

require_relative 'utils/attrs'

module Jekyll
  class InlineCodeTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      @attrs = parse_attrs(params_string)

      @filename = get_required_attribute(
        @attrs, { tag: 'inline_code', attribute: 'filename' }
      )
    end

    def guess_language(filename)
      case File.extname(filename)
      when '.js'
        'javascript'
      when '.py'
        'python'
      when '.rb'
        'ruby'
      else
        raise "Unrecognised code file extension: #{File.extname(filename)}"
      end
    end

    def render(context)
      # This allows us to deduce the source path of the image
      site = context.registers[:site]
      src = site.config['source']

      year = context.registers[:page]['date'].year

      src_code = File.read("#{src}/_files/#{year}/#{@filename}").strip
      language = @attrs['language'] || guess_language(@filename)

      input = "```#{language}\n" \
              "#{src_code}\n" \
              "```\n"

      site.find_converter_instance(Jekyll::Converters::Markdown)
          .convert(input)
    end
  end
end

Liquid::Template.register_tag('inline_code', Jekyll::InlineCodeTag)
