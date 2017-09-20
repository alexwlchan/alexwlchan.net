require 'nokogiri'

module Jekyll
  module AtomFeedFilters
    def strip_html_attrs(html)
      doc = Nokogiri::HTML.fragment(html)

      doc.xpath('@style|.//@style|@data-lang|.//@data-lang|@controls|.//@controls').remove
      # doc.xpath('@data-lang|.//@data-lang').remove
      # doc.xpath('@controls|.//@controls').remove

      doc.to_s
    end
  end
end

Liquid::Template::register_filter(Jekyll::AtomFeedFilters)
