# This plugin allows me to inline a file as highlighted code.
#
# It means I can have a file that can be downloaded, and include the complete
# code in the body of the post, and the two will stay in sync.
# (For example, a Python script.)
#
# Takes two parameters: the language code, and the path to the file.
#
# e.g. {% inline_code python _files/2020/redrive_sqs_queue.py %}
#

module Jekyll
  class InlineCodeTag < Liquid::Tag
    def initialize(_tag_name, text, _tokens)
      super
      @lang, @path = text.strip.split(" ")
    end

    def render(context)
      site = context.registers[:site]
      src = site.config["source"]

      src_code = File.read("#{src}/#{@path}").strip

      "```#{@lang}\n#{src_code}\n```\n"
    end
  end
end

Liquid::Template.register_tag("inline_code", Jekyll::InlineCodeTag)
