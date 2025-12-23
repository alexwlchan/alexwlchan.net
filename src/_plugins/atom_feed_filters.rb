# frozen_string_literal: true

# This plugin provides some filters that I use when generating the Atom feed.
# I write the site in Markdown and test it in my browser; I need to make some
# changes for everything to look okay in RSS.

require 'nokogiri'

module HtmlModifiers
  # Remove any elements that have `data-norss`.
  #
  # This is a way I can signal in my markup that a particular element is
  # for the website only, and should not be included in the RSS.
  def self.remove_norss_elements(doc)
    doc.xpath('.//*[@data-norss]').remove
  end

  def self.fix_social_embeds_for_rss(doc)
    doc.css('blockquote.embed').each do |embed|
      embed.css('svg.logo').remove
      embed.css('img.avatar').remove
    end

    # Replace twemoji SVG images with the plaintext emoji counterparts; these
    # render better in RSS readers.
    doc.css('img.twemoji').each do |img|
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
  def self.fix_tags_with_relative_urls(doc)
    tags_with_relative_attributes = [
      { css: 'img', attribute: 'src' },
      { css: 'a', attribute: 'href' },
      { css: 'source', attribute: 'srcset' },

      # NOTE: <image> tags appear in inline SVGs, not HTML.
      { css: 'image', attribute: 'src' }
    ]

    tags_with_relative_attributes.each do |tag|
      doc.css(tag[:css]).each { |t| fix_relative_url(t, tag) }
    end
  end

  def self.fix_relative_url(tag, options)
    attribute_name = options[:attribute]
    existing_value = tag.get_attribute(attribute_name)

    values = existing_value.split(',').map(&:strip)

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

      # Remove all inline <style> tags
      doc.xpath('style').remove

      # Remove inline attributes from an HTML string that aren't allowed in
      # an Atom feed, according to https://github.com/rubys/feedvalidator
      attribute_names = %w[style controls aria-hidden]
                        .flat_map { |name| ["@#{name}", ".//@#{name}"] }
      doc.xpath(attribute_names.join('|')).remove

      HtmlModifiers.remove_norss_elements(doc)
      HtmlModifiers.fix_social_embeds_for_rss(doc)
      HtmlModifiers.fix_tags_with_relative_urls(doc)

      # Removing elements may have left empty paragraphs; remove them.
      doc.to_s.gsub('<p></p>', '')
    end

    # According to https://github.com/rubys/feedvalidator, embedding
    # <iframe> in an RSS feed can be a security risk, so instead we replace
    # such YouTube iframes with a flat link to the page.
    #
    # Params:
    # +html+:: HTML string to clean.
    #
    def fix_youtube_iframes(html)
      doc = Nokogiri::HTML(html)
      doc.search('//iframe').each do |f_node|
        video_id = f_node.attributes['id'].to_s.split('_').last
        url = "https://youtube.com/watch?v=#{video_id}"
        new_node = Nokogiri::HTML.fragment("<p><a href=\"#{url}\">#{url}</a></p>")
        f_node.replace(new_node)
      end
      doc.at_xpath('//body').to_s[('<body>'.length)..-('</body>'.length + 1)]
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
