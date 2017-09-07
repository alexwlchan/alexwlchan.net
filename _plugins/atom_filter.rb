require 'uri'

module Jekyll
  module AtomFilter

    def rfc2822_date(date)
      date.rfc2822
    end

    # Create a TagURI
    # See http://web.archive.org/web/20110514113830/http://diveintomark.org/archives/2004/05/28/howto-atom-id
    # Based on feedgenerator.django.utils.feedgenerator
    def atom_id(post)
      if post["date"]
        d = ",#{post["date"].strftime("%Y-%m-%d")}"
      else
        d = ""
      end

      uri = URI(@context.registers[:site].config["url"] + post.url)
      if uri.fragment
        fragment = "/#{uri.fragment}"
      else
        fragment = ""
      end

      "tag:#{uri.hostname}#{d}:#{uri.path}#{fragment}"
    end
  end
end

Liquid::Template::register_filter(Jekyll::AtomFilter)
