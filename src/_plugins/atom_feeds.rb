require 'nokogiri'

module Jekyll
  module AtomFeedFilters
    def strip_html_attrs(html)
      doc = Nokogiri::HTML.fragment(html)
      doc.xpath('@style|.//@style|@data-lang|.//@data-lang|@controls|.//@controls').remove
      doc.to_s
    end

    # Matches all whitespace that follows
    #   1. A '>', which closes an XML tag or
    #   2. A '}', which closes a Liquid tag
    # We will strip all of this whitespace to minify the template
    #
    # This isn't as nice as using a proper XML parser, but I've been unable
    # to get that working in Ruby!  This is taken from jekyll-feed.
    MINIFY_REGEX = %r!(?<=>|})\s+!

    def minify_xml(xml)
      xml.gsub(MINIFY_REGEX, "")
    end
  end
end

Liquid::Template::register_filter(Jekyll::AtomFeedFilters)
