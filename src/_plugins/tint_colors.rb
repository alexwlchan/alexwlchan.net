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
# There are two parts to this plugin:
#
#   1.  A pre-render hook that checks there's sufficient contrast between
#       the chosen tint color and the background of the page.
#
#   2.  A tag you can use in the <head> of a page to get the custom CSS
#       variables (if any) for this page:
#
#           {% tint_color_css %}
#
#       The output of this tag may be empty, if this page doesn't use
#       any custom colours.
#

require_relative 'utils/contrast'

# Throws an error if the CSS colors on a given page don't have enough
# contrast with the white/black backgrounds.
def ensure_sufficient_contrast(page_data)
  colors = page_data.fetch('colors', {})

  primary_color_light = colors['css_light']
  primary_color_dark = colors['css_dark']

  if primary_color_light.nil? && primary_color_dark.nil?
    return
  end

  if contrast(primary_color_light, '#ffffff') < 4.5
    throw "light color: insufficient contrast between white and #{primary_color_light}: #{contrast(primary_color_light, '#ffffff')} < 4.5"
  end

  return unless contrast(primary_color_dark, '#000000') < 4.5

  throw "dark color: insufficient contrast between black and #{primary_color_dark}: #{contrast(primary_color_dark, '#000000')} < 4.5"
end

Jekyll::Hooks.register :pages, :pre_render do |page|
  ensure_sufficient_contrast(page.data)
end

Jekyll::Hooks.register :documents, :pre_render do |doc|
  ensure_sufficient_contrast(doc.data)
end

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
