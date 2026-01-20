# This plugin allows me to put an update on a post, e.g.
#
#    {% update date="2020-05-02" %}
#      Here is some new information
#    {% endupdate %}
#

require_relative 'utils/attrs'

module Jekyll
  class UpdateBlock < Liquid::Block
    def initialize(tag_name, params_string, options)
      super
      attrs = parse_attrs(params_string)
      @date = Date.parse(attrs['date'], '%Y-%m-%d')
    end

    def render(context)
      super

      # https://stackoverflow.com/q/19169849/1558022
      site = context.registers[:site]
      converter = site.find_converter_instance(::Jekyll::Converters::Markdown)

      timestamp_tpl = Liquid::Template.parse(File.read('src/_includes/timestamp.html'))
      timestamp_html = timestamp_tpl.render!('include' => { 'date' => @date })

      md = "**Update, #{timestamp_html}:** #{super}"

      update_tpl = Liquid::Template.parse(File.read('src/_includes/update.html'))
      update_tpl.render!('date' => @date, 'text' => converter.convert(md))
    end
  end
end

Liquid::Template.register_tag('update', Jekyll::UpdateBlock)
