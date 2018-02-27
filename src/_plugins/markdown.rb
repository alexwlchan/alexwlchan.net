module Jekyll
  module MarkdownFilter
    def render_markdown(input)
      site = @context.registers[:site]
      converter = site.find_converter_instance(::Jekyll::Converters::Markdown)
      converter.convert(input).sub("<p>", "").sub("</p>", "")
    end
  end
end

Liquid::Template::register_filter(Jekyll::MarkdownFilter)
