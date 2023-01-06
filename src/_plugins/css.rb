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

def convert_css(site, css_string)
  converter = site.find_converter_instance(::Jekyll::Converters::Scss)
  converter.convert(css_string)
end

module Jekyll
  class CssStylesheet < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @css_cache = Hash.new()
      @md5_cache = Hash.new()
    end

    def render(context)
      site = context.registers[:site]
      src = site.config["source"]
      dst = site.config["destination"]

      if context.registers[:page].nil?
        color = "#d01c11"
      else
        color = (context.registers[:page]["theme"] || {})["color"] || "#d01c11"
      end

      if context.registers[:page].nil? || context.registers[:page]["date"].nil?
        year = nil
      else
        year = context.registers[:page]["date"].year
        slug = context.registers[:page]["slug"]
      end

      # If there's an individual stylesheet for this page, then we concatenate
      # it with the default stylesheet and write it to an appropriate name,
      # e.g. /styles/2022/2022-in-reading.css
      #
      # This matches the per-year naming convention used for other resources.
      if !year.nil? and File.exist? "#{src}/styles/#{year}/#{slug}.scss"
        css = convert_css(site, <<-EOT
          $primary-color: #{color};

          @import "_main.scss";

          #{File.open("#{src}/styles/#{year}/#{slug}.scss").read}
          EOT
        )

        md5 = Digest::MD5.new.hexdigest css

        out_path = "/styles/#{year}/#{slug}.css"
        FileUtils.mkdir_p File.dirname("#{dst}/#{out_path}")
        File.write("#{dst}#{out_path}", css)

      # If there's no individual stylesheet for this page, then we just use
      # the default stylesheet with the page's tint colour.
      #
      # These are shared among all pages with the same colour, to reduce
      # the number of individual files and improve caching.
      else
        out_path = "/styles/style.#{color.gsub('#', '')}.css"

        # We only need to create and write the CSS file for this colour
        # if one hasn't already
        unless @css_cache.has_key? color
          @css_cache[color] = convert_css(site, <<-EOT
            $primary-color: #{color};

            @import "_main.scss";
            EOT
          )

          @md5_cache[color] = Digest::MD5.new.hexdigest @css_cache[color]

          FileUtils.mkdir_p File.dirname("#{dst}/#{out_path}")
          File.write("#{dst}#{out_path}", @css_cache[color])

          md5 = @md5_cache[color]
        end
      end

      <<-EOT
        <link rel="stylesheet" href="#{out_path}?md5=#{md5}">
      EOT
    end
  end
end

Liquid::Template.register_tag("css_stylesheet", Jekyll::CssStylesheet)
