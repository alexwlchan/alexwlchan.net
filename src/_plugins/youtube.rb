# This is a plugin for embedding YouTube videos.
#
# Insert the full URL of the YouTube video in question, for example:
#
#     {% youtube https://www.youtube.com/watch?v=Ej2EJVMkTKw %}
#

require 'cgi'
require 'uri'

require 'nokogiri'


module Jekyll
  module YouTubeAtomFeedFilters

    # According to https://github.com/rubys/feedvalidator, embedding
    # <iframe> in an RSS feed can be a security risk, so instead we replace
    # such YouTube iframes with a flat link to the page.
    #
    # TODO: Regex matching is crappy, use Nokogiri to do it properly.
    #
    # Params:
    # +html+:: HTML string to clean.
    #
    def fix_youtube_iframes(html)
      doc = Nokogiri::HTML(html)
      doc.search('//iframe').each do |f_node|
        video_id = f_node.attributes["id"].to_s.split("_").last
        url = "https://youtube.com/watch?v=#{video_id}"
        new_node = Nokogiri::HTML.fragment("<p><a href=\"#{url}\">#{url}</a></p>")
        f_node.replace(new_node)
      end
      doc.to_s
    end

  end
end

Liquid::Template::register_filter(Jekyll::YouTubeAtomFeedFilters)


module Jekyll
  class YouTubeTag < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @url = text.split(" ").last
      query_string = URI.parse(@url).query
      @video_id = CGI.parse(query_string)["v"].first
    end

    def render(context)
      <<-EOT
<iframe class="youtube"
        id="youtube_#{@video_id}"
        width="560" height="315"
        src="https://www.youtube.com/embed/#{@video_id}"
        frameborder="0" allowfullscreen></iframe>
EOT
    end
  end
end

Liquid::Template.register_tag('youtube', Jekyll::YouTubeTag)
