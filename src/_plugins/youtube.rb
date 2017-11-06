# This is a plugin for embedding YouTube videos.
#
# Insert the full URL of the YouTube video in question, for example:
#
#     {% youtube https://www.youtube.com/watch?v=Ej2EJVMkTKw %}
#

require 'cgi'
require 'uri'

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
      doc = Nokogiri::HTML.fragment(html)
      doc.xpath('style|@style|.//@style|@data-lang|.//@data-lang|@controls|.//@controls').remove
      doc.to_s
    end

  end
end


module Jekyll
  class YouTubeTag < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @url = text.split(" ").last
      query_string = URI.parse(@url).query
      @video_id = CGI.parse(query_string)["v"].first
    end

    def render(context)
      path = "/slides/#{@deck}/#{@deck}.#{@number.to_s.rjust(3, '0')}.png"
<<-EOT
<iframe width="560" height="315" src="https://www.youtube.com/embed/#{@video_id}" frameborder="0" allowfullscreen></iframe>
EOT
    end
  end
end


Liquid::Template::register_filter(Jekyll::YouTubeAtomFeedFilters)
Liquid::Template.register_tag('youtube', Jekyll::YouTubeTag)
