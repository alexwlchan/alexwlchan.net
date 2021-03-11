# This plugin provides some filters that I use when generating the Atom feed.
# I write the site in Markdown and test it in my browser; I need to make some
# changes for everything to look okay in RSS.

require "nokogiri"

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
      doc.xpath('style|@style|.//@style|@data-lang|.//@data-lang|@controls|.//@controls|@aria-hidden|.//@aria-hidden').remove

      # Remove the small blue bird I add to tweet blockquotes from the RSS feed;
      # it only exists for display purposes.
      doc.xpath('.//div[@class="twitter_birb"]').remove

      # Remove the avatar from tweets; the RSS feed should just include the
      # plaintext blockquote.
      doc.xpath('.//span[@class="avatar"]').remove

      # Fix references in images and <a> tags.  Normally these are relative URLs,
      # e.g. <a href="/another-page/">  That works fine if you're looking at the
      # site in a web browser, but if you're in an RSS feed all the links will be
      # broken.  Add the hostname to the feed URLs.
      doc.xpath(".//img").each { |img_tag|
        if img_tag["src"].start_with?("/images")
          img_tag["src"] = "https://alexwlchan.net" + img_tag["src"]
        end
      }

      doc.xpath(".//a").each { |a_tag|
        if a_tag["href"].start_with?("/")
          a_tag["href"] = "https://alexwlchan.net" + a_tag["href"]
        end
      }

      # Fix references to images in inline SVGs.
      doc.xpath(".//image").each { |image|
        if image["href"].start_with?("/images")
          image["href"] = "https://alexwlchan.net" + image["href"]
        end
      }

      # Replace any custom separator icons (which are <center> tags with a couple
      # of attributes and an inline SVG) with a plain <hr/>.
      doc.xpath('.//center').each { |c|
        c.replace("<hr>")
      }

      doc.to_s
    end
    
    def pretty_print_xml(xml)
      doc = Nokogiri.XML(xml) do |config|
        config.default_xml.noblanks
      end
      doc.to_xml(:indent => 2)
    end
  end
end

Liquid::Template::register_filter(Jekyll::AtomFeedFilters)
