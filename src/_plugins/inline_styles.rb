# This plugin is for adding extra styles to posts/pages.
#
# It tries to balance a couple of requirements:
#
#   1.  I want to have per-post and per-page styles that aren't in the
#       global stylesheet.
#
#   2.  I sometimes want access to Sass variables (e.g. palette colours)
#       from these per-page styles.
#
#   3.  You're only meant to put <style> tags in the <head> of a document.
#
# == How it works ==
#
# In the body of posts, I can create <style> blocks.  I can also create
# blocks with the attribute `type="x-text/scss"`.
#
# In the final template, these <style> blocks will be removed from the
# <body>, and consolidated and inserted in the <head>.  Any SCSS blocks
# will run through the site's Sass processor first.

require 'nokogiri'

class InlineStylesFilters
  def self.get_inline_styles(html, site)
    unless html.include? '<style'
      return { 'html' => html, 'inline_styles' => '' }
    end

    doc = Nokogiri::HTML(html)

    inline_styles = Hash.new { [] }

    doc.xpath('style|.//style').each do |style|
      style_type = style.get_attribute('type')
      media = style.get_attribute('media')

      if style_type == 'x-text/scss'
        converter = site.find_converter_instance(Jekyll::Converters::Scss)
        css = converter.convert(<<~SCSS
          @import "mixins.scss";

          #{style.text}
        SCSS
                               )
        inline_styles[media] <<= css.strip
      else
        inline_styles[media] <<= style.text.strip
      end

      # NOTE: this deliberately bypasses the Nokogiri HTML rendering,
      # and just does a regex-esque find and replace.
      #
      # There are certain issues where, e.g. Nokogiri will try to insert
      # a closing </source> tag which is redundant, so instead we operate
      # on the raw HTML and try to preserve the existing formatting as
      # much as possible.
      html = html.gsub(%r{<style[^>]*>\s*#{Regexp.escape(style.text)}\s*</style>}, '')
    end

    if inline_styles.empty?
      return {
        'html' => html,
        'inline_styles' => ''
      }
    end

    lines = inline_styles.map do |media, css|
      if media.nil?
        css
      else
        "@media #{media} { #{css.join("\n")} }"
      end
    end

    {
      'html' => html,
      'inline_styles' => lines.join(' ')
    }
  end
end

module Jekyll
  module InlineStyles
    def get_inline_styles(html)
      cache = Jekyll::Cache.new('InlineStyles')

      cache.getset(html) do
        site = @context.registers[:site]
        InlineStylesFilters.get_inline_styles(html, site)
      end
    end
  end
end

if defined? Liquid
  Liquid::Template.register_filter(Jekyll::InlineStyles)
end
