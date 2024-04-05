# Creates the CSS file and <link> tag for pages.
#
# There's a base CSS file for the entire site (in `_scss/_main.scss`),
# which individual pages can customise in two ways:
#
#     - Setting a custom tint colour in the front matter.
#
# This plugin will:
#
#     - Create an appropriate CSS file for the page
#     - Create a <link> tag that points to it
#     - Include a query parameter to cache-bust if/when the CSS changes
#
require 'digest'
require 'fileutils'

require_relative 'utils/contrast'

Jekyll::Hooks.register :site, :pre_render
  open('.header_colours.txt', 'w') do |f|
    f.puts '#d01c11'
  end
end

def get_page_color(page, name)
  if page.nil?
    nil
  else
    (page['colors'] || {})[name]
  end
end

module Jekyll
  class CssStylesheet < Liquid::Tag
    def render(context)
      primary_color_light = get_page_color(context.registers[:page], 'css_light')
      primary_color_dark = get_page_color(context.registers[:page], 'css_dark')

      if primary_color_light.nil? && primary_color_dark.nil?
        return
      end

      if contrast(primary_color_light, '#ffffff') < 4.5
        throw "light color: insufficient contrast between white and #{primary_color_light}: #{contrast(primary_color_light, '#ffffff')} < 4.5"
      end

      if contrast(primary_color_dark, '#000000') < 4.5
        throw "dark color: insufficient contrast between black and #{primary_color_dark}: #{contrast(primary_color_dark, '#000000')} < 4.5"
      end

      open('.header_colours.txt', 'a') do |f|
        f.puts primary_color_light
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

Liquid::Template.register_tag('css_stylesheet', Jekyll::CssStylesheet)
