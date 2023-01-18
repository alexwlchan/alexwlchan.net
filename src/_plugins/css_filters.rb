require 'nokogiri'

module Jekyll
  module ExtractStyleTagFilter
    def remove_inline_styles(html)
      unless html.include? '<style'
        return html
      end

      doc = Nokogiri::HTML.fragment(html)
      doc.xpath('style|.//style').remove
      doc.to_s
    end

    def get_inline_styles(html)
      unless html.include? '<style'
        return ''
      end

      doc = Nokogiri::HTML.fragment(html)

      inline_styles = Hash.new { [] }

      doc.xpath('style|.//style').each do |style|
        style_type = style.get_attribute('type')
        media = style.get_attribute('media')

        if style_type == 'x-text/scss'
          site = @context.registers[:site]
          converter = site.find_converter_instance(Jekyll::Converters::Scss)
          css = converter.convert(<<~SCSS
            @import "mixins.scss";
            @import "variables.scss";

            #{style.text}
          SCSS
                                 )

          inline_styles[media] <<= css
        else
          inline_styles[media] <<= style.text
        end
      end

      if inline_styles.empty?
        return ''
      end

      lines = inline_styles.map do |media, css|
        if media.nil?
          css
        else
          "@media #{media} { #{css.join("\n")} }"
        end
      end

      <<~HTML
      <style>
        #{lines.join("\n")}
      </style>
      HTML
    end
  end
end

Liquid::Template.register_filter(Jekyll::ExtractStyleTagFilter)
