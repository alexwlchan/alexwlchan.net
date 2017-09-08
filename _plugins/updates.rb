module Jekyll
  class UpdateBlock < Liquid::Block

    def initialize(tag_name, markup, options)
      super
      @date = Date.parse(markup, "%Y-%m-%d")
    end

    def render(context)
      result = super

      # https://stackoverflow.com/q/19169849/1558022
      site = context.registers[:site]
      converter = site.find_converter_instance(::Jekyll::Converters::Markdown)
      update_string = "**Update, #{@date.strftime("%-d %B %Y")}:**"
      <<-EOT
<blockquote class="update">
  #{converter.convert(update_string + super(context))}
</blockquote>
EOT
    end
  end
end

Liquid::Template.register_tag('update', Jekyll::UpdateBlock)
