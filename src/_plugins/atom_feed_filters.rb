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

    # Replace twemoji SVG images with the plaintext emoji counterparts; these
    # render better in RSS readers.
    doc.xpath('.//img[@class="twemoji"]').each do |img|
      emoji = img.get_attribute('alt')
      img.replace Nokogiri::HTML.fragment(emoji)
    end
  end

  # Fix references in images and <a> tags.
  #
  # Normally these are relative URLs, e.g. <a href="/another-page/">
  # That works fine if you're looking at the site in a web browser, but
  # if you're in an RSS feed all the links will be broken.  Add the hostname
  # to the feed URLs.
  def self.fix_relative_url(tag, options)
    attribute_name = options[:attribute]
    existing_value = tag.get_attribute(attribute_name)

    values = existing_value.split(', ')

    new_values = values.map do |v|
      if (v.start_with? '/images') || (v.start_with? '/files')
        "https://alexwlchan.net#{v}"
      else
        v
      end
    end

    tag.set_attribute(attribute_name, new_values.join(', '))
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

      tags_with_relative_attributes = [
        { xpath: './/img', attribute: 'src' },
        { xpath: './/a', attribute: 'href' },
        { xpath: './/source', attribute: 'srcset' },

        # NOTE: <image> tags appear in inline SVGs, not HTML.
        { xpath: './/image', attribute: 'src' }
      ]

      tags_with_relative_attributes.each do |tag|
        doc.xpath(doc[:xpath]).each { |t| HtmlModifiers.fix_relative_url(t, tag) }
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
