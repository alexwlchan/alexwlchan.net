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

# Given the front matter from a page, get the CSS colors (if any).
def get_css_colors(page)
  colors = page.fetch('colors', {})

  primary_color_light = colors['css_light']
  primary_color_dark = colors['css_dark']

  if primary_color_light.nil? && primary_color_dark.nil?
    return
  end

  { 'light' => primary_color_light, 'dark' => primary_color_dark }
end

# Throws an error if the CSS colors on a given page don't have enough
# contrast with the white/black backgrounds.
def ensure_sufficient_contrast(css_colors)
  contrast_with_white = contrast(css_colors['light'], '#ffffff')

  if contrast_with_white < 4.5
    throw "light color: insufficient contrast between white and #{css_colors['light']}: #{contrast_with_white} < 4.5"
  end

  contrast_with_black = contrast(css_colors['dark'], '#000000')

  if contrast_with_black < 4.5
    throw "dark color: insufficient contrast between black and #{css_colors['dark']}: #{contrast_with_black} < 4.5"
  end
end

Jekyll::Hooks.register :pages, :pre_render do |page|
  css_colors = get_css_colors(page.data)

  unless css_colors.nil?
    ensure_sufficient_contrast(css_colors)
  end
end

Jekyll::Hooks.register :documents, :pre_render do |doc|
  css_colors = get_css_colors(doc.data)

  unless css_colors.nil?
    ensure_sufficient_contrast(css_colors)
  end
end

module Jekyll
  class TintColorCssTag < Liquid::Tag
    def render(context)
      page = context.registers[:page]

      css_colors = get_css_colors(page)

      if css_colors.nil?
        return
      end

      sass = <<~SCSS
        @import "variables.scss";

        @include create_colour_variables(#{css_colors['light']}, #{css_colors['dark']});
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
