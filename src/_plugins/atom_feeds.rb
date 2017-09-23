require 'nokogiri'

module Jekyll
  module AtomFeedFilters

    # Remove inline attributes from an HTML string that aren't allowed in
    # an Atom feed, according to https://github.com/rubys/feedvalidator
    #
    # Params:
    # +html+:: HTML string to clean.
    #
    def strip_html_attrs(html)
      doc = Nokogiri::HTML.fragment(html)
      doc.xpath('@style|.//@style|@data-lang|.//@data-lang|@controls|.//@controls').remove
      doc.to_s
    end

    # Minify an XML string.
    #
    # Here minification just means removing all whitespace that comes
    # after a '>'.  This isn't as nice as using a proper XML parser, but
    # I've been unable to get that working in Ruby.
    # TODO: Use Nokogiri to do this properly.
    #
    # Params:
    # +xml+:: XML string to minify.
    #
    def minify_xml(xml)
      xml.gsub(%r|>\s+|, ">")
    end

  end
end

Liquid::Template::register_filter(Jekyll::AtomFeedFilters)
