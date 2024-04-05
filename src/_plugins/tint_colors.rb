# Handle custom tint colours on pages.
#
# You can set a custom CSS colour in the front matter for a page,
# in which case the links/header for that page will all be tinted
# based on that colour.
#
# This plugin handles all the extra colour management.
#
# == Usage ==
#
# There is one part to this plugin:
#
#   1.  A tag you can use in the <head> of a page to get the custom CSS
#       variables (if any) for this page:
#
#           {% tint_color_css %}
#
#       The output of this tag may be empty, if this page doesn't use
#       any custom colours.
#

require_relative 'utils/contrast'

module Jekyll
  class TintColorCssTag < Liquid::Tag
    def render(context)
      page = context.registers[:page]

      colors = page.fetch('colors', {})

      primary_color_light = colors['css_light']
      primary_color_dark = colors['css_dark']

      if primary_color_light.nil? && primary_color_dark.nil?
        return
      end

      sass = <<~SCSS
        @import "variables.scss";

        @include create_colour_variables(#{primary_color_light}, #{primary_color_dark});
      SCSS

      css = context.registers[:site]
                   .find_converter_instance(Jekyll::Converters::Scss)
                   .convert(sass)

      <<~HTML
        <style>#{css}</style>
      HTML
    end
  end
end

Liquid::Template.register_tag('tint_color_css', Jekyll::TintColorCssTag)
