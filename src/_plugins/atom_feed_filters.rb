# frozen_string_literal: true

# This plugin provides some filters that I use when generating the Atom feed.
# I write the site in Markdown and test it in my browser; I need to make some
# changes for everything to look okay in RSS.

require 'nokogiri'

module HtmlModifiers
  def self.fix_tweets_for_rss(doc)
    # Remove the small blue bird I add to tweet blockquotes; it's only there
    # so that my faux tweet embeds look more like real tweets.
    doc.xpath('.//div[@class="twitter_birb"]').remove

    # Remove the avatar from tweets; the RSS feed should just include the
    # plaintext blockquote.
    doc.xpath('.//span[@class="avatar"]').remove
  end
end

module Jekyll
  module AtomFeedFilters
    def fix_html_for_feed_readers(html)
      doc = Nokogiri::HTML.fragment(html)

      # Remove inline attributes from an HTML string that aren't allowed in
      # an Atom feed, according to https://github.com/rubys/feedvalidator
      doc.xpath('style|@style|.//@style|@data-lang|.//@data-lang|@controls|.//@controls|@aria-hidden|.//@aria-hidden').remove

      HtmlModifiers.fix_tweets_for_rss(doc)

      # Fix references in images and <a> tags.  Normally these are relative URLs,
      # e.g. <a href="/another-page/">  That works fine if you're looking at the
      # site in a web browser, but if you're in an RSS feed all the links will be
      # broken.  Add the hostname to the feed URLs.
      doc.xpath('.//img').each do |img_tag|
        img_tag['src'] = "https://alexwlchan.net#{img_tag['src']}" if img_tag['src'].start_with?('/images')
      end

      doc.xpath('.//source').each do |source_tag|
        next if source_tag['srcset'].nil?

        source_tag['srcset'] = source_tag['srcset']
                               .split(',')
                               .map do |s|
          if s.strip.start_with?('/images')
            "https://alexwlchan.net#{s.strip}"
          else
            s
          end
        end
                               .join(', ')
      end

      doc.xpath('.//a').each do |a_tag|
        a_tag['href'] = "https://alexwlchan.net#{a_tag['href']}" if a_tag['href']&.start_with?('/')
      end

      # Fix references to images in inline SVGs.
      doc.xpath('.//image').each do |image|
        image['href'] = "https://alexwlchan.net#{image['href']}" if image['href'].start_with? '/images'
      end

      # Remove any elements that have data-rss-exclude="true"
      #
      # e.g. <img src="example.jpg" data-rss-exclude="true">
      #
      # This gives me a way to exclude elements from the RSS.
      doc.xpath('.//*[@data-rss-exclude="true"]').remove

      # Removing elements may have left empty paragraphs; remove them.
      doc.to_s.gsub('<p></p>', '')
    end

    def pretty_print_xml(xml)
      doc = Nokogiri.XML(xml) do |config|
        config.default_xml.noblanks
      end
      doc.to_xml(indent: 2)
    end
  end
end

Liquid::Template.register_filter(Jekyll::AtomFeedFilters) if defined? Liquid
