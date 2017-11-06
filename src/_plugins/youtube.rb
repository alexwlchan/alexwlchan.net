# This is a plugin for embedding YouTube videos.
#
# Insert the full URL of the YouTube video in question, for example:
#
#     {% youtube https://www.youtube.com/watch?v=Ej2EJVMkTKw %}
#

require 'cgi'
require 'uri'


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

Liquid::Template.register_tag('youtube', Jekyll::YouTubeTag)
