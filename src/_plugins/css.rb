# Creates the CSS file and <link> tag for pages.
#
# There's a base CSS file for the entire site (in `_scss/_main.scss`),
# which individual pages can customise in two ways:
#
#     - Setting a custom tint colour in the front matter.
#
#     - Adding extra CSS rules in `styles/${year}/${slug}.scss`.
#       Note that this has access to all the mixins/functions/variables
#       in the rest of the SCSS styles.
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

def convert_css(site, css_string)
  converter = site.find_converter_instance(Jekyll::Converters::Scss)
  converter.convert(css_string)
end

Jekyll::Hooks.register :site, :pre_render do
  FileUtils.rm_f('_site/styles/style.css')
  FileUtils.rm_f('.header_colours.txt')
end

module Jekyll
  class CssStylesheet < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @css_cache = {}
      @md5_cache = {}
    end

    def render(context)
      site = context.registers[:site]
      src = site.config['source']
      dst = site.config['destination']

      # Create the base style sheet
      unless File.exist? "#{dst}/styles/style.css"
        base_css = convert_css(site, File.read("#{src}/_scss/style.scss"))

        @base_css_md5 = Digest::MD5.new.hexdigest base_css

        out_path = '/styles/style.css'
        FileUtils.mkdir_p File.dirname("#{dst}/#{out_path}")
        File.write("#{dst}#{out_path}", base_css)
      end

      primary_color_light = if context.registers[:page].nil?
                              '#d01c11'
                            else
                              (context.registers[:page]['colors'] || {})['css_light'] || '#d01c11'
                            end

      primary_color_dark = if context.registers[:page].nil?
                             '#FF4242'
                           else
                             (context.registers[:page]['colors'] || {})['css_dark'] || '#FF4242'
                           end

      if contrast(primary_color_light, '#ffffff') < 4.5
        throw "light color: insufficient contrast between white and #{primary_color_light}: #{contrast(primary_color_light, '#ffffff')} < 7"
      end

      if contrast(primary_color_dark, '#000000') < 4.5
        throw "dark color: insufficient contrast between black and #{primary_color_dark}: #{contrast(primary_color_dark, '#000000')} < 7"
      end

      open('.header_colours.txt', 'a') do |f|
        f.puts primary_color_light
        f.puts primary_color_dark
      end

      # If there's no individual stylesheet for this page, then we just use
      # the default stylesheet with the page's tint colour.
      #
      # These are shared among all pages with the same colour, to reduce
      # the number of individual files and improve caching.
      else
        # We only need to create and write the CSS file for this colour
        # if one hasn't already
        unless @css_cache.key? primary_color_light
          @css_cache[primary_color_light] = convert_css(site, <<~SCSS
          $primary-color-light: #{primary_color_light};
          $primary-color-dark:  #{primary_color_dark};

            @import "_main.scss";
          SCSS
          )
        end

        css = @css_cache[primary_color_light]
      end

      md5 = @md5_cache[color]

      <<~HTML
        <link rel="stylesheet" href="/styles/style.css?md5=#{@base_css_md5}">
        <style>#{css}</style>
      HTML
    end
  end
end

Liquid::Template.register_tag('css_stylesheet', Jekyll::CssStylesheet)
